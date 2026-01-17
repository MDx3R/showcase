"""Course formatters for Telegram."""

from datetime import datetime

from showcase.course.application.read_models.course_read_model import CourseReadModel


def format_course_short(course: CourseReadModel, index: int | None = None) -> str:
    """Format a short course description for list display."""
    prefix = f"{index}. " if index is not None else ""
    price_str = f"{course.cost:.0f} ₽"
    if course.discounted_cost:
        price_str = f"~~{course.cost:.0f}~~ {course.discounted_cost:.0f} ₽"

    duration_str = f"{course.duration_hours} ч."
    format_str = _format_to_display(course.format.value)

    return (
        f"{prefix}**{course.name}**\n"
        f"💰 {price_str} | ⏱ {duration_str} | 📍 {format_str}"
    )


def format_course_list(courses: list[CourseReadModel], page: int = 1) -> str:
    """Format a list of courses for display."""
    if not courses:
        return "❌ Курсы не найдены."

    text = f"📚 **Найдено курсов: {len(courses)}**\n\n"

    for idx, course in enumerate(courses, start=1):
        text += format_course_short(course, index=idx)
        text += "\n\n"

    return text


def format_course_detail(course: CourseReadModel) -> str:
    """Format a detailed course description."""
    price_str = f"{course.cost:.0f} ₽"
    if course.discounted_cost:
        price_str = f"~~{course.cost:.0f}~~ **{course.discounted_cost:.0f} ₽**"

    format_str = _format_to_display(course.format.value)
    education_format_str = _education_format_to_display(course.education_format.value)
    certificate_str = _certificate_to_display(course.certificate_type.value)
    status_str = _status_to_display(course.status.value)

    text = f"📚 **{course.name}**\n\n"

    if course.description:
        # Truncate description if too long
        desc = (
            course.description[:500] + "..."
            if len(course.description) > 500
            else course.description
        )
        text += f"{desc}\n\n"

    text += f"💰 **Цена:** {price_str}\n"
    text += f"⏱ **Длительность:** {course.duration_hours} часов\n"
    text += f"📍 **Формат:** {format_str}\n"
    text += f"👥 **Обучение:** {education_format_str}\n"
    text += f"📜 **Сертификат:** {certificate_str}\n"
    text += f"📊 **Статус:** {status_str}\n"

    if course.locations:
        locations_str = ", ".join(course.locations[:3])
        if len(course.locations) > 3:
            locations_str += f" и ещё {len(course.locations) - 3}"
        text += f"🗺 **Местоположения:** {locations_str}\n"

    if course.start_date:
        start_str = course.start_date.strftime("%d.%m.%Y")
        text += f"📅 **Начало:** {start_str}\n"

    if course.categories:
        categories_str = ", ".join([c.name for c in course.categories[:3]])
        if len(course.categories) > 3:
            categories_str += f" и ещё {len(course.categories) - 3}"
        text += f"🏷 **Категории:** {categories_str}\n"

    if course.tags:
        tags_str = ", ".join(course.tags[:5])
        if len(course.tags) > 5:
            tags_str += f" и ещё {len(course.tags) - 5}"
        text += f"#️⃣ **Теги:** {tags_str}\n"

    if course.acquired_skills:
        skills_str = ", ".join([s.name for s in course.acquired_skills[:3]])
        if len(course.acquired_skills) > 3:
            skills_str += f" и ещё {len(course.acquired_skills) - 3}"
        text += f"🎯 **Навыки:** {skills_str}\n"

    if course.lecturers:
        lecturers_str = ", ".join([l.name for l in course.lecturers[:2]])
        if len(course.lecturers) > 2:
            lecturers_str += f" и ещё {len(course.lecturers) - 2}"
        text += f"👨‍🏫 **Преподаватели:** {lecturers_str}\n"

    if course.sections:
        text += "\n📋 **Программа курса:**\n"
        for section in course.sections[:5]:
            hours_str = f" ({section.hours} ч.)" if section.hours else ""
            text += f"  • {section.name}{hours_str}\n"
        if len(course.sections) > 5:
            text += f"  ... и ещё {len(course.sections) - 5} модулей\n"

    return text


def _format_to_display(format_value: str) -> str:
    """Convert format enum value to display string."""
    mapping = {
        "online": "Онлайн",
        "offline": "Офлайн",
        "mixed": "Смешанный",
    }
    return mapping.get(format_value, format_value)


def _education_format_to_display(format_value: str) -> str:
    """Convert education format enum value to display string."""
    mapping = {
        "group": "Групповое",
        "individual": "Индивидуальное",
        "self_paced": "Самостоятельное",
        "mentorled": "С ментором",
        "cohort": "Поток/Набор",
    }
    return mapping.get(format_value, format_value)


def _certificate_to_display(cert_value: str) -> str:
    """Convert certificate type enum value to display string."""
    mapping = {
        "certificate": "Сертификат",
        "diploma": "Диплом",
        "attestation": "Аттестация",
        "none": "Без сертификата",
    }
    return mapping.get(cert_value, cert_value)


def _status_to_display(status_value: str) -> str:
    """Convert status enum value to display string."""
    mapping = {
        "active": "Активный",
        "enrolling": "Набор открыт",
        "archived": "Архив",
        "draft": "Черновик",
    }
    return mapping.get(status_value, status_value)
