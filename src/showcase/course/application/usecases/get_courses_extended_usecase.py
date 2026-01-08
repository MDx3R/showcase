"""Use case implementation for extended courses filtering."""

from showcase.course.application.interfaces.repositories import ICourseReadRepository
from showcase.course.application.interfaces.repositories.course_read_repository import (
    CoursesFilter,
)
from showcase.course.application.interfaces.usecases.query.get_courses_extended_usecase import (
    IGetCoursesExtendedUseCase,
)
from showcase.course.application.read_models.course_read_model import CourseReadModel


class GetCoursesExtendedUseCase(IGetCoursesExtendedUseCase):
    def __init__(self, course_read_repository: ICourseReadRepository) -> None:
        self.course_read_repository = course_read_repository

    async def execute(self, query: CoursesFilter) -> list[CourseReadModel]:
        return await self.course_read_repository.filter_extended(query)
