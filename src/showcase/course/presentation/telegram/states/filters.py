"""Filter state for course filtering."""

from aiogram.fsm.state import State, StatesGroup
from uuid import UUID

from showcase.course.domain.value_objects import CourseStatus, Format


class FilterState(StatesGroup):
    """State for course filtering."""

    waiting_for_search = State()
    waiting_for_recommendation = State()
    browsing_courses = State()
    viewing_course = State()
