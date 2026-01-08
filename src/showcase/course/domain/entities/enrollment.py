from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Self
from uuid import UUID, uuid4

from common.domain.exceptions import InvariantViolationError
from common.domain.value_objects.datetime import DateTime
from common.domain.value_objects.email import Email
from common.domain.value_objects.phone_number import PhoneNumber


@dataclass
class Enrollment:
    enrollment_id: UUID
    course_id: UUID
    email: Email
    full_name: str
    phone: PhoneNumber | None
    message: str | None
    user_id: UUID | None
    created_at: DateTime

    @classmethod
    def create(
        cls,
        course_id: UUID,
        email: Email,
        full_name: str,
        phone: PhoneNumber | None = None,
        message: str | None = None,
        user_id: UUID | None = None,
    ) -> Self:
        if not full_name.strip():
            raise InvariantViolationError("Full name cannot be empty")

        return cls(
            enrollment_id=uuid4(),
            course_id=course_id,
            email=email,
            full_name=full_name,
            phone=phone,
            message=message,
            user_id=user_id,
            created_at=DateTime(datetime.now(UTC)),
        )
