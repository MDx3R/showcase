"""Use case for getting tag by ID."""

from showcase.course.application.dtos.queries.get_tag_by_id_query import GetTagByIdQuery
from showcase.course.application.interfaces.repositories.tag_read_repository import (
    ITagReadRepository,
)
from showcase.course.application.interfaces.usecases.query.get_tag_by_id_use_case import (
    IGetTagByIdUseCase,
)
from showcase.course.application.read_models.tag_read_model import TagReadModel


class GetTagByIdUseCase(IGetTagByIdUseCase):
    """Implementation of getting tag by ID."""

    def __init__(self, tag_repository: ITagReadRepository) -> None:
        self.tag_repository = tag_repository

    async def execute(self, query: GetTagByIdQuery) -> TagReadModel:
        """Execute the use case."""
        return await self.tag_repository.get_by_id(query.tag_id)
