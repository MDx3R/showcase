"""Telegram bot entry point."""

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from showcase.course.application.interfaces.services.recommendation_service import (
    IRecommendationService,
)
from showcase.course.application.interfaces.usecases.query import IGetCoursesUseCase
from showcase.course.application.interfaces.usecases.query.get_course_by_id_usecase import (
    IGetCourseByIdUseCase,
)
from showcase.course.application.interfaces.usecases.query.get_courses_search_usecase import (
    IGetCoursesSearchUseCase,
)
from showcase.category.application.interfaces.usecases.query.get_categories_usecase import (
    IGetCategoriesUseCase,
)
from showcase.course.presentation.telegram.handlers.commands import CommandHandler
from showcase.course.presentation.telegram.handlers.callbacks import CallbackHandler
from showcase.course.presentation.telegram.handlers.queries import QueryHandler


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
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))

    return bot


def create_dispatcher(
    get_courses_use_case: IGetCoursesUseCase,
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
        recommendation_service: Service for course recommendations

    Returns:
        Configured Dispatcher instance
    """
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Initialize handlers
    command_handler = CommandHandler(
        get_courses_use_case=get_courses_use_case,
        get_course_by_id_use_case=get_course_by_id_use_case,
        get_courses_search_use_case=get_courses_search_use_case,
    )

    callback_handler = CallbackHandler(
        get_courses_use_case=get_courses_use_case,
        get_course_by_id_use_case=get_course_by_id_use_case,
        get_categories_use_case=get_categories_use_case,
    )

    query_handler = QueryHandler(
        get_courses_search_use_case=get_courses_search_use_case,
        recommendation_service=recommendation_service,
    )

    # Register routers
    dp.include_router(command_handler.router)
    dp.include_router(callback_handler.router)
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
