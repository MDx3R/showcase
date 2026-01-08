"""Get categories query DTO."""

from dataclasses import dataclass


@dataclass
class GetCategoriesQuery:
    """Query to get all categories with optional filters."""

    skip: int = 0
    limit: int = 100
