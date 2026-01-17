"""Pagination and reset callback handlers."""

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from showcase.course.presentation.telegram.services.course_list_service import (
    CourseListService,
)


class PaginationCallbackHandler:
    """Handler for pagination and reset callbacks."""

    def __init__(self, course_list_service: CourseListService) -> None:
        self.course_list_service = course_list_service
        self.router = Router()

        self._register_handlers()

    def _register_handlers(self) -> None:
        self.router.callback_query.register(
            self._handle_page, F.data.startswith("page_")
        )
        self.router.callback_query.register(
            self._handle_back_to_list, F.data == "back_to_list"
        )
        self.router.callback_query.register(
            self._handle_filter_reset, F.data == "filter_reset"
        )

    async def _handle_page(self, callback: CallbackQuery, state: FSMContext) -> None:
        try:
            page = int(callback.data.split("_", 1)[1])
        except (ValueError, IndexError):
            await callback.answer("❌ Неверный номер страницы.", show_alert=True)
            return

        await self.course_list_service.display_course_list(callback, state, page=page)

    async def _handle_back_to_list(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        await self.course_list_service.display_course_list(callback, state, page=1)

    async def _handle_filter_reset(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        extra_text = "✅ Все фильтры сброшены."
        await self.course_list_service.display_course_list(
            callback, state, page=1, extra_text=extra_text, reset_filters=True
        )
