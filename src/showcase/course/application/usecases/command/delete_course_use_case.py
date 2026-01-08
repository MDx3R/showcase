from uuid import UUID

from showcase.course.application.interfaces.repositories.course_repository import (
    ICourseRepository,
)
from showcase.course.application.interfaces.usecases.command.delete_course_use_case import (
    IDeleteCourseUseCase,
)


class DeleteCourseUseCase(IDeleteCourseUseCase):
    def __init__(self, course_repository: ICourseRepository) -> None:
        self.course_repository = course_repository

    async def execute(self, course_id: UUID) -> UUID:
        await self.course_repository.delete(course_id)
        return course_id
