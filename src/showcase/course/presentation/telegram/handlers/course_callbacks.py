"""Course detail and enrollment callback handlers."""

from uuid import UUID

from aiogram import F, Router
from aiogram.types import CallbackQuery
from showcase.course.application.dtos.queries import GetCourseByIdQuery
from showcase.course.application.interfaces.usecases.query.get_course_by_id_usecase import (
    IGetCourseByIdUseCase,
)
from showcase.course.presentation.telegram.formatters.course import format_course_detail
from showcase.course.presentation.telegram.keyboards.builder import (
    build_course_detail_keyboard,
)


class CourseCallbackHandler:
    """Handler for course-related callbacks."""

    def __init__(self, get_course_by_id_use_case: IGetCourseByIdUseCase) -> None:
        self.get_course_by_id_use_case = get_course_by_id_use_case
        self.router = Router()

        self._register_handlers()

    def _register_handlers(self) -> None:
        self.router.callback_query.register(
            self._handle_course_detail, F.data.startswith("course_")
        )
        self.router.callback_query.register(
            self._handle_enroll, F.data.startswith("enroll_")
        )

    async def _handle_course_detail(self, callback: CallbackQuery) -> None:
        course_id_str = (callback.data or "").split("_", 1)[1]
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
        if len(text) > 4096:
            text = text[:4090] + "...\n\n(Текст обрезан)"

        keyboard = build_course_detail_keyboard(course_id)
        if callback.message:
            await callback.message.edit_text(  # pyright: ignore[reportAttributeAccessIssue]
                text, reply_markup=keyboard
            )
        await callback.answer()

    async def _handle_enroll(self, callback: CallbackQuery) -> None:
        course_id_str = (callback.data or "").split("_", 1)[1]
        text = (
            f"📝 Запись на курс\n\n"
            f"Для записи на курс свяжитесь с администрацией.\n"
            f"ID курса: {course_id_str}\n"
            f"Или используйте нашу веб-версию (/help)!"
        )
        await callback.answer(text, show_alert=True)
