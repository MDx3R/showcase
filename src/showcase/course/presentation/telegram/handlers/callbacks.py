"""Callback handlers for Telegram bot."""

from uuid import UUID

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from showcase.category.application.interfaces.usecases.query.get_categories_usecase import (
    IGetCategoriesUseCase,
)
from showcase.course.application.dtos.queries import GetCourseByIdQuery, GetCoursesQuery
from showcase.course.application.interfaces.usecases.query import IGetCoursesUseCase
from showcase.course.application.interfaces.usecases.query.get_course_by_id_usecase import (
    IGetCourseByIdUseCase,
)
from showcase.course.domain.value_objects import CourseStatus, Format
from showcase.course.presentation.telegram.formatters.course import (
    format_course_detail,
    format_course_list,
)
from showcase.course.presentation.telegram.keyboards.builder import (
    build_category_filter_keyboard,
    build_course_detail_keyboard,
    build_course_list_keyboard,
    build_filter_keyboard,
    build_format_filter_keyboard,
    build_main_menu_keyboard,
    build_status_filter_keyboard,
)
from showcase.course.presentation.telegram.states.filters import FilterState


class CallbackHandler:
    """Handler for Telegram bot callback queries."""

    def __init__(
        self,
        get_courses_use_case: IGetCoursesUseCase,
        get_course_by_id_use_case: IGetCourseByIdUseCase,
        get_categories_use_case: IGetCategoriesUseCase,
    ) -> None:
        self.get_courses_use_case = get_courses_use_case
        self.get_course_by_id_use_case = get_course_by_id_use_case
        self.get_categories_use_case = get_categories_use_case
        self.router = Router()

        self._register_handlers()

    def _register_handlers(self) -> None:
        """Register callback handlers."""
        self.router.callback_query.register(
            self._handle_main_menu, lambda c: c.data == "main_menu"
        )
        self.router.callback_query.register(
            self._handle_search, lambda c: c.data == "search"
        )
        self.router.callback_query.register(
            self._handle_recommend, lambda c: c.data == "recommend"
        )
        self.router.callback_query.register(
            self._handle_list_all, lambda c: c.data == "list_all"
        )
        self.router.callback_query.register(
            self._handle_filters, lambda c: c.data == "filters"
        )
        self.router.callback_query.register(
            self._handle_course_detail,
            lambda c: c.data and c.data.startswith("course_"),
        )
        self.router.callback_query.register(
            self._handle_page, lambda c: c.data and c.data.startswith("page_")
        )
        self.router.callback_query.register(
            self._handle_enroll, lambda c: c.data and c.data.startswith("enroll_")
        )
        self.router.callback_query.register(
            self._handle_back_to_list, lambda c: c.data == "back_to_list"
        )
        self.router.callback_query.register(
            self._handle_filter_format, lambda c: c.data == "filter_format"
        )
        self.router.callback_query.register(
            self._handle_filter_status, lambda c: c.data == "filter_status"
        )
        self.router.callback_query.register(
            self._handle_filter_format_select,
            lambda c: c.data and c.data.startswith("filter_format_"),
        )
        self.router.callback_query.register(
            self._handle_filter_status_select,
            lambda c: c.data and c.data.startswith("filter_status_"),
        )
        self.router.callback_query.register(
            self._handle_filter_reset, lambda c: c.data == "filter_reset"
        )
        self.router.callback_query.register(
            self._handle_filter_category, lambda c: c.data == "filter_category"
        )
        self.router.callback_query.register(
            self._handle_filter_category_select,
            lambda c: c.data and c.data.startswith("filter_category_"),
        )

    async def _handle_main_menu(self, callback: CallbackQuery) -> None:
        """Handle main menu callback."""
        text = "👋 Добро пожаловать в бот каталога курсов!\n\n" "Выберите действие:"
        keyboard = build_main_menu_keyboard()
        await callback.message.edit_text(
            text, reply_markup=keyboard, parse_mode="Markdown"
        )
        await callback.answer()

    async def _handle_search(self, callback: CallbackQuery, state: FSMContext) -> None:
        """Handle search callback."""
        await state.set_state(FilterState.waiting_for_search)
        text = "🔍 Введите запрос для поиска курсов:"
        await callback.message.edit_text(text, parse_mode="Markdown")
        await callback.answer()

    async def _handle_recommend(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        """Handle recommend callback."""
        await state.set_state(FilterState.waiting_for_recommendation)
        text = (
            "✨ **Рекомендации**\n\n"
            "Опишите, какой курс вы ищете.\n"
            "Например: 'Хочу изучить Python для начинающих'"
        )
        await callback.message.edit_text(text, parse_mode="Markdown")
        await callback.answer()

    async def _handle_list_all(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        """Handle list all courses callback."""
        # Reset filters when showing all courses
        await state.update_data(page=1)
        page = 1
        page_size = 5
        skip = (page - 1) * page_size

        query = GetCoursesQuery(is_published=True, skip=skip, limit=page_size + 1)
        all_courses = await self.get_courses_use_case.execute(query)

        has_next = len(all_courses) > page_size
        courses = all_courses[:page_size]

        if not courses:
            await callback.message.edit_text("❌ Курсы не найдены.")
            await callback.answer()
            return

        text = format_course_list(courses, page=page)
        keyboard = build_course_list_keyboard(courses, page=page, has_next=has_next)

        await callback.message.edit_text(
            text, reply_markup=keyboard, parse_mode="Markdown"
        )
        await callback.answer()

    async def _handle_filters(self, callback: CallbackQuery) -> None:
        """Handle filters callback."""
        text = "🔧 **Фильтры**\n\nВыберите фильтр для настройки:"
        keyboard = build_filter_keyboard()
        await callback.message.edit_text(
            text, reply_markup=keyboard, parse_mode="Markdown"
        )
        await callback.answer()

    async def _handle_course_detail(self, callback: CallbackQuery) -> None:
        """Handle course detail callback."""
        course_id_str = callback.data.split("_", 1)[1]
        try:
            course_id = UUID(course_id_str)
        except ValueError:
            await callback.answer("❌ Неверный ID курса.", show_alert=True)
            return

        query = GetCourseByIdQuery(course_id=course_id)
        try:
            course = await self.get_course_by_id_use_case.execute(query)
        except ValueError:
            await callback.answer("❌ Курс не найден.", show_alert=True)
            return

        text = format_course_detail(course)
        keyboard = build_course_detail_keyboard(course_id)

        # Telegram has a limit of 4096 characters per message
        if len(text) > 4096:
            text = text[:4090] + "...\n\n(Текст обрезан)"

        await callback.message.edit_text(
            text, reply_markup=keyboard, parse_mode="Markdown"
        )
        await callback.answer()

    async def _handle_page(self, callback: CallbackQuery, state: FSMContext) -> None:
        """Handle pagination callback."""
        try:
            page = int(callback.data.split("_", 1)[1])
        except (ValueError, IndexError):
            await callback.answer("❌ Неверный номер страницы.", show_alert=True)
            return

        # Get current filter state if any
        data = await state.get_data()
        status = data.get("status")
        category_id = data.get("category_id")
        page_size = 5
        skip = (page - 1) * page_size

        # Request one extra to check if there's next page
        query = GetCoursesQuery(
            is_published=True,
            status=CourseStatus(status) if status else None,
            category_id=UUID(category_id) if category_id else None,
            skip=skip,
            limit=page_size + 1,
        )
        all_courses = await self.get_courses_use_case.execute(query)

        has_next = len(all_courses) > page_size
        courses = all_courses[:page_size]

        if not courses:
            await callback.answer("❌ Курсы не найдены.", show_alert=True)
            return

        # Update current page in state
        await state.update_data(page=page)

        text = format_course_list(courses, page=page)
        keyboard = build_course_list_keyboard(courses, page=page, has_next=has_next)

        await callback.message.edit_text(
            text, reply_markup=keyboard, parse_mode="Markdown"
        )
        await callback.answer()

    async def _handle_enroll(self, callback: CallbackQuery) -> None:
        """Handle enrollment callback."""
        course_id_str = callback.data.split("_", 1)[1]
        text = (
            f"📝 **Запись на курс**\n\n"
            f"Для записи на курс свяжитесь с администрацией.\n"
            f"ID курса: `{course_id_str}`"
        )
        await callback.answer(text, show_alert=True)

    async def _handle_back_to_list(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        """Handle back to list callback."""
        data = await state.get_data()
        status = data.get("status")
        category_id = data.get("category_id")
        page = 1
        page_size = 5
        skip = (page - 1) * page_size

        query = GetCoursesQuery(
            is_published=True,
            status=CourseStatus(status) if status else None,
            category_id=UUID(category_id) if category_id else None,
            skip=skip,
            limit=page_size + 1,
        )
        all_courses = await self.get_courses_use_case.execute(query)

        has_next = len(all_courses) > page_size
        courses = all_courses[:page_size]

        if not courses:
            await callback.message.edit_text("❌ Курсы не найдены.")
            await callback.answer()
            return

        await state.update_data(page=page)

        text = format_course_list(courses, page=page)
        keyboard = build_course_list_keyboard(courses, page=page, has_next=has_next)

        await callback.message.edit_text(
            text, reply_markup=keyboard, parse_mode="Markdown"
        )
        await callback.answer()

    async def _handle_filter_format(self, callback: CallbackQuery) -> None:
        """Handle format filter selection."""
        text = "📍 Выберите формат обучения:"
        keyboard = build_format_filter_keyboard()
        await callback.message.edit_text(
            text, reply_markup=keyboard, parse_mode="Markdown"
        )
        await callback.answer()

    async def _handle_filter_status(self, callback: CallbackQuery) -> None:
        """Handle status filter selection."""
        text = "📊 Выберите статус курса:"
        keyboard = build_status_filter_keyboard()
        await callback.message.edit_text(
            text, reply_markup=keyboard, parse_mode="Markdown"
        )
        await callback.answer()

    async def _handle_filter_format_select(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        """Handle format filter selection."""
        format_str = callback.data.split("_", 2)[2]

        if format_str == "none":
            await state.update_data(format=None)
            text = "✅ Фильтр формата сброшен."
        else:
            format_mapping = {
                "online": Format.ONLINE,
                "offline": Format.OFFLINE,
                "mixed": Format.MIXED,
            }
            format_value = format_mapping.get(format_str)
            if format_value:
                await state.update_data(format=format_value.value)
                text = f"✅ Установлен фильтр: {format_value.value}"
            else:
                await callback.answer("❌ Неверный формат.", show_alert=True)
                return

        # Apply filter and show results
        await state.update_data(page=1)
        data = await state.get_data()
        status = data.get("status")
        category_id = data.get("category_id")
        page_size = 5

        query = GetCoursesQuery(
            is_published=True,
            status=CourseStatus(status) if status else None,
            category_id=UUID(category_id) if category_id else None,
            skip=0,
            limit=page_size + 1,
        )
        all_courses = await self.get_courses_use_case.execute(query)

        has_next = len(all_courses) > page_size
        courses = all_courses[:page_size]

        if courses:
            text = f"{text}\n\n" + format_course_list(courses, page=1)
            keyboard = build_course_list_keyboard(courses, page=1, has_next=has_next)
        else:
            text = f"{text}\n\n❌ Курсы не найдены."
            keyboard = build_main_menu_keyboard()

        await callback.message.edit_text(
            text, reply_markup=keyboard, parse_mode="Markdown"
        )
        await callback.answer()

    async def _handle_filter_status_select(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        """Handle status filter selection."""
        status_str = callback.data.split("_", 2)[2]

        if status_str == "none":
            await state.update_data(status=None)
            text = "✅ Фильтр статуса сброшен."
        else:
            status_mapping = {
                "active": CourseStatus.ACTIVE,
                "enrolling": CourseStatus.ENROLLING,
                "archived": CourseStatus.ARCHIVED,
            }
            status_value = status_mapping.get(status_str)
            if status_value:
                await state.update_data(status=status_value.value)
                text = f"✅ Установлен фильтр: {status_value.value}"
            else:
                await callback.answer("❌ Неверный статус.", show_alert=True)
                return

        # Apply filter and show results
        await state.update_data(page=1)
        data = await state.get_data()
        status = data.get("status")
        category_id = data.get("category_id")
        page_size = 5

        query = GetCoursesQuery(
            is_published=True,
            status=CourseStatus(status) if status else None,
            category_id=UUID(category_id) if category_id else None,
            skip=0,
            limit=page_size + 1,
        )
        all_courses = await self.get_courses_use_case.execute(query)

        has_next = len(all_courses) > page_size
        courses = all_courses[:page_size]

        if courses:
            text = f"{text}\n\n" + format_course_list(courses, page=1)
            keyboard = build_course_list_keyboard(courses, page=1, has_next=has_next)
        else:
            text = f"{text}\n\n❌ Курсы не найдены."
            keyboard = build_main_menu_keyboard()

        await callback.message.edit_text(
            text, reply_markup=keyboard, parse_mode="Markdown"
        )
        await callback.answer()

    async def _handle_filter_category(self, callback: CallbackQuery) -> None:
        """Handle category filter selection."""
        from showcase.category.application.dtos.queries import GetCategoriesQuery

        query = GetCategoriesQuery(limit=20)
        categories = await self.get_categories_use_case.execute(query)

        if not categories:
            await callback.answer("❌ Категории не найдены.", show_alert=True)
            return

        text = "🏷 **Выберите категорию:**"
        keyboard = build_category_filter_keyboard(categories)
        await callback.message.edit_text(
            text, reply_markup=keyboard, parse_mode="Markdown"
        )
        await callback.answer()

    async def _handle_filter_category_select(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        """Handle category filter selection."""
        category_str = callback.data.split("_", 2)[2]

        if category_str == "none":
            await state.update_data(category_id=None)
            text = "✅ Фильтр категории сброшен."
        else:
            try:
                category_id = UUID(category_str)
                await state.update_data(category_id=str(category_id))
                text = f"✅ Установлен фильтр категории"
            except ValueError:
                await callback.answer("❌ Неверная категория.", show_alert=True)
                return

        # Apply filter and show results
        await state.update_data(page=1)
        data = await state.get_data()
        status = data.get("status")
        category_id = data.get("category_id")
        page_size = 5

        query = GetCoursesQuery(
            is_published=True,
            status=CourseStatus(status) if status else None,
            category_id=UUID(category_id) if category_id else None,
            skip=0,
            limit=page_size + 1,
        )
        all_courses = await self.get_courses_use_case.execute(query)

        has_next = len(all_courses) > page_size
        courses = all_courses[:page_size]

        if courses:
            text = f"{text}\n\n" + format_course_list(courses, page=1)
            keyboard = build_course_list_keyboard(courses, page=1, has_next=has_next)
        else:
            text = f"{text}\n\n❌ Курсы не найдены."
            keyboard = build_main_menu_keyboard()

        await callback.message.edit_text(
            text, reply_markup=keyboard, parse_mode="Markdown"
        )
        await callback.answer()

    async def _handle_filter_reset(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        """Handle filter reset."""
        await state.clear()
        await state.update_data(page=1)
        text = "✅ Все фильтры сброшены."

        page_size = 5
        query = GetCoursesQuery(is_published=True, skip=0, limit=page_size + 1)
        all_courses = await self.get_courses_use_case.execute(query)

        has_next = len(all_courses) > page_size
        courses = all_courses[:page_size]

        if courses:
            text = f"{text}\n\n" + format_course_list(courses, page=1)
            keyboard = build_course_list_keyboard(courses, page=1, has_next=has_next)
        else:
            text = f"{text}\n\n❌ Курсы не найдены."
            keyboard = build_main_menu_keyboard()

        await callback.message.edit_text(
            text, reply_markup=keyboard, parse_mode="Markdown"
        )
        await callback.answer()
