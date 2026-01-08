"""Get lecturers query DTO."""

from dataclasses import dataclass


@dataclass
class GetLecturersQuery:
    """Query to get all lecturers."""

    skip: int = 0
    limit: int = 100
