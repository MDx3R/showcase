"""Query handlers for Telegram bot (text input handling)."""

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from showcase.course.application.dtos.queries import GetCoursesSearchQuery
from showcase.course.application.interfaces.services.recommendation_service import (
    GetRecommendationsDTO,
    IRecommendationService,
)
from showcase.course.application.interfaces.usecases.query.get_courses_search_usecase import (
    IGetCoursesSearchUseCase,
)
from showcase.course.presentation.telegram.formatters.course import format_course_list
from showcase.course.presentation.telegram.keyboards.builder import (
    build_course_list_keyboard,
    build_main_menu_keyboard,
)
from showcase.course.presentation.telegram.services.course_list_service import (
    CourseListService,
)
from showcase.course.presentation.telegram.states.filters import FilterState


class QueryHandler:
    """Handler for text query inputs."""

    def __init__(
        self,
        get_courses_search_use_case: IGetCoursesSearchUseCase,
        recommendation_service: IRecommendationService,
        course_list_service: CourseListService,
    ) -> None:
        self.get_courses_search_use_case = get_courses_search_use_case
        self.recommendation_service = recommendation_service
        self.course_list_service = course_list_service
        self.router = Router()

        self._register_handlers()

    def _register_handlers(self) -> None:
        """Register query handlers."""
        self.router.message.register(
            self._handle_search_query, FilterState.waiting_for_search
        )
        self.router.message.register(
            self._handle_recommendation_query, FilterState.waiting_for_recommendation
        )

    async def _handle_search_query(self, message: Message, state: FSMContext) -> None:
        """Handle search query input."""
        query_text = message.text.strip()

        if not query_text:
            await message.answer("❌ Запрос не может быть пустым.")
            return

        search_query = GetCoursesSearchQuery(
            query=query_text, limit=10
        )  # Increased limit for better results
        try:
            courses = await self.get_courses_search_use_case.execute(search_query)
        except Exception as e:
            print(f"Error searching courses: {e}")
            text = "❌ Произошла ошибка при поиске курсов."
            keyboard = build_main_menu_keyboard()
            await message.answer(text, reply_markup=keyboard)
            await state.clear()
            return

        if not courses:
            text = f"❌ По запросу '{query_text}' ничего не найдено."
            keyboard = build_main_menu_keyboard()
            await message.answer(text, reply_markup=keyboard)
            await state.clear()
            return

        text = f"🔍 <b>Результаты поиска по запросу:</b> '{query_text}'\n\n"
        text += format_course_list(courses)
        keyboard = build_course_list_keyboard(
            courses, page=1, has_next=len(courses) >= 10
        )

        await message.answer(text, reply_markup=keyboard)
        await state.clear()

    async def _handle_recommendation_query(
        self, message: Message, state: FSMContext
    ) -> None:
        """Handle recommendation query input."""
        query_text = message.text.strip()

        if not query_text:
            await message.answer("❌ Запрос не может быть пустым.")
            return

        # Show loading message
        loading_msg = await message.answer("⏳ Анализирую ваш запрос...")

        try:
            dto = GetRecommendationsDTO(query=query_text, limit=10)
            recommendations = await self.recommendation_service.recommend(dto)
            courses = recommendations.courses

            if not courses:
                text = (
                    f"❌ К сожалению, не удалось найти подходящие курсы по запросу:\n"
                    f"'{query_text}'\n\n"
                    f"Попробуйте изменить формулировку или использовать поиск."
                )
                keyboard = build_main_menu_keyboard()
                await loading_msg.edit_text(
                    text, reply_markup=keyboard
                )
                await state.clear()
                return

            text = (
                f"✨ <b>Рекомендации для вас</b>\n\n" f"<i>Ваш запрос:</i> '{query_text}'\n\n"
            )
            text += format_course_list(courses)
            keyboard = build_course_list_keyboard(
                courses, page=1, has_next=len(courses) >= 10
            )

            await loading_msg.edit_text(
                text, reply_markup=keyboard
            )
            await state.clear()

        except Exception as e:
            print(f"Error getting recommendations: {e}")
            text = "❌ Произошла ошибка при поиске рекомендаций.\nПопробуйте использовать обычный поиск."
            keyboard = build_main_menu_keyboard()
            await loading_msg.edit_text(
                text, reply_markup=keyboard
            )
            await state.clear()
