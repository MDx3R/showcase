"""Service for handling course list display and pagination."""

from typing import Optional
from uuid import UUID

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from showcase.course.application.dtos.queries import GetCoursesQuery
from showcase.course.application.interfaces.usecases.query import IGetCoursesUseCase
from showcase.course.domain.value_objects import CourseStatus, Format
from showcase.course.presentation.telegram.formatters.course import format_course_list
from showcase.course.presentation.telegram.keyboards.builder import (
    build_course_list_keyboard,
    build_main_menu_keyboard,
)

PAGE_SIZE = 5  # Constant for pagination


class CourseListService:
    """Service for fetching and displaying paginated course lists."""

    def __init__(self, get_courses_use_case: IGetCoursesUseCase) -> None:
        self.get_courses_use_case = get_courses_use_case

    async def display_course_list(
        self,
        callback_or_message: CallbackQuery | Message,
        state: FSMContext,
        page: int = 1,
        extra_text: str = "",
        reset_filters: bool = False,
    ) -> None:
        """Fetch and display courses based on current filters and page."""
        if reset_filters:
            await state.clear()

        data = await state.get_data()
        status = data.get("status")
        category_id = data.get("category_id")
        format_value = data.get("format")  # Now used

        skip = (page - 1) * PAGE_SIZE
        query = GetCoursesQuery(
            is_published=True,
            status=CourseStatus(status) if status else None,
            category_id=UUID(category_id) if category_id else None,
            format=(
                Format(format_value) if format_value else None
            ),  # Added format filter
            skip=skip,
            limit=PAGE_SIZE + 1,
        )

        try:
            all_courses = await self.get_courses_use_case.execute(query)
        except Exception as e:
            # Log error (placeholder; integrate actual logger)
            print(f"Error fetching courses: {e}")
            text = "❌ Произошла ошибка при загрузке курсов."
            keyboard = build_main_menu_keyboard()
            await self._send_response(callback_or_message, text, keyboard)
            return

        has_next = len(all_courses) > PAGE_SIZE
        courses = all_courses[:PAGE_SIZE]

        await state.update_data(page=page)

        if not courses:
            text = (
                f"{extra_text}\n\n❌ Курсы не найдены."
                if extra_text
                else "❌ Курсы не найдены."
            )
            keyboard = build_main_menu_keyboard()
        else:
            # Format only the current page courses for display
            text = (
                f"{extra_text}\n\n" + format_course_list(courses, page=page)
                if extra_text
                else format_course_list(courses, page=page)
            )
            # Pass actual page number; keyboard builder handles already-sliced lists
            keyboard = build_course_list_keyboard(
                courses, page=page, page_size=PAGE_SIZE, has_next=has_next
            )

        await self._send_response(callback_or_message, text, keyboard)

    async def _send_response(
        self,
        callback_or_message: CallbackQuery | Message,
        text: str,
        keyboard,
    ) -> None:
        """Send or edit message based on input type."""
        if isinstance(callback_or_message, CallbackQuery):
            await callback_or_message.message.edit_text(text, reply_markup=keyboard)
            await callback_or_message.answer()
        else:
            await callback_or_message.answer(text, reply_markup=keyboard)
