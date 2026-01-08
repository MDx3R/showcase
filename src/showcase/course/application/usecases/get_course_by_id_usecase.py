"""Get course by ID use case implementation."""

from showcase.course.application.dtos.queries import GetCourseByIdQuery
from showcase.course.application.interfaces.repositories import ICourseReadRepository
from showcase.course.application.interfaces.usecases.query import IGetCourseByIdUseCase
from showcase.course.application.read_models.course_read_model import CourseReadModel


class GetCourseByIdUseCase(IGetCourseByIdUseCase):
    """Use case for getting a course by ID."""

    def __init__(self, course_read_repository: ICourseReadRepository) -> None:
        self.course_read_repository = course_read_repository

    async def execute(self, query: GetCourseByIdQuery) -> CourseReadModel:
        """Execute the get course by ID query."""
        return await self.course_read_repository.get_by_id(query.course_id)
