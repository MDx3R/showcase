"""Tag read repository implementation."""

from uuid import UUID

from common.infrastructure.database.postgres.sqlalchemy.executor import QueryExecutor
from showcase.course.application.interfaces.repositories.tag_read_repository import (
    ITagReadRepository,
)
from showcase.course.application.read_models.tag_read_model import TagReadModel
from showcase.course.infrastructure.database.postgres.sqlalchemy.mappers.tag_mapper import (
    TagMapper,
)
from showcase.course.infrastructure.database.postgres.sqlalchemy.models.tag import (
    TagBase,
)
from sqlalchemy import select


class TagReadRepository(ITagReadRepository):
    """Read repository for tags."""

    def __init__(self, executor: QueryExecutor) -> None:
        self.executor = executor

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[TagReadModel]:
        """Get all tags."""
        stmt = select(TagBase).offset(skip).limit(limit)
        models = await self.executor.execute_scalar_many(stmt)
        return [TagMapper.to_read_model(model) for model in models]

    async def get_by_id(self, tag_id: UUID) -> TagReadModel:
        """Get a tag by ID."""
        stmt = select(TagBase).where(TagBase.tag_id == tag_id)
        model = await self.executor.execute_scalar_one(stmt)
        if not model:
            raise ValueError(f"Tag with id {tag_id} not found")
        return TagMapper.to_read_model(model)
