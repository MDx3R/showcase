from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class EnrollUserCommand:
    course_id: UUID
    email: str
    full_name: str
    phone: str | None = None
    message: str | None = None
    user_id: UUID | None = None
