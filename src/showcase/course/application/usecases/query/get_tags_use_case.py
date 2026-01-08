"""Use case for getting all tags."""

from showcase.course.application.dtos.queries.get_tags_query import GetTagsQuery
from showcase.course.application.interfaces.repositories.tag_read_repository import (
    ITagReadRepository,
)
from showcase.course.application.interfaces.usecases.query.get_tags_use_case import (
    IGetTagsUseCase,
)
from showcase.course.application.read_models.tag_read_model import TagReadModel


class GetTagsUseCase(IGetTagsUseCase):
    """Implementation of getting all tags."""

    def __init__(self, tag_repository: ITagReadRepository) -> None:
        self.tag_repository = tag_repository

    async def execute(self, query: GetTagsQuery) -> list[TagReadModel]:
        """Execute the use case."""
        return await self.tag_repository.get_all(skip=query.skip, limit=query.limit)
