from uuid import UUID

from showcase.course.application.interfaces.repositories.tag_repository import (
    ITagRepository,
)
from showcase.course.application.interfaces.usecases.command.delete_tag_use_case import (
    IDeleteTagUseCase,
)


class DeleteTagUseCase(IDeleteTagUseCase):
    def __init__(self, tag_repository: ITagRepository) -> None:
        self.tag_repository = tag_repository

    async def execute(self, tag_id: UUID) -> UUID:
        await self.tag_repository.delete(tag_id)
        return tag_id
