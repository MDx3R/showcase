"""Lecturer bounded context DI container."""

from typing import Any

from dependency_injector import containers, providers
from showcase.lecturer.application.usecases import (
    CreateLecturerUseCase,
    GetLecturerByIdUseCase,
    GetLecturersUseCase,
    UpdateLecturerUseCase,
)
from showcase.lecturer.application.usecases.command.delete_lecturer_use_case import (
    DeleteLecturerUseCase,
)
from showcase.lecturer.infrastructure.database.postgres.sqlalchemy.repositories import (
    LecturerReadRepository,
    LecturerRepository,
)


class LecturerContainer(containers.DeclarativeContainer):
    """Dependency injection container for lecturer bounded context."""

    # Explicit dependency declarations
    uuid_generator: providers.Dependency[Any] = providers.Dependency()
    query_executor: providers.Dependency[Any] = providers.Dependency()
    clock: providers.Dependency[Any] = providers.Dependency()

    # Read repository
    lecturer_read_repository = providers.Factory(LecturerReadRepository, query_executor)

    # Write repository
    lecturer_repository = providers.Factory(LecturerRepository, query_executor)

    # Read use cases
    get_lecturers_usecase = providers.Factory(
        GetLecturersUseCase, lecturer_read_repository
    )
    get_lecturer_by_id_usecase = providers.Factory(
        GetLecturerByIdUseCase, lecturer_read_repository
    )

    # Write use cases
    create_lecturer_usecase = providers.Factory(
        CreateLecturerUseCase,
        lecturer_repository=lecturer_repository,
        uuid_generator=uuid_generator,
    )
    update_lecturer_usecase = providers.Factory(
        UpdateLecturerUseCase, lecturer_repository
    )
    delete_lecturer_usecase = providers.Factory(
        DeleteLecturerUseCase, lecturer_repository
    )
