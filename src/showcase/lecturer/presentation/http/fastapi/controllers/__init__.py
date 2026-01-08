"""Lecturer FastAPI controllers using CBV."""

from typing import Annotated
from uuid import UUID

from common.presentation.http.dto.response import IDResponse
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_utils.cbv import cbv
from showcase.lecturer.application.dtos.commands.create_lecturer_command import (
    CreateLecturerCommand,
)
from showcase.lecturer.application.dtos.commands.update_lecturer_command import (
    UpdateLecturerCommand,
)
from showcase.lecturer.application.dtos.queries import (
    GetLecturerByIdQuery,
    GetLecturersQuery,
)
from showcase.lecturer.application.interfaces.usecases.command.create_lecturer_use_case import (
    ICreateLecturerUseCase,
)
from showcase.lecturer.application.interfaces.usecases.command.delete_lecturer_use_case import (
    IDeleteLecturerUseCase,
)
from showcase.lecturer.application.interfaces.usecases.command.update_lecturer_use_case import (
    IUpdateLecturerUseCase,
)
from showcase.lecturer.application.interfaces.usecases.query import (
    IGetLecturerByIdUseCase,
    IGetLecturersUseCase,
)
from showcase.lecturer.application.read_models.lecturer_read_model import (
    LecturerReadModel,
)


lecturer_router = APIRouter(prefix="/lecturers", tags=["lecturers"])


@cbv(lecturer_router)
class LecturerController:
    """Controller (CBV) for lecturer endpoints using fastapi_utils.cbv."""

    get_lecturers_use_case: IGetLecturersUseCase = Depends()
    get_lecturer_by_id_use_case: IGetLecturerByIdUseCase = Depends()
    create_lecturer_use_case: ICreateLecturerUseCase = Depends()
    update_lecturer_use_case: IUpdateLecturerUseCase = Depends()
    delete_lecturer_use_case: IDeleteLecturerUseCase = Depends()

    @lecturer_router.get("/")
    async def list_lecturers(
        self,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=1000)] = 100,
    ) -> list[LecturerReadModel]:
        """Get all lecturers."""
        query = GetLecturersQuery(skip=skip, limit=limit)
        return await self.get_lecturers_use_case.execute(query)

    @lecturer_router.get("/{lecturer_id}")
    async def get_lecturer_by_id(self, lecturer_id: UUID) -> LecturerReadModel:
        """Get a lecturer by ID."""
        try:
            query = GetLecturerByIdQuery(lecturer_id=lecturer_id)
            return await self.get_lecturer_by_id_use_case.execute(query)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @lecturer_router.post("/")
    async def create_lecturer(self, command: CreateLecturerCommand) -> IDResponse:
        """Create a new lecturer."""
        lecturer_id = await self.create_lecturer_use_case.execute(command)
        return IDResponse.from_uuid(lecturer_id)

    @lecturer_router.put("/{lecturer_id}")
    async def update_lecturer(
        self, lecturer_id: UUID, command: UpdateLecturerCommand
    ) -> IDResponse:
        """Update an existing lecturer."""
        command.lecturer_id = lecturer_id
        updated_id = await self.update_lecturer_use_case.execute(command)
        return IDResponse.from_uuid(updated_id)

    @lecturer_router.delete("/{lecturer_id}")
    async def delete_lecturer(self, lecturer_id: UUID) -> IDResponse:
        deleted_id = await self.delete_lecturer_use_case.execute(lecturer_id)
        return IDResponse.from_uuid(deleted_id)
