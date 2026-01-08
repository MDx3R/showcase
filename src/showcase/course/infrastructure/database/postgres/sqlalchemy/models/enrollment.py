from __future__ import annotations

from datetime import datetime
from uuid import UUID

from common.infrastructure.database.postgres.sqlalchemy.models import Base
from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column


class EnrollmentBase(Base):
    __tablename__ = "enrollments"

    enrollment_id: Mapped[UUID] = mapped_column(PGUUID, primary_key=True)
    course_id: Mapped[UUID] = mapped_column(
        ForeignKey("courses.course_id"), nullable=False
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    user_id: Mapped[UUID | None] = mapped_column(PGUUID, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
