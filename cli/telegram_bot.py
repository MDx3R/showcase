"""Telegram bot entry point."""

import asyncio

from bootstrap.config import AppConfig
from bootstrap.utils import log_config
from common.infrastructure.database.postgres.sqlalchemy.database import Database
from common.infrastructure.di.container.common import CommonContainer
from common.infrastructure.logger.logging.logger_factory import LoggerFactory
from common.infrastructure.services.llama_index.client import MappedOpenAI
from showcase.category.infrastructure.di.container import CategoryContainer
from showcase.course.infrastructure.di.container import (
    CourseContainer,
    RecommendationContainer,
)
from showcase.course.presentation.telegram import (
    create_bot,
    create_dispatcher,
    start_polling,
)


def main() -> None:
    """Initialize and start Telegram bot."""
    # Load configuration
    config = AppConfig.load()

    if not config.telegram or not config.telegram.enabled:
        print("Telegram bot is disabled in configuration.")
        return

    if not config.telegram.token:
        raise ValueError(
            "Telegram bot token is not configured. Set TELEGRAM__TOKEN environment variable or configure in YAML."
        )

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

    # Bootstrap common container with config and database
    common_container = CommonContainer(config=config, database=database, logger=logger)

    query_executor = common_container.query_executor

    course_container = CourseContainer(
        uuid_generator=common_container.uuid_generator,
        query_executor=query_executor,
        clock=common_container.clock,
    )

    category_container = CategoryContainer(
        uuid_generator=common_container.uuid_generator,
        query_executor=query_executor,
        clock=common_container.clock,
    )

    recommendation_container = RecommendationContainer(
        logger=logger,
        llm=llm,
        course_read_repository=course_container.course_read_repository,
        category_read_repository=category_container.category_read_repository,
    )

    # Create bot and dispatcher
    logger.info("creating telegram bot...")
    bot = create_bot(
        token=config.telegram.token,
        get_courses_use_case=course_container.get_courses_usecase(),
        get_course_by_id_use_case=course_container.get_course_by_id_usecase(),
        get_courses_search_use_case=course_container.get_courses_search_usecase(),
        recommendation_service=recommendation_container.recommendation_service(),
    )

    dp = create_dispatcher(
        get_courses_use_case=course_container.get_courses_usecase(),
        get_course_by_id_use_case=course_container.get_course_by_id_usecase(),
        get_courses_search_use_case=course_container.get_courses_search_usecase(),
        get_categories_use_case=category_container.get_categories_usecase(),
        recommendation_service=recommendation_container.recommendation_service(),
    )

    logger.info("telegram bot initialized")

    # Start polling
    async def run() -> None:
        try:
            logger.info("starting telegram bot polling...")
            await start_polling(bot, dp)
        finally:
            await bot.session.close()
            await database.shutdown()
            logger.info("telegram bot stopped")

    asyncio.run(run())


if __name__ == "__main__":
    main()
