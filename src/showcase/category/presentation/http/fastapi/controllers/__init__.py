"""Category FastAPI controllers using CBV."""

from typing import Annotated
from uuid import UUID

from common.presentation.http.dto.response import IDResponse
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_utils.cbv import cbv
from showcase.category.application.dtos.commands.create_category_command import (
    CreateCategoryCommand,
)
from showcase.category.application.dtos.commands.update_category_command import (
    UpdateCategoryCommand,
)
from showcase.category.application.dtos.queries import (
    GetCategoriesQuery,
    GetCategoryByIdQuery,
)
from showcase.category.application.interfaces.usecases.command.create_category_use_case import (
    ICreateCategoryUseCase,
)
from showcase.category.application.interfaces.usecases.command.delete_category_use_case import (
    IDeleteCategoryUseCase,
)
from showcase.category.application.interfaces.usecases.command.update_category_use_case import (
    IUpdateCategoryUseCase,
)
from showcase.category.application.interfaces.usecases.query import (
    IGetCategoriesUseCase,
    IGetCategoryByIdUseCase,
)
from showcase.category.application.read_models.category_read_model import (
    CategoryReadModel,
)
from showcase.category.presentation.http.fastapi.dto.request import (
    CreateCategoryRequest,
    UpdateCategoryRequest,
)


category_router = APIRouter(prefix="/categories", tags=["categories"])


@cbv(category_router)
class CategoryController:
    """Controller (CBV) for category endpoints using fastapi_utils.cbv."""

    get_categories_use_case: IGetCategoriesUseCase = Depends()
    get_category_by_id_use_case: IGetCategoryByIdUseCase = Depends()
    create_category_use_case: ICreateCategoryUseCase = Depends()
    update_category_use_case: IUpdateCategoryUseCase = Depends()
    delete_category_use_case: IDeleteCategoryUseCase = Depends()

    @category_router.get("/")
    async def list_categories(
        self,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=1000)] = 100,
    ) -> list[CategoryReadModel]:
        """Get all categories with optional filters."""
        query = GetCategoriesQuery(skip=skip, limit=limit)
        return await self.get_categories_use_case.execute(query)

    @category_router.get("/{category_id}")
    async def get_category_by_id(self, category_id: UUID) -> CategoryReadModel:
        """Get a category by ID."""
        try:
            query = GetCategoryByIdQuery(category_id=category_id)
            return await self.get_category_by_id_use_case.execute(query)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e

    @category_router.post("/")
    async def create_category(self, request: CreateCategoryRequest) -> IDResponse:
        """Create a new category."""
        command = CreateCategoryCommand(
            name=request.name,
            description=request.description,
        )
        category_id = await self.create_category_use_case.execute(command)
        return IDResponse.from_uuid(category_id)

    @category_router.put("/{category_id}")
    async def update_category(
        self, category_id: UUID, request: UpdateCategoryRequest
    ) -> IDResponse:
        """Update an existing category."""
        command = UpdateCategoryCommand(
            category_id=category_id,
            name=request.name,
            description=request.description,
        )
        updated_id = await self.update_category_use_case.execute(command)
        return IDResponse.from_uuid(updated_id)

    @category_router.delete("/{category_id}")
    async def delete_category(self, category_id: UUID) -> IDResponse:
        deleted_id = await self.delete_category_use_case.execute(category_id)
        return IDResponse.from_uuid(deleted_id)
