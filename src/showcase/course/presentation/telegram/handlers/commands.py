"""Command handlers for Telegram bot."""

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from common.infrastructure.config.deployment_meta import DeploymentMeta
from showcase.course.application.dtos.queries import GetCoursesSearchQuery
from showcase.course.application.interfaces.usecases.query import (
    IGetCoursesUseCase,
)
from showcase.course.application.interfaces.usecases.query.get_course_by_id_usecase import (
    IGetCourseByIdUseCase,
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


class CommandHandler:
    """Handler for Telegram bot commands."""

    def __init__(
        self,
        deploy_meta: DeploymentMeta,
        get_courses_use_case: IGetCoursesUseCase,
        get_course_by_id_use_case: IGetCourseByIdUseCase,
        get_courses_search_use_case: IGetCoursesSearchUseCase,
        course_list_service: CourseListService,
    ) -> None:
        self.deploy_meta = deploy_meta
        self.get_courses_use_case = get_courses_use_case
        self.get_course_by_id_use_case = get_course_by_id_use_case
        self.get_courses_search_use_case = get_courses_search_use_case
        self.course_list_service = course_list_service
        self.router = Router()

        self._register_handlers()

    def _register_handlers(self) -> None:
        """Register command handlers."""
        self.router.message.register(self._handle_start, CommandStart())
        self.router.message.register(self._handle_help, Command("help"))
        self.router.message.register(self._handle_list, Command("list"))
        self.router.message.register(self._handle_search, Command("search"))

    async def _handle_start(self, message: Message) -> None:
        """Handle /start command."""
        text = (
            "👋 Добро пожаловать в бот каталога курсов!\n\n"
            "Доступные команды:\n"
            "/list - показать все курсы\n"
            "/search &lt;запрос&gt; - поиск курсов\n"
            "/help - помощь\n\n"
            "Или используйте меню ниже:"
        )
        keyboard = build_main_menu_keyboard()
        await message.answer(text, reply_markup=keyboard)

    async def _handle_help(self, message: Message) -> None:
        """Handle /help command."""
        text = (
            "📖 <b>Помощь</b>\n\n"
            "<b>Команды:</b>\n"
            "/start - начать работу\n"
            "/list - показать все курсы\n"
            "/search &lt;запрос&gt; - поиск курсов по тексту\n"
            "/help - эта справка\n\n"
            "<b>Использование:</b>\n"
            "• Используйте меню для навигации\n"
            "• Для рекомендаций нажмите '✨ Рекомендации' и введите свой запрос\n"
            "• Используйте фильтры для уточнения поиска\n\n"
            f'🖥️ Также посетите нашу <a href="{self.deploy_meta.external_url}">веб-версию</a>!'
        )
        keyboard = build_main_menu_keyboard()
        await message.answer(text, reply_markup=keyboard)

    async def _handle_list(self, message: Message, state: FSMContext) -> None:
        """Handle /list command."""
        await state.clear()  # Reset filters
        await self.course_list_service.display_course_list(message, state, page=1)

    async def _handle_search(self, message: Message) -> None:
        """Handle /search command."""
        # Extract search query from command
        parts = (message.text or "").split(maxsplit=1)
        if len(parts) < 2:
            await message.answer(
                "❌ Укажите запрос для поиска.\nПример: /search Python"
            )
            return

        query_text = parts[1]
        search_query = GetCoursesSearchQuery(query=query_text, limit=10)
        courses = await self.get_courses_search_use_case.execute(search_query)

        if not courses:
            await message.answer(f"❌ По запросу '{query_text}' ничего не найдено.")
            return

        text = format_course_list(courses)
        keyboard = build_course_list_keyboard(
            courses, page=1, has_next=len(courses) >= 10
        )

        await message.answer(text, reply_markup=keyboard)
