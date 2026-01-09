from uuid import UUID

from idp.identity.domain.entity.identity import Role
from pydantic import BaseModel


class IdentityResponse(BaseModel):
    id: UUID
    email: str
    username: str
    role: Role
