"""Command handlers for Telegram bot."""

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from showcase.course.application.dtos.queries import (
    GetCoursesQuery,
    GetCoursesSearchQuery,
)
from showcase.course.application.interfaces.usecases.query import (
    IGetCoursesUseCase,
)
from showcase.course.application.interfaces.usecases.query.get_course_by_id_usecase import (
    IGetCourseByIdUseCase,
)
from showcase.course.application.interfaces.usecases.query.get_courses_search_usecase import (
    IGetCoursesSearchUseCase,
)
from showcase.course.presentation.telegram.formatters.course import format_course_list
from showcase.course.presentation.telegram.keyboards.builder import (
    build_course_list_keyboard,
    build_main_menu_keyboard,
)


class CommandHandler:
    """Handler for Telegram bot commands."""

    def __init__(
        self,
        get_courses_use_case: IGetCoursesUseCase,
        get_course_by_id_use_case: IGetCourseByIdUseCase,
        get_courses_search_use_case: IGetCoursesSearchUseCase,
    ) -> None:
        self.get_courses_use_case = get_courses_use_case
        self.get_course_by_id_use_case = get_course_by_id_use_case
        self.get_courses_search_use_case = get_courses_search_use_case
        self.router = Router()

        self._register_handlers()

    def _register_handlers(self) -> None:
        """Register command handlers."""
        self.router.message.register(self._handle_start, CommandStart())
        self.router.message.register(self._handle_help, Command("help"))
        self.router.message.register(self._handle_list, Command("list"))
        self.router.message.register(self._handle_search, Command("search"))

    async def _handle_start(self, message: Message) -> None:
        """Handle /start command."""
        text = (
            "👋 Добро пожаловать в бот каталога курсов!\n\n"
            "Доступные команды:\n"
            "/list - показать все курсы\n"
            "/search <запрос> - поиск курсов\n"
            "/help - помощь\n\n"
            "Или используйте меню ниже:"
        )
        keyboard = build_main_menu_keyboard()
        await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")

    async def _handle_help(self, message: Message) -> None:
        """Handle /help command."""
        text = (
            "📖 **Помощь**\n\n"
            "**Команды:**\n"
            "/start - начать работу\n"
            "/list - показать все курсы\n"
            "/search <запрос> - поиск курсов по тексту\n"
            "/help - эта справка\n\n"
            "**Использование:**\n"
            "• Используйте меню для навигации\n"
            "• Для рекомендаций нажмите '✨ Рекомендации' и введите свой запрос\n"
            "• Используйте фильтры для уточнения поиска"
        )
        keyboard = build_main_menu_keyboard()
        await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")

    async def _handle_list(self, message: Message) -> None:
        """Handle /list command."""
        query = GetCoursesQuery(is_published=True, limit=5)
        courses = await self.get_courses_use_case.execute(query)

        if not courses:
            await message.answer("❌ Курсы не найдены.")
            return

        text = format_course_list(courses)
        keyboard = build_course_list_keyboard(
            courses, page=1, has_next=len(courses) >= 5
        )

        await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")

    async def _handle_search(self, message: Message) -> None:
        """Handle /search command."""
        # Extract search query from command
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            await message.answer(
                "❌ Укажите запрос для поиска.\nПример: /search Python"
            )
            return

        query_text = parts[1]
        search_query = GetCoursesSearchQuery(query=query_text, limit=5)
        courses = await self.get_courses_search_use_case.execute(search_query)

        if not courses:
            await message.answer(f"❌ По запросу '{query_text}' ничего не найдено.")
            return

        text = format_course_list(courses)
        keyboard = build_course_list_keyboard(
            courses, page=1, has_next=len(courses) >= 5
        )

        await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")
