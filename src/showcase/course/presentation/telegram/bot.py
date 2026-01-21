"""Telegram bot entry point."""

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from common.infrastructure.config.deployment_meta import DeploymentMeta
from showcase.category.application.interfaces.usecases.query.get_categories_usecase import (
    IGetCategoriesUseCase,
)
from showcase.course.application.interfaces.services.recommendation_service import (
    IRecommendationService,
)
from showcase.course.application.interfaces.usecases.query import (
    IGetCoursesExtendedUseCase,
    IGetCoursesUseCase,
)
from showcase.course.application.interfaces.usecases.query.get_course_by_id_usecase import (
    IGetCourseByIdUseCase,
)
from showcase.course.application.interfaces.usecases.query.get_courses_search_usecase import (
    IGetCoursesSearchUseCase,
)
from showcase.course.presentation.telegram.handlers.commands import CommandHandler
from showcase.course.presentation.telegram.handlers.course_callbacks import (
    CourseCallbackHandler,
)
from showcase.course.presentation.telegram.handlers.filter_callbacks import (
    FilterCallbackHandler,
)
from showcase.course.presentation.telegram.handlers.menu_callbacks import (
    MenuCallbackHandler,
)
from showcase.course.presentation.telegram.handlers.pagination_callbacks import (
    PaginationCallbackHandler,
)
from showcase.course.presentation.telegram.handlers.queries import QueryHandler
from showcase.course.presentation.telegram.services.course_list_service import (
    CourseListService,
)


def create_bot(
    token: str,
    get_courses_use_case: IGetCoursesUseCase,
    get_course_by_id_use_case: IGetCourseByIdUseCase,
    get_courses_search_use_case: IGetCoursesSearchUseCase,
    recommendation_service: IRecommendationService,
) -> Bot:
    """Create and configure Telegram bot.

    Args:
        token: Telegram bot token
        get_courses_use_case: Use case for getting courses
        get_course_by_id_use_case: Use case for getting course by ID
        get_courses_search_use_case: Use case for searching courses
        recommendation_service: Service for course recommendations

    Returns:
        Configured Bot instance

    """
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    return bot


def create_dispatcher(
    deploy_meta: DeploymentMeta,
    get_courses_use_case: IGetCoursesExtendedUseCase,
    get_course_by_id_use_case: IGetCourseByIdUseCase,
    get_courses_search_use_case: IGetCoursesSearchUseCase,
    get_categories_use_case: IGetCategoriesUseCase,
    recommendation_service: IRecommendationService,
) -> Dispatcher:
    """Create and configure Telegram bot dispatcher.

    Args:
        get_courses_use_case: Use case for getting courses
        get_course_by_id_use_case: Use case for getting course by ID
        get_courses_search_use_case: Use case for searching courses
        get_categories_use_case: Use case for getting categories
        recommendation_service: Service for course recommendations

    Returns:
        Configured Dispatcher instance

    """
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Shared service for course listing
    course_list_service = CourseListService(get_courses_use_case)

    # Initialize handlers
    command_handler = CommandHandler(
        deploy_meta=deploy_meta,
        get_courses_search_use_case=get_courses_search_use_case,
        course_list_service=course_list_service,
    )

    menu_callback_handler = MenuCallbackHandler(
        course_list_service=course_list_service,
    )

    course_callback_handler = CourseCallbackHandler(
        deploy_meta=deploy_meta,
        get_course_by_id_use_case=get_course_by_id_use_case,
    )

    filter_callback_handler = FilterCallbackHandler(
        get_categories_use_case=get_categories_use_case,
        course_list_service=course_list_service,
    )

    pagination_callback_handler = PaginationCallbackHandler(
        course_list_service=course_list_service,
    )

    query_handler = QueryHandler(
        get_courses_search_use_case=get_courses_search_use_case,
        recommendation_service=recommendation_service,
        course_list_service=course_list_service,
    )

    # Register routers
    dp.include_router(command_handler.router)
    dp.include_router(menu_callback_handler.router)
    dp.include_router(course_callback_handler.router)
    dp.include_router(filter_callback_handler.router)
    dp.include_router(pagination_callback_handler.router)
    dp.include_router(query_handler.router)

    return dp


async def start_polling(
    bot: Bot,
    dispatcher: Dispatcher,
) -> None:
    """Start bot polling.

    Args:
        bot: Telegram bot instance
        dispatcher: Bot dispatcher instance

    """
    await dispatcher.start_polling(bot)
