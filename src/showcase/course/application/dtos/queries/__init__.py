"""Course query DTOs."""

from showcase.course.application.dtos.queries.get_course_by_id_query import (
    GetCourseByIdQuery,
)
from showcase.course.application.dtos.queries.get_courses_query import GetCoursesQuery
from showcase.course.application.dtos.queries.get_courses_search_query import (
    GetCoursesSearchQuery,
)
from showcase.course.application.dtos.queries.get_skill_by_id_query import (
    GetSkillByIdQuery,
)
from showcase.course.application.dtos.queries.get_skills_query import GetSkillsQuery
from showcase.course.application.dtos.queries.get_tag_by_id_query import GetTagByIdQuery
from showcase.course.application.dtos.queries.get_tags_query import GetTagsQuery


__all__ = [
    "GetCourseByIdQuery",
    "GetCoursesQuery",
    "GetCoursesSearchQuery",
    "GetSkillByIdQuery",
    "GetSkillsQuery",
    "GetTagByIdQuery",
    "GetTagsQuery",
]
