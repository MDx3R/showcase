"""Use case interface for getting tag by ID."""

from abc import ABC, abstractmethod

from showcase.course.application.dtos.queries.get_tag_by_id_query import GetTagByIdQuery
from showcase.course.application.read_models.tag_read_model import TagReadModel


class IGetTagByIdUseCase(ABC):
    """Interface for getting tag by ID."""

    @abstractmethod
    async def execute(self, query: GetTagByIdQuery) -> TagReadModel:
        """Execute the use case."""
        pass
