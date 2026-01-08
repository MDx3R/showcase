"""Category use case interfaces."""

from .get_categories_usecase import IGetCategoriesUseCase
from .get_category_by_id_usecase import IGetCategoryByIdUseCase


__all__ = ["IGetCategoriesUseCase", "IGetCategoryByIdUseCase"]
