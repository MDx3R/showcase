"""Filter-related callback handlers."""

from uuid import UUID

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from showcase.category.application.dtos.queries import GetCategoriesQuery
from showcase.category.application.interfaces.usecases.query.get_categories_usecase import (
    IGetCategoriesUseCase,
)
from showcase.course.domain.value_objects import CourseStatus, Format
from showcase.course.presentation.telegram.keyboards.builder import (
    build_category_filter_keyboard,
    build_format_filter_keyboard,
    build_status_filter_keyboard,
)
from showcase.course.presentation.telegram.services.course_list_service import (
    CourseListService,
)


class FilterCallbackHandler:
    """Handler for filter callbacks."""

    def __init__(
        self,
        get_categories_use_case: IGetCategoriesUseCase,
        course_list_service: CourseListService,
    ) -> None:
        self.get_categories_use_case = get_categories_use_case
        self.course_list_service = course_list_service
        self.router = Router()

        self._register_handlers()

    def _register_handlers(self) -> None:
        self.router.callback_query.register(
            self._handle_filter_format, F.data == "filter_format"
        )
        self.router.callback_query.register(
            self._handle_filter_status, F.data == "filter_status"
        )
        self.router.callback_query.register(
            self._handle_filter_category, F.data == "filter_category"
        )
        self.router.callback_query.register(
            self._handle_filter_format_select, F.data.startswith("filter_format_")
        )
        self.router.callback_query.register(
            self._handle_filter_status_select, F.data.startswith("filter_status_")
        )
        self.router.callback_query.register(
            self._handle_filter_category_select, F.data.startswith("filter_category_")
        )

    async def _handle_filter_format(self, callback: CallbackQuery) -> None:
        text = "📍 Выберите формат обучения:"
        keyboard = build_format_filter_keyboard()
        if callback.message:
            await callback.message.edit_text(text, reply_markup=keyboard)  # pyright: ignore[reportAttributeAccessIssue]
        await callback.answer()

    async def _handle_filter_status(self, callback: CallbackQuery) -> None:
        text = "📊 Выберите статус курса:"
        keyboard = build_status_filter_keyboard()
        if callback.message:
            await callback.message.edit_text(text, reply_markup=keyboard)  # pyright: ignore[reportAttributeAccessIssue]
        await callback.answer()

    async def _handle_filter_category(self, callback: CallbackQuery) -> None:
        query = GetCategoriesQuery(limit=20)
        categories = await self.get_categories_use_case.execute(query)

        if not categories:
            await callback.answer("❌ Категории не найдены.", show_alert=True)
            return

        text = "🏷 <b>Выберите категорию:</b>"
        keyboard = build_category_filter_keyboard(categories)
        if callback.message:
            await callback.message.edit_text(text, reply_markup=keyboard)  # pyright: ignore[reportAttributeAccessIssue]
        await callback.answer()

    async def _handle_filter_format_select(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        if not callback.data:
            await callback.answer("❌ Неверный формат.", show_alert=True)
            return
        format_str = callback.data.split("_", 2)[2]
        if format_str == "none":
            await state.update_data(format=None)
            extra_text = "✅ Фильтр формата сброшен."
        else:
            format_mapping = {
                "online": Format.ONLINE,
                "offline": Format.OFFLINE,
                "mixed": Format.MIXED,
            }
            format_value = format_mapping.get(format_str)
            if format_value:
                await state.update_data(format=format_value.value)
                extra_text = f"✅ Установлен фильтр: {format_value.value}"
            else:
                await callback.answer("❌ Неверный формат.", show_alert=True)
                return

        await self.course_list_service.display_course_list(
            callback, state, page=1, extra_text=extra_text
        )

    async def _handle_filter_status_select(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        if not callback.data:
            await callback.answer("❌ Неверный статус.", show_alert=True)
            return
        status_str = callback.data.split("_", 2)[2]
        if status_str == "none":
            await state.update_data(status=None)
            extra_text = "✅ Фильтр статуса сброшен."
        else:
            status_mapping = {
                "active": CourseStatus.ACTIVE,
                "enrolling": CourseStatus.ENROLLING,
                "archived": CourseStatus.ARCHIVED,
            }
            status_value = status_mapping.get(status_str)
            if status_value:
                await state.update_data(status=status_value.value)
                extra_text = f"✅ Установлен фильтр: {status_value.value}"
            else:
                await callback.answer("❌ Неверный статус.", show_alert=True)
                return

        await self.course_list_service.display_course_list(
            callback, state, page=1, extra_text=extra_text
        )

    async def _handle_filter_category_select(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        if not callback.data:
            await callback.answer("❌ Неверная категория.", show_alert=True)
            return
        category_str = callback.data.split("_", 2)[2]
        if category_str == "none":
            await state.update_data(category_id=None)
            extra_text = "✅ Фильтр категории сброшен."
        else:
            try:
                category_id = UUID(category_str)
                await state.update_data(category_id=str(category_id))
                extra_text = "✅ Установлен фильтр категории"
            except ValueError:
                await callback.answer("❌ Неверная категория.", show_alert=True)
                return

        await self.course_list_service.display_course_list(
            callback, state, page=1, extra_text=extra_text
        )
