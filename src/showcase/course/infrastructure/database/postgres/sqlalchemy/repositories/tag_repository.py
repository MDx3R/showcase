"""Tag write repository implementation."""

from collections.abc import Iterable, Sequence
from uuid import UUID

from common.infrastructure.database.postgres.sqlalchemy.executor import QueryExecutor
from showcase.course.application.interfaces.repositories.tag_repository import (
    ITagRepository,
)
from showcase.course.domain.entities.tag import Tag
from showcase.course.infrastructure.database.postgres.sqlalchemy.models.tag import (
    TagBase,
)
from sqlalchemy import delete, select


class TagRepository(ITagRepository):
    """Write repository for tags."""

    def __init__(self, executor: QueryExecutor) -> None:
        self.executor = executor

    async def get_by_id(self, tag_id: UUID) -> Tag:
        """Get a tag by ID."""
        stmt = select(TagBase).where(TagBase.tag_id == tag_id)
        model = await self.executor.execute_scalar_one(stmt)
        if not model:
            raise ValueError(f"Tag with id {tag_id} not found")
        return self._to_domain(model)

    async def add(self, tag: Tag) -> None:
        """Add a new tag."""
        model = self._to_persistence(tag)
        await self.executor.add(model)

    async def add_all(self, tags: Iterable[Tag]) -> None:
        """Add new tags."""
        if not tags:
            return

        models = [self._to_persistence(t) for t in tags]
        await self.executor.add_all(models)

    async def update(self, tag: Tag) -> None:
        """Update an existing tag."""
        model = self._to_persistence(tag)
        await self.executor.save(model)

    async def delete(self, tag_id: UUID) -> None:
        """Delete a tag by ID."""
        await self.executor.execute(delete(TagBase).where(TagBase.tag_id == tag_id))

    async def get_by_values(self, tags: Iterable[str]) -> Sequence[Tag]:
        """Get existing tags by their values."""
        if not tags:
            return []

        stmt = select(TagBase).where(TagBase.name.in_(tags))
        models = await self.executor.execute_scalar_many(stmt)
        return [self._to_domain(m) for m in models]

    @staticmethod
    def _to_domain(model: TagBase) -> Tag:
        """Map ORM model to domain entity."""
        return Tag(tag_id=model.tag_id, value=model.name)

    @staticmethod
    def _to_persistence(entity: Tag) -> TagBase:
        """Map domain entity to ORM model."""
        return TagBase(tag_id=entity.tag_id, name=entity.value)
