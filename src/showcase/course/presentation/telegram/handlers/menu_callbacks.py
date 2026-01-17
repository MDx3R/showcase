"""Menu-related callback handlers."""

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from showcase.course.presentation.telegram.keyboards.builder import (
    build_filter_keyboard,
    build_main_menu_keyboard,
)
from showcase.course.presentation.telegram.services.course_list_service import (
    CourseListService,
)
from showcase.course.presentation.telegram.states.filters import FilterState


class MenuCallbackHandler:
    """Handler for menu callbacks."""

    def __init__(self, course_list_service: CourseListService) -> None:
        self.course_list_service = course_list_service
        self.router = Router()

        self._register_handlers()

    def _register_handlers(self) -> None:
        self.router.callback_query.register(
            self._handle_main_menu, F.data == "main_menu"
        )
        self.router.callback_query.register(self._handle_search, F.data == "search")
        self.router.callback_query.register(
            self._handle_recommend, F.data == "recommend"
        )
        self.router.callback_query.register(self._handle_list_all, F.data == "list_all")
        self.router.callback_query.register(self._handle_filters, F.data == "filters")

    async def _handle_main_menu(self, callback: CallbackQuery) -> None:
        text = "👋 Добро пожаловать в бот каталога курсов!\n\nВыберите действие:"
        keyboard = build_main_menu_keyboard()
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()

    async def _handle_search(self, callback: CallbackQuery, state: FSMContext) -> None:
        await state.set_state(FilterState.waiting_for_search)
        text = "🔍 Введите запрос для поиска курсов:"
        await callback.message.edit_text(text)
        await callback.answer()

    async def _handle_recommend(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        await state.set_state(FilterState.waiting_for_recommendation)
        text = (
            "✨ <b>Рекомендации</b>\n\n"
            "Опишите, какой курс вы ищете.\n"
            "Например: 'Хочу изучить Python для начинающих'"
        )
        await callback.message.edit_text(text)
        await callback.answer()

    async def _handle_list_all(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        await state.clear()  # Reset filters
        await self.course_list_service.display_course_list(callback, state, page=1)

    async def _handle_filters(self, callback: CallbackQuery) -> None:
        text = "🔧 <b>Фильтры</b>\n\nВыберите фильтр для настройки:"
        keyboard = build_filter_keyboard()
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()
