import re
from dataclasses import dataclass

from common.domain.exceptions import InvariantViolationError


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise InvariantViolationError("Email cannot be empty")

        if not self._is_valid_email(self.value):
            raise InvariantViolationError("Invalid email format")

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
