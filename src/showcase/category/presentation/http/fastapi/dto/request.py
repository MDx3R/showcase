"""Presentation layer request DTOs for category with validation."""

from pydantic import BaseModel, Field


class CreateCategoryRequest(BaseModel):
    """Request model for creating a category."""

    name: str = Field(min_length=1, max_length=255)
    description: str | None = None


class UpdateCategoryRequest(BaseModel):
    """Request model for updating a category (without category_id in body)."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None
