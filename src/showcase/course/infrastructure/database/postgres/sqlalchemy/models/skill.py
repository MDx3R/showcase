"""SQLAlchemy model for Skill."""

from __future__ import annotations

from uuid import UUID

from common.infrastructure.database.postgres.sqlalchemy.models import Base
from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column


class SkillBase(Base):
    """SQLAlchemy model for Skill."""

    __tablename__ = "skills"

    skill_id: Mapped[UUID] = mapped_column(PGUUID, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text)
