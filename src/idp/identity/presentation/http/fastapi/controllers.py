from typing import Annotated

from common.presentation.http.dto.response import IDResponse
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_utils.cbv import cbv
from idp.identity.application.dtos.commands.create_identity_command import (
    CreateIdentityCommand,
)
from idp.identity.application.exceptions import (
    EmailAlreadyTakenError,
)
from idp.identity.application.interfaces.usecases.command.create_identity_use_case import (
    ICreateIdentityUseCase,
)
from idp.identity.domain.value_objects.descriptor import IdentityDescriptor
from idp.identity.presentation.http.dto.request import RegisterUserRequest
from idp.identity.presentation.http.dto.response import IdentityResponse
from idp.identity.presentation.http.fastapi.auth import (
    get_descriptor,
    require_authenticated,
    require_unauthenticated,
)


identity_router = APIRouter()


@cbv(identity_router)
class IdentityController:
    create_identity_use_case: ICreateIdentityUseCase = Depends()

    @identity_router.get("/me", dependencies=[Depends(require_authenticated)])
    async def me(
        self, descriptor: Annotated[IdentityDescriptor, Depends(get_descriptor)]
    ) -> IdentityResponse:
        return IdentityResponse(
            id=descriptor.identity_id,
            email=descriptor.email,
            username=descriptor.username,
            role=descriptor.role,
        )

    @identity_router.post("/register", dependencies=[Depends(require_unauthenticated)])
    async def register(self, request: RegisterUserRequest) -> IDResponse:
        try:
            identity_id = await self.create_identity_use_case.execute(
                CreateIdentityCommand(request.email, request.username, request.password)
            )
            return IDResponse(id=identity_id)
        except EmailAlreadyTakenError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": "EmailAlreadyTakenError",
                    "email": exc.email,
                    "message": f"Электронная почта '{request.email}' уже занята другим пользователем.",
                },
            ) from exc
