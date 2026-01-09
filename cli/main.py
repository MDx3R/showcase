"""Application entry point."""

from collections.abc import AsyncGenerator
from typing import Any

from bootstrap.config import AppConfig
from bootstrap.utils import log_config
from common.infrastructure.database.postgres.sqlalchemy.database import Database
from common.infrastructure.di.container.common import CommonContainer
from common.infrastructure.logger.logging.logger_factory import LoggerFactory
from common.infrastructure.services.llama_index.client import MappedOpenAI
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from idp.auth.application.interfaces.usecases.command.login_use_case import (
    ILoginUseCase,
)
from idp.auth.application.interfaces.usecases.command.logout_use_case import (
    ILogoutUseCase,
)
from idp.auth.application.interfaces.usecases.command.refresh_token_use_case import (
    IRefreshTokenUseCase,
)
from idp.auth.infrastructure.di.container.container import AuthContainer, TokenContainer
from idp.auth.presentation.http.fastapi.controllers import auth_router
from idp.identity.application.interfaces.services.token_intospector import (
    ITokenIntrospector,
)
from idp.identity.application.interfaces.usecases.command.create_identity_use_case import (
    ICreateIdentityUseCase,
)
from idp.identity.infrastructure.di.container.container import IdentityContainer
from idp.identity.presentation.http.fastapi.controllers import identity_router
from showcase.category.application.interfaces.usecases.command.create_category_use_case import (
    ICreateCategoryUseCase,
)
from showcase.category.application.interfaces.usecases.command.delete_category_use_case import (
    IDeleteCategoryUseCase,
)
from showcase.category.application.interfaces.usecases.command.update_category_use_case import (
    IUpdateCategoryUseCase,
)
from showcase.category.application.interfaces.usecases.query.get_categories_usecase import (
    IGetCategoriesUseCase,
)
from showcase.category.application.interfaces.usecases.query.get_category_by_id_usecase import (
    IGetCategoryByIdUseCase,
)
from showcase.category.infrastructure.di.container import CategoryContainer
from showcase.category.presentation.http.fastapi.controllers import category_router
from showcase.course.application.interfaces.services.recommendation_service import (
    IRecommendationService,
)
from showcase.course.application.interfaces.usecases.command.create_course_use_case import (
    ICreateCourseUseCase,
)
from showcase.course.application.interfaces.usecases.command.create_skill_use_case import (
    ICreateSkillUseCase,
)
from showcase.course.application.interfaces.usecases.command.create_tag_use_case import (
    ICreateTagUseCase,
)
from showcase.course.application.interfaces.usecases.command.delete_course_use_case import (
    IDeleteCourseUseCase,
)
from showcase.course.application.interfaces.usecases.command.delete_skill_use_case import (
    IDeleteSkillUseCase,
)
from showcase.course.application.interfaces.usecases.command.delete_tag_use_case import (
    IDeleteTagUseCase,
)
from showcase.course.application.interfaces.usecases.command.enroll_user_use_case import (
    IEnrollUserUseCase,
)
from showcase.course.application.interfaces.usecases.command.update_course_use_case import (
    IUpdateCourseUseCase,
)
from showcase.course.application.interfaces.usecases.command.update_skill_use_case import (
    IUpdateSkillUseCase,
)
from showcase.course.application.interfaces.usecases.command.update_tag_use_case import (
    IUpdateTagUseCase,
)
from showcase.course.application.interfaces.usecases.query import (
    IGetCourseByIdUseCase,
    IGetCoursesSearchUseCase,
    IGetCoursesUseCase,
    IGetSkillByIdUseCase,
    IGetSkillsUseCase,
    IGetTagByIdUseCase,
    IGetTagsUseCase,
)

