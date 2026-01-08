"""Course use cases."""

from showcase.course.application.usecases.command.create_course_use_case import (
    CreateCourseUseCase,
)
from showcase.course.application.usecases.command.create_skill_use_case import (
    CreateSkillUseCase,
)
from showcase.course.application.usecases.command.create_tag_use_case import (
    CreateTagUseCase,
)
from showcase.course.application.usecases.command.delete_course_use_case import (
    DeleteCourseUseCase,
)
from showcase.course.application.usecases.command.delete_skill_use_case import (
    DeleteSkillUseCase,
)
from showcase.course.application.usecases.command.delete_tag_use_case import (
    DeleteTagUseCase,
)
from showcase.course.application.usecases.command.update_course_use_case import (
    UpdateCourseUseCase,
)
from showcase.course.application.usecases.command.update_skill_use_case import (
    UpdateSkillUseCase,
)
from showcase.course.application.usecases.command.update_tag_use_case import (
    UpdateTagUseCase,
)
from showcase.course.application.usecases.get_course_by_id_usecase import (
    GetCourseByIdUseCase,
)
from showcase.course.application.usecases.get_courses_search_usecase import (
    GetCoursesSearchUseCase,
)
from showcase.course.application.usecases.get_courses_usecase import GetCoursesUseCase
from showcase.course.application.usecases.query.get_skill_by_id_use_case import (
    GetSkillByIdUseCase,
)
from showcase.course.application.usecases.query.get_skills_use_case import (
    GetSkillsUseCase,
)
from showcase.course.application.usecases.query.get_tag_by_id_use_case import (
    GetTagByIdUseCase,
)
from showcase.course.application.usecases.query.get_tags_use_case import (
    GetTagsUseCase,
)


__all__ = [
    "CreateCourseUseCase",
    "CreateSkillUseCase",
    "CreateTagUseCase",
    "DeleteCourseUseCase",
    "DeleteSkillUseCase",
    "DeleteTagUseCase",
    "GetCourseByIdUseCase",
    "GetCoursesSearchUseCase",
    "GetCoursesUseCase",
    "GetSkillByIdUseCase",
    "GetSkillsUseCase",
    "GetTagByIdUseCase",
    "GetTagsUseCase",
    "UpdateCourseUseCase",
    "UpdateSkillUseCase",
    "UpdateTagUseCase",
]
