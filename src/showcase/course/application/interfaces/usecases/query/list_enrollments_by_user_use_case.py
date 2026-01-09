from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from uuid import UUID

from showcase.course.application.read_models.enrollment_read_model import (
    EnrollmentReadModel,
)


class IListEnrollmentsByUserUseCase(ABC):
    @abstractmethod
    async def execute(
        self, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> Sequence[EnrollmentReadModel]:
        pass
