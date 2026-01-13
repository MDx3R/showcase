from abc import ABC, abstractmethod
from uuid import UUID

from idp.identity.domain.entity.identity import Identity


class IIdentityRepository(ABC):
    @abstractmethod
    async def get_by_id(self, identity_id: UUID) -> Identity: ...
    @abstractmethod
    async def exists_by_email(self, email: str) -> bool: ...
    @abstractmethod
    async def get_by_email(self, email: str) -> Identity: ...
    @abstractmethod
    async def add(self, entity: Identity) -> None: ...
