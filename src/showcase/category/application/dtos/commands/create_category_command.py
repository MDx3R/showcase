"""DTO for CreateCategory command."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateCategoryCommand:
    name: str
    description: str | None = None
