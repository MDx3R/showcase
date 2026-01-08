"""Course status value object."""

from enum import Enum


class CourseStatus(str, Enum):
    """Status of a course."""

    ACTIVE = "active"
    ENROLLING = "enrolling"
    ARCHIVED = "archived"
    DRAFT = "draft"
