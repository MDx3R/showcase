from abc import ABC, abstractmethod
from collections.abc import Sequence
from uuid import UUID

from showcase.course.application.read_models.enrollment_read_model import (
    EnrollmentReadModel,
)
from showcase.course.domain.entities.enrollment import Enrollment


class IEnrollmentRepository(ABC):
    @abstractmethod
    async def add(self, enrollment: Enrollment) -> None:
        pass

    @abstractmethod
    async def list_by_course(
        self, course_id: UUID, skip: int = 0, limit: int = 100
    ) -> Sequence[EnrollmentReadModel]:
        pass

    @abstractmethod
    async def list_by_user(
        self, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> Sequence[EnrollmentReadModel]:
        pass
