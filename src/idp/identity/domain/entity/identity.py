from dataclasses import dataclass
from enum import Enum
from typing import Self
from uuid import UUID

from idp.identity.domain.value_objects.password import Password
from idp.identity.domain.value_objects.username import Username


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"


@dataclass
class Identity:
    identity_id: UUID
    role: Role
    username: Username
    password: Password

    @classmethod
    def create(cls, identity_id: UUID, username: str, password: str) -> Self:
        return cls(
            identity_id=identity_id,
            role=Role.USER,
            username=Username(username),
            password=Password(password),
        )
