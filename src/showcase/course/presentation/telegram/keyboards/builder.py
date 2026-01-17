"""Keyboard builders for Telegram bot."""

from collections.abc import Sequence
from uuid import UUID

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from showcase.course.application.read_models.course_read_model import CourseReadModel


def build_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Build main menu keyboard."""
    builder = InlineKeyboardBuilder()

    builder.button(text="🔍 Поиск курсов", callback_data="search")
    builder.button(text="✨ Рекомендации", callback_data="recommend")
    builder.button(text="📚 Все курсы", callback_data="list_all")
    builder.button(text="🔧 Фильтры", callback_data="filters")

    builder.adjust(2)
    return builder.as_markup()


def build_course_list_keyboard(
    courses: Sequence[CourseReadModel],
    page: int = 1,
    page_size: int = 5,
    has_next: bool = False,
) -> InlineKeyboardMarkup:
    """Build keyboard for course list with pagination."""
    builder = InlineKeyboardBuilder()

    # Course buttons
    # If courses list is smaller or equal to page_size, assume it's already sliced to current page
    if len(courses) <= page_size:
        # Already sliced, show all courses
        course_list = courses
    else:
        # Full list, slice it
        start_idx = (page - 1) * page_size
        end_idx = min(start_idx + page_size, len(courses))
        course_list = courses[start_idx:end_idx]

    for course in course_list:
        course_name = course.name[:30] + "..." if len(course.name) > 30 else course.name
        builder.button(
            text=f"📚 {course_name}",
            callback_data=f"course_{course.course_id}",
        )

    builder.adjust(3)

    # Pagination buttons
    pagination_row = []
    if page > 1:
        pagination_row.append(
            InlineKeyboardButton(text="◀️ Назад", callback_data=f"page_{page - 1}")
        )
    if has_next:
        pagination_row.append(
            InlineKeyboardButton(text="Вперёд ▶️", callback_data=f"page_{page + 1}")
        )

    if pagination_row:
        builder.row(*pagination_row)

    builder.button(text="🏠 Главное меню", callback_data="main_menu")

    return builder.as_markup()


def build_course_detail_keyboard(
    course_id: UUID, back_to_list: bool = True
) -> InlineKeyboardMarkup:
    """Build keyboard for course detail view."""
    builder = InlineKeyboardBuilder()

    builder.button(text="📝 Записаться", callback_data=f"enroll_{course_id}")
    if back_to_list:
        builder.button(text="⬅️ Назад к списку", callback_data="back_to_list")
    builder.button(text="🏠 Главное меню", callback_data="main_menu")

    builder.adjust(1)
    return builder.as_markup()


def build_filter_keyboard() -> InlineKeyboardMarkup:
    """Build filter selection keyboard."""
    builder = InlineKeyboardBuilder()

    builder.button(text="📍 Формат (онлайн/офлайн)", callback_data="filter_format")
    builder.button(text="📊 Статус", callback_data="filter_status")
    builder.button(text="🏷 Категория", callback_data="filter_category")
    builder.button(text="❌ Сбросить фильтры", callback_data="filter_reset")
    builder.button(text="🏠 Главное меню", callback_data="main_menu")

    builder.adjust(2)
    return builder.as_markup()


def build_format_filter_keyboard() -> InlineKeyboardMarkup:
    """Build format filter selection keyboard."""
    builder = InlineKeyboardBuilder()

    builder.button(text="🌐 Онлайн", callback_data="filter_format_online")
    builder.button(text="🏢 Офлайн", callback_data="filter_format_offline")
    builder.button(text="🔀 Смешанный", callback_data="filter_format_mixed")
    builder.button(text="❌ Без фильтра", callback_data="filter_format_none")
    builder.button(text="⬅️ Назад", callback_data="filters")

    builder.adjust(2)
    return builder.as_markup()


def build_status_filter_keyboard() -> InlineKeyboardMarkup:
    """Build status filter selection keyboard."""
    builder = InlineKeyboardBuilder()

    builder.button(text="✅ Активные", callback_data="filter_status_active")
    builder.button(text="📝 Набор открыт", callback_data="filter_status_enrolling")
    builder.button(text="📦 Архив", callback_data="filter_status_archived")
    builder.button(text="❌ Без фильтра", callback_data="filter_status_none")
    builder.button(text="⬅️ Назад", callback_data="filters")

    builder.adjust(2)
    return builder.as_markup()


def build_category_filter_keyboard(
    categories: Sequence, max_per_page: int = 10
) -> InlineKeyboardMarkup:
    """Build category filter selection keyboard."""
    builder = InlineKeyboardBuilder()

    for category in categories[:max_per_page]:
        category_name = (
            category.name[:30] + "..." if len(category.name) > 30 else category.name
        )
        builder.button(
            text=f"🏷 {category_name}",
            callback_data=f"filter_category_{category.category_id}",
        )

    builder.button(text="❌ Без фильтра", callback_data="filter_category_none")
    builder.button(text="⬅️ Назад", callback_data="filters")

    builder.adjust(1)
    return builder.as_markup()


def build_pagination_keyboard(
    page: int,
    has_next: bool,
    prefix: str = "page",
) -> InlineKeyboardMarkup:
    """Build simple pagination keyboard."""
    builder = InlineKeyboardBuilder()

    if page > 1:
        builder.button(text="◀️ Назад", callback_data=f"{prefix}_{page - 1}")
    if has_next:
        builder.button(text="Вперёд ▶️", callback_data=f"{prefix}_{page + 1}")

    return builder.as_markup()
