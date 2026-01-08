"""Use case: search courses by full-text query."""

from showcase.course.application.dtos.queries.get_courses_search_query import (
    GetCoursesSearchQuery,
)
from showcase.course.application.interfaces.repositories.course_read_repository import (
    ICourseReadRepository,
)
from showcase.course.application.interfaces.usecases.query.get_courses_search_usecase import (
    IGetCoursesSearchUseCase,
)
from showcase.course.application.read_models.course_read_model import CourseReadModel


class GetCoursesSearchUseCase(IGetCoursesSearchUseCase):
    def __init__(self, repository: ICourseReadRepository) -> None:
        self._repo = repository

    async def execute(self, query: GetCoursesSearchQuery) -> list[CourseReadModel]:
        return await self._repo.search(query.query, skip=query.skip, limit=query.limit)
