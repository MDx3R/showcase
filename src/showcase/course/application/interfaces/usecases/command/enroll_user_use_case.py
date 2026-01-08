from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from showcase.course.application.dtos.commands.enroll_user_command import (
    EnrollUserCommand,
)


class IEnrollUserUseCase(ABC):
    @abstractmethod
    async def execute(self, command: EnrollUserCommand) -> UUID:
        pass