# Controllers (read-side)
from showcase.course.application.interfaces.usecases.query.get_courses_extended_usecase import (
    IGetCoursesExtendedUseCase,
)
from showcase.course.application.interfaces.usecases.query.list_enrollments_by_course_use_case import (
    IListEnrollmentsByCourseUseCase,
)
from showcase.course.application.interfaces.usecases.query.list_enrollments_by_user_use_case import (
    IListEnrollmentsByUserUseCase,
)
from showcase.course.infrastructure.di.container import (
    CourseContainer,
    RecommendationContainer,
)
from showcase.course.presentation.http.fastapi.controllers import (
    course_router,
    recommendations_router,
    skills_router,
    tags_router,
)
from showcase.lecturer.application.interfaces.usecases.command.create_lecturer_use_case import (
    ICreateLecturerUseCase,
)
from showcase.lecturer.application.interfaces.usecases.command.delete_lecturer_use_case import (
    IDeleteLecturerUseCase,
)
from showcase.lecturer.application.interfaces.usecases.command.update_lecturer_use_case import (
    IUpdateLecturerUseCase,
)
from showcase.lecturer.application.interfaces.usecases.query import (
    IGetLecturerByIdUseCase,
    IGetLecturersUseCase,
)
from showcase.lecturer.infrastructure.di.container import LecturerContainer
from showcase.lecturer.presentation.http.fastapi.controllers import lecturer_router


def init_course(app: FastAPI, container: CourseContainer) -> None:
    app.include_router(course_router, prefix="/api", tags=["courses"])
    app.include_router(skills_router, prefix="/api", tags=["skills"])
    app.include_router(tags_router, prefix="/api", tags=["tags"])

    app.dependency_overrides[IGetCoursesUseCase] = (
        lambda: container.get_courses_usecase()
    )
    app.dependency_overrides[IGetCoursesExtendedUseCase] = (
        lambda: container.filter_courses_usecase()
    )
    app.dependency_overrides[IGetCourseByIdUseCase] = (
        lambda: container.get_course_by_id_usecase()
    )
    app.dependency_overrides[IGetCoursesSearchUseCase] = (
        lambda: container.get_courses_search_usecase()
    )
    app.dependency_overrides[ICreateCourseUseCase] = (
        lambda: container.create_course_usecase()
    )
    app.dependency_overrides[IUpdateCourseUseCase] = (
        lambda: container.update_course_usecase()
    )
    app.dependency_overrides[IGetSkillsUseCase] = lambda: container.get_skills_usecase()
    app.dependency_overrides[IGetSkillByIdUseCase] = (
        lambda: container.get_skill_by_id_usecase()
    )
    app.dependency_overrides[ICreateSkillUseCase] = (
        lambda: container.create_skill_usecase()
    )
    app.dependency_overrides[IUpdateSkillUseCase] = (
        lambda: container.update_skill_usecase()
    )
    app.dependency_overrides[IGetTagsUseCase] = lambda: container.get_tags_usecase()
    app.dependency_overrides[IGetTagByIdUseCase] = (
        lambda: container.get_tag_by_id_usecase()
    )
    app.dependency_overrides[ICreateTagUseCase] = lambda: container.create_tag_usecase()
    app.dependency_overrides[IUpdateTagUseCase] = lambda: container.update_tag_usecase()

    # Delete use cases
    app.dependency_overrides[IDeleteCourseUseCase] = (
        lambda: container.delete_course_usecase()
    )
    app.dependency_overrides[IDeleteSkillUseCase] = (
        lambda: container.delete_skill_usecase()
    )
    app.dependency_overrides[IDeleteTagUseCase] = lambda: container.delete_tag_usecase()

    app.dependency_overrides[IEnrollUserUseCase] = lambda: container.enroll_use_case()
    app.dependency_overrides[IListEnrollmentsByCourseUseCase] = (
        lambda: container.list_enrollments_use_case()
    )
    app.dependency_overrides[IListEnrollmentsByUserUseCase] = (
        lambda: container.list_enrollments_by_user_use_case()
    )


def init_lecturer(app: FastAPI, container: LecturerContainer) -> None:
    app.include_router(lecturer_router, prefix="/api", tags=["lecturers"])

    app.dependency_overrides[IGetLecturersUseCase] = (
        lambda: container.get_lecturers_usecase()
    )
    app.dependency_overrides[IGetLecturerByIdUseCase] = (
        lambda: container.get_lecturer_by_id_usecase()
    )
    app.dependency_overrides[ICreateLecturerUseCase] = (
        lambda: container.create_lecturer_usecase()
    )
    app.dependency_overrides[IUpdateLecturerUseCase] = (
        lambda: container.update_lecturer_usecase()
    )
    app.dependency_overrides[IDeleteLecturerUseCase] = (
        lambda: container.delete_lecturer_usecase()
    )


