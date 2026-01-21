"""Course detail and enrollment callback handlers."""

from uuid import UUID

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from common.infrastructure.config.deployment_meta import DeploymentMeta
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

    def __init__(
        self,
        deploy_meta: DeploymentMeta,
        get_course_by_id_use_case: IGetCourseByIdUseCase,
    ) -> None:
        self.deploy_meta = deploy_meta
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

    async def _handle_course_detail(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
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

        data = await state.get_data()
        back_to_list = data.get("back_to_list", True)

        keyboard = build_course_detail_keyboard(course_id, back_to_list=back_to_list)
        if callback.message:
            await callback.message.answer(  # pyright: ignore[reportAttributeAccessIssue]
                text, reply_markup=keyboard
            )
        await callback.answer()

    async def _handle_enroll(self, callback: CallbackQuery) -> None:
        course_id_str = (callback.data or "").split("_", 1)[1]

        text = (
            "📝 <b>Запись на курс</b>\n\n"
            "Чтобы записаться на курс, свяжитесь с администрацией платформы.\n\n"
            f"🔑 <b>ID курса:</b> <code>{course_id_str}</code>\n\n"
            f"🌐 Или воспользуйтесь нашей "
            f'<a href="{self.deploy_meta.external_url.rstrip("/")}/courses/{course_id_str}">'
            f"веб-версией</a> для записи онлайн."
        )

        if callback.message:
            await callback.message.answer(text, disable_web_page_preview=True)

        await callback.answer()
