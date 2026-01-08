"""SQLAlchemy model for Lecturer."""

from uuid import UUID

from common.infrastructure.database.postgres.sqlalchemy.models import Base
from sqlalchemy import String, Text, text
from sqlalchemy.dialects.postgresql import ARRAY, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column


class LecturerBase(Base):
    """SQLAlchemy model for Lecturer."""

    __tablename__ = "lecturers"

    lecturer_id: Mapped[UUID] = mapped_column(PGUUID, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    position: Mapped[str | None] = mapped_column(String(255))
    bio: Mapped[str | None] = mapped_column(Text)
    photo_url: Mapped[str | None] = mapped_column(String(512))
    competencies: Mapped[list[str]] = mapped_column(
        ARRAY(String(255)), nullable=False, server_default=text("'{}'")
    )
