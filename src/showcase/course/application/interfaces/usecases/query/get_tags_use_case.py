"""Use case interface for getting all tags."""

from abc import ABC, abstractmethod

from showcase.course.application.dtos.queries.get_tags_query import GetTagsQuery
from showcase.course.application.read_models.tag_read_model import TagReadModel


class IGetTagsUseCase(ABC):
    """Interface for getting all tags."""

    @abstractmethod
    async def execute(self, query: GetTagsQuery) -> list[TagReadModel]:
        """Execute the use case."""
        pass
