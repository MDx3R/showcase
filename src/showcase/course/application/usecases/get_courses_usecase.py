"""Course use case implementations."""

from showcase.course.application.dtos.queries import GetCoursesQuery
from showcase.course.application.interfaces.repositories import ICourseReadRepository
from showcase.course.application.interfaces.usecases.query import IGetCoursesUseCase
from showcase.course.application.read_models.course_read_model import CourseReadModel


class GetCoursesUseCase(IGetCoursesUseCase):
    """Use case for getting courses."""

    def __init__(self, course_read_repository: ICourseReadRepository) -> None:
        self.course_read_repository = course_read_repository

    async def execute(self, query: GetCoursesQuery) -> list[CourseReadModel]:
        """Execute the get courses query."""
        return await self.course_read_repository.get_all(
            status=query.status,
            is_published=query.is_published,
            category_id=query.category_id,
            skip=query.skip,
            limit=query.limit,
        )
