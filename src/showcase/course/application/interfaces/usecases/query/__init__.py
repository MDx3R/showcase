"""Course use case interfaces."""

from .get_course_by_id_usecase import IGetCourseByIdUseCase
from .get_courses_search_usecase import IGetCoursesSearchUseCase
from .get_courses_usecase import IGetCoursesUseCase
from .get_skill_by_id_use_case import IGetSkillByIdUseCase
from .get_skills_use_case import IGetSkillsUseCase
from .get_tag_by_id_use_case import IGetTagByIdUseCase
from .get_tags_use_case import IGetTagsUseCase


__all__ = [
    "IGetCourseByIdUseCase",
    "IGetCoursesSearchUseCase",
    "IGetCoursesUseCase",
    "IGetSkillByIdUseCase",
    "IGetSkillsUseCase",
    "IGetTagByIdUseCase",
    "IGetTagsUseCase",
]
