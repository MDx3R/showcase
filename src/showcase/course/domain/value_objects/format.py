"""Course format value object."""

from enum import Enum


class Format(str, Enum):
    """Format of a course."""

    ONLINE = "online"
    OFFLINE = "offline"
    MIXED = "mixed"
