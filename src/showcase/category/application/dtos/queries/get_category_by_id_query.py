"""Get category by ID query DTO."""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class GetCategoryByIdQuery:
    """Query to get a category by ID."""

    category_id: UUID
