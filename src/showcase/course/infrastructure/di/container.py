"""Course bounded context DI container."""

from typing import Any

from dependency_injector import containers, providers
from showcase.course.application.usecases import (
    CreateCourseUseCase,
    CreateSkillUseCase,
    CreateTagUseCase,
    DeleteCourseUseCase,
    DeleteSkillUseCase,
    DeleteTagUseCase,
    GetCourseByIdUseCase,
    GetCoursesSearchUseCase,
    GetCoursesUseCase,
    GetSkillByIdUseCase,
    GetSkillsUseCase,
    GetTagByIdUseCase,
    GetTagsUseCase,
    UpdateCourseUseCase,
    UpdateSkillUseCase,
    UpdateTagUseCase,
)
from showcase.course.application.usecases.command.enroll_user_use_case import (
    EnrollUserUseCase,
)
from showcase.course.application.usecases.get_courses_extended_usecase import (
    GetCoursesExtendedUseCase,
)
from showcase.course.application.usecases.query.list_enrollments_by_course_use_case import (
    ListEnrollmentsByCourseUseCase,
)
from showcase.course.application.usecases.query.list_enrollments_by_user_use_case import (
    ListEnrollmentsByUserUseCase,
)
from showcase.course.infrastructure.database.postgres.sqlalchemy.repositories import (
    CourseReadRepository,
    CourseRepository,
    SkillReadRepository,
    SkillRepository,
    TagReadRepository,
    TagRepository,
)
from showcase.course.infrastructure.database.postgres.sqlalchemy.repositories.enrollment_repository import (
    EnrollmentRepository,
)
from showcase.course.infrastructure.services.recommendation_service import (
    RecommendationService,
)


class CourseContainer(containers.DeclarativeContainer):
    """Dependency injection container for course bounded context."""

    # Explicit dependency declarations
    uuid_generator: providers.Dependency[Any] = providers.Dependency()
    query_executor: providers.Dependency[Any] = providers.Dependency()
    clock: providers.Dependency[Any] = providers.Dependency()

    # Read repositories
    course_read_repository = providers.Factory(CourseReadRepository, query_executor)
    skill_read_repository = providers.Factory(SkillReadRepository, query_executor)
    tag_read_repository = providers.Factory(TagReadRepository, query_executor)

    # Write repositories
    course_repository = providers.Factory(CourseRepository, query_executor)
    skill_repository = providers.Factory(SkillRepository, query_executor)
    tag_repository = providers.Factory(TagRepository, query_executor)
    enrollment_repository = providers.Factory(EnrollmentRepository, query_executor)

    # Read use cases
    get_courses_usecase = providers.Factory(GetCoursesUseCase, course_read_repository)
    get_course_by_id_usecase = providers.Factory(
        GetCourseByIdUseCase, course_read_repository
    )
    get_courses_search_usecase = providers.Factory(
        GetCoursesSearchUseCase, course_read_repository
    )
    filter_courses_usecase = providers.Factory(
        GetCoursesExtendedUseCase, course_read_repository
    )
    get_skills_usecase = providers.Factory(GetSkillsUseCase, skill_read_repository)
    get_skill_by_id_usecase = providers.Factory(
        GetSkillByIdUseCase, skill_read_repository
    )
    get_tags_usecase = providers.Factory(GetTagsUseCase, tag_read_repository)
    get_tag_by_id_usecase = providers.Factory(GetTagByIdUseCase, tag_read_repository)

    list_enrollments_use_case = providers.Factory(
        ListEnrollmentsByCourseUseCase, enrollment_repository
    )
    list_enrollments_by_user_use_case = providers.Factory(
        ListEnrollmentsByUserUseCase, enrollment_repository
    )

    # Write use cases
    create_course_usecase = providers.Factory(
        CreateCourseUseCase,
        course_repository=course_repository,
        uuid_generator=uuid_generator,
        tag_repository=tag_repository,
    )
    update_course_usecase = providers.Factory(
        UpdateCourseUseCase,
        course_repository=course_repository,
        uuid_generator=uuid_generator,
        tag_repository=tag_repository,
    )
    delete_course_usecase = providers.Factory(DeleteCourseUseCase, course_repository)
    create_skill_usecase = providers.Factory(
        CreateSkillUseCase,
        skill_repository=skill_repository,
        uuid_generator=uuid_generator,
    )
    update_skill_usecase = providers.Factory(UpdateSkillUseCase, skill_repository)
    delete_skill_usecase = providers.Factory(DeleteSkillUseCase, skill_repository)
    create_tag_usecase = providers.Factory(
        CreateTagUseCase,
        tag_repository=tag_repository,
        uuid_generator=uuid_generator,
    )
    update_tag_usecase = providers.Factory(UpdateTagUseCase, tag_repository)
    delete_tag_usecase = providers.Factory(DeleteTagUseCase, tag_repository)

    enroll_use_case = providers.Factory(EnrollUserUseCase, enrollment_repository)


class RecommendationContainer(containers.DeclarativeContainer):
    """Dependency injection container for course recommendations."""

    # Explicit dependency declarations
    logger: providers.Dependency[Any] = providers.Dependency()
    llm: providers.Dependency[Any] = providers.Dependency()
    course_read_repository: providers.Dependency[Any] = providers.Dependency()
    category_read_repository: providers.Dependency[Any] = providers.Dependency()

    # Services
    recommendation_service = providers.Factory(
        RecommendationService,
        logger=logger,
        llm=llm,
        course_repository=course_read_repository,
        category_repository=category_read_repository,
    )
