"""Category bounded context DI container."""

from typing import Any

from dependency_injector import containers, providers
from showcase.category.application.usecases import (
    CreateCategoryUseCase,
    DeleteCategoryUseCase,
    GetCategoriesUseCase,
    GetCategoryByIdUseCase,
    UpdateCategoryUseCase,
)
from showcase.category.infrastructure.database.postgres.sqlalchemy.repositories import (
    CategoryReadRepository,
    CategoryRepository,
)


class CategoryContainer(containers.DeclarativeContainer):
    """Dependency injection container for category bounded context."""

    # Explicit dependency declarations
    uuid_generator: providers.Dependency[Any] = providers.Dependency()
    query_executor: providers.Dependency[Any] = providers.Dependency()
    clock: providers.Dependency[Any] = providers.Dependency()

    # Read repository
    category_read_repository = providers.Factory(CategoryReadRepository, query_executor)

    # Write repository
    category_repository = providers.Factory(CategoryRepository, query_executor)

    # Read use cases
    get_categories_usecase = providers.Factory(
        GetCategoriesUseCase, category_read_repository
    )
    delete_category_usecase = providers.Factory(
        DeleteCategoryUseCase, category_repository
    )
    get_category_by_id_usecase = providers.Factory(
        GetCategoryByIdUseCase, category_read_repository
    )

    # Write use cases
    create_category_usecase = providers.Factory(
        CreateCategoryUseCase,
        category_repository=category_repository,
        uuid_generator=uuid_generator,
    )
    update_category_usecase = providers.Factory(
        UpdateCategoryUseCase, category_repository
    )
