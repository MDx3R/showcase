"""SQLAlchemy model for Tag."""

from __future__ import annotations

from uuid import UUID

from common.infrastructure.database.postgres.sqlalchemy.models import Base
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column


class TagBase(Base):
    """SQLAlchemy model for Tag."""

    __tablename__ = "tags"

    tag_id: Mapped[UUID] = mapped_column(PGUUID, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
