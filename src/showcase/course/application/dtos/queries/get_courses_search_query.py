"""Get courses search query DTO."""

from dataclasses import dataclass


@dataclass
class GetCoursesSearchQuery:
    query: str
    skip: int = 0
    limit: int = 50
    # optional filters kept for parity
    is_published: bool | None = None
    status: str | None = None
