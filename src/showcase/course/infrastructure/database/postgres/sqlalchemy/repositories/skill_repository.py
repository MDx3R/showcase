"""Skill write repository implementation."""

from uuid import UUID

from common.infrastructure.database.postgres.sqlalchemy.executor import QueryExecutor
from showcase.course.application.interfaces.repositories.skill_repository import (
    ISkillRepository,
)
from showcase.course.domain.entities.skill import Skill
from showcase.course.infrastructure.database.postgres.sqlalchemy.models.skill import (
    SkillBase,
)
from sqlalchemy import delete, select


class SkillRepository(ISkillRepository):
    """Write repository for skills."""

    def __init__(self, executor: QueryExecutor) -> None:
        self.executor = executor

    async def get_by_id(self, skill_id: UUID) -> Skill:
        """Get a skill by ID."""
        stmt = select(SkillBase).where(SkillBase.skill_id == skill_id)
        model = await self.executor.execute_scalar_one(stmt)
        if not model:
            raise ValueError(f"Skill with id {skill_id} not found")
        return self._to_domain(model)

    async def add(self, skill: Skill) -> None:
        """Add a new skill."""
        model = self._to_persistence(skill)
        await self.executor.add(model)

    async def update(self, skill: Skill) -> None:
        """Update an existing skill."""
        model = self._to_persistence(skill)
        await self.executor.save(model)

    async def delete(self, skill_id: UUID) -> None:
        """Delete a skill by ID."""
        await self.executor.execute(
            delete(SkillBase).where(SkillBase.skill_id == skill_id)
        )

    @staticmethod
    def _to_domain(model: SkillBase) -> Skill:
        """Map ORM model to domain entity."""
        return Skill(
            skill_id=model.skill_id,
            name=model.name,
            description=model.description,
        )

    @staticmethod
    def _to_persistence(entity: Skill) -> SkillBase:
        """Map domain entity to ORM model."""
        return SkillBase(
            skill_id=entity.skill_id,
            name=entity.name,
            description=entity.description,
        )
