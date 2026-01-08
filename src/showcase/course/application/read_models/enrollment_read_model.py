from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class EnrollmentReadModel:
    enrollment_id: UUID
    course_id: UUID
    email: str
    full_name: str
    phone: str | None
    message: str | None
    user_id: UUID | None
    created_at: datetime
