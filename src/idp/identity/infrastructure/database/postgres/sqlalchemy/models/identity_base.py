from uuid import UUID

from common.infrastructure.database.postgres.sqlalchemy.models import Base
from idp.identity.domain.entity.identity import Role
from sqlalchemy import Enum, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column


class IdentityBase(Base):
    __tablename__ = "identities"

    identity_id: Mapped[UUID] = mapped_column(PGUUID, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