def init_category(app: FastAPI, container: CategoryContainer) -> None:
    app.include_router(category_router, prefix="/api", tags=["categories"])

    app.dependency_overrides[IGetCategoriesUseCase] = (
        lambda: container.get_categories_usecase()
    )
    app.dependency_overrides[IGetCategoryByIdUseCase] = (
        lambda: container.get_category_by_id_usecase()
    )
    app.dependency_overrides[ICreateCategoryUseCase] = (
        lambda: container.create_category_usecase()
    )
    app.dependency_overrides[IUpdateCategoryUseCase] = (
        lambda: container.update_category_usecase()
    )
    app.dependency_overrides[IDeleteCategoryUseCase] = (
        lambda: container.delete_category_usecase()
    )


def init_auth(app: FastAPI, container: AuthContainer) -> None:
    app.include_router(auth_router, prefix="/auth", tags=["auth"])

    app.dependency_overrides[ILoginUseCase] = lambda: container.login_use_case()
    app.dependency_overrides[ILogoutUseCase] = lambda: container.logout_use_case()
    app.dependency_overrides[IRefreshTokenUseCase] = (
        lambda: container.refresh_token_use_case()
    )


def init_identity(app: FastAPI, container: IdentityContainer) -> None:
    app.include_router(identity_router, prefix="/users", tags=["users"])

    app.dependency_overrides[ICreateIdentityUseCase] = (
        lambda: container.create_identity_use_case()
    )
    app.dependency_overrides[ITokenIntrospector] = (
        lambda: container.token_introspector()
    )


def init_token(app: FastAPI, container: TokenContainer) -> None:
    app.dependency_overrides[ITokenIntrospector] = (
        lambda: container.token_introspector()
    )


def init_recommendations(app: FastAPI, container: RecommendationContainer) -> None:
    app.include_router(recommendations_router, prefix="/api", tags=["recommendations"])

    app.dependency_overrides[IRecommendationService] = (
        lambda: container.recommendation_service()
    )


def main() -> FastAPI:
    """Initialize and bootstrap the application.

    Returns:
        Configured App instance.

    """
    # Load configuration
    config = AppConfig.load()

    # Initialize logger
    logger = LoggerFactory.create(None, config.env, config.logger)
    logger.info("logger initialized")

    log_config(logger, config)

    # Initialize database
    logger.info("initializing database...")
    database = Database.create(config.db, logger)
    logger.info("database initialized")

    llm = MappedOpenAI(
        model=config.llm.model,
        api_key=config.llm.api_key,
        api_base=config.llm.base_url,
        temperature=0.3,
    )
    MappedOpenAI.override(config.llm.model, config.llm.provider_model)
    logger.info("llm initialized")

    # Create FastAPI server
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
        yield
        await database.shutdown()

    server = FastAPI(lifespan=lifespan)

    # Bootstrap common container with config and database
    common_container = CommonContainer(config=config, database=database)

    uuid_generator = common_container.uuid_generator
    query_executor = common_container.query_executor
    clock = common_container.clock

    identity_container = IdentityContainer(
        uuid_generator=uuid_generator,
        query_executor=query_executor,
        token_introspector=None,  # NOTE: Need to be overriden later
    )

    token_container = TokenContainer(
        auth_config=config.auth,
        clock=clock,
        uuid_generator=uuid_generator,
        token_generator=common_container.token_generator,
        query_executor=query_executor,
        identity_repository=identity_container.identity_repository,
    )

    identity_container.token_introspector.override(token_container.token_introspector)

    auth_container = AuthContainer(
        identity_service=identity_container.identity_service,
        token_issuer=token_container.token_issuer,
        token_revoker=token_container.token_revoker,
        token_refresher=token_container.token_refresher,
    )

    course_container = CourseContainer(
        uuid_generator=uuid_generator, query_executor=query_executor, clock=clock
    )
    lecturer_container = LecturerContainer(
        uuid_generator=uuid_generator, query_executor=query_executor, clock=clock
    )
    category_container = CategoryContainer(
        uuid_generator=uuid_generator, query_executor=query_executor, clock=clock
    )

    recommendation_container = RecommendationContainer(
        llm=llm,
        course_read_repository=course_container.course_read_repository,
        category_read_repository=category_container.category_read_repository,
    )

    # Register routes
    init_course(server, course_container)
    init_lecturer(server, lecturer_container)
    init_category(server, category_container)
    init_identity(server, identity_container)
    init_auth(server, auth_container)
    init_token(server, token_container)
    init_recommendations(server, recommendation_container)

    # Create and configure app
    return server


app = main()
if __name__ == "__main__":
    pass
