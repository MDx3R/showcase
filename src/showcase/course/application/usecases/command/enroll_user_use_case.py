from uuid import UUID

from common.domain.value_objects.email import Email
from common.domain.value_objects.phone_number import PhoneNumber
from showcase.course.application.dtos.commands.enroll_user_command import (
    EnrollUserCommand,
)
from showcase.course.application.interfaces.repositories.enrollment_repository import (
    IEnrollmentRepository,
)
from showcase.course.application.interfaces.usecases.command.enroll_user_use_case import (
    IEnrollUserUseCase,
)
from showcase.course.domain.entities.enrollment import Enrollment


class EnrollUserUseCase(IEnrollUserUseCase):
    def __init__(self, enrollment_repository: IEnrollmentRepository) -> None:
        self.enrollment_repository = enrollment_repository

    async def execute(self, command: EnrollUserCommand) -> UUID:
        email = Email(command.email)
        phone = PhoneNumber(command.phone) if command.phone else None

        enrollment = Enrollment.create(
            course_id=command.course_id,
            email=email,
            full_name=command.full_name,
            phone=phone,
            message=command.message,
            user_id=command.user_id,
        )

        await self.enrollment_repository.add(enrollment)
        return enrollment.enrollment_id
