from dataclasses import dataclass
from uuid import UUID

from idp.identity.domain.entity.identity import Role


@dataclass(frozen=True)
class IdentityDescriptor:
    identity_id: UUID
    username: str
    role: Role
