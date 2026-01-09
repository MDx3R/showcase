from collections.abc import Sequence
from uuid import UUID

from showcase.course.application.interfaces.repositories.enrollment_repository import (
    IEnrollmentRepository,
)
from showcase.course.application.interfaces.usecases.query.list_enrollments_by_user_use_case import (
    IListEnrollmentsByUserUseCase,
)
from showcase.course.application.read_models.enrollment_read_model import (
    EnrollmentReadModel,
)


class ListEnrollmentsByUserUseCase(IListEnrollmentsByUserUseCase):
    def __init__(self, enrollment_repository: IEnrollmentRepository) -> None:
        self.enrollment_repository = enrollment_repository

    async def execute(
        self, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> Sequence[EnrollmentReadModel]:
        return await self.enrollment_repository.list_by_user(
            user_id, skip=skip, limit=limit
        )
