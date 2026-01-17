"""Filter state for course filtering."""


from aiogram.fsm.state import State, StatesGroup


class FilterState(StatesGroup):
    """State for course filtering."""

    waiting_for_search = State()
    waiting_for_recommendation = State()
    browsing_courses = State()
    viewing_course = State()
