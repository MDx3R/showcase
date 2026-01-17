"""Course read repository implementation."""

from typing import Any, cast
from uuid import UUID

from common.infrastructure.database.postgres.sqlalchemy.executor import (
    QueryExecutor,
)
from showcase.category.infrastructure.database.postgres.sqlalchemy.models.category import (
    CategoryBase,
)
from showcase.course.application.interfaces.repositories import ICourseReadRepository
from showcase.course.application.interfaces.repositories.course_read_repository import (
    CoursesFilter,
    CourseSortField,
    CourseSortOrder,
    SimpleCoursesFilter,
)
from showcase.course.application.read_models.course_read_model import CourseReadModel
from showcase.course.domain.value_objects import CourseStatus
from showcase.course.infrastructure.database.postgres.sqlalchemy.mappers import (
    CourseReadMapper,
)
from showcase.course.infrastructure.database.postgres.sqlalchemy.models import (
    CourseBase,
)
from showcase.course.infrastructure.database.postgres.sqlalchemy.models.tag import (
    TagBase,
)
from sqlalchemy import ColumnElement, func, select
from sqlalchemy.orm import contains_eager, joinedload


class CourseReadRepository(ICourseReadRepository):
    """Read repository for courses."""

    def __init__(self, executor: QueryExecutor) -> None:
        self.executor = executor

    async def get_by_id(self, course_id: UUID) -> CourseReadModel:
        """Get a course by ID."""
        stmt = (
            select(CourseBase)
            .where(CourseBase.course_id == course_id)
            .options(
                joinedload(CourseBase.sections),
                joinedload(CourseBase.categories),
                joinedload(CourseBase.tags),
                joinedload(CourseBase.acquired_skills),
                joinedload(CourseBase.lecturers),
            )
        )
        model = await self.executor.execute_scalar_one(stmt)
        if not model:
            raise ValueError(f"Course with id {course_id} not found")
        return CourseReadMapper.to_read_model(model)

    async def get_all(
        self,
        status: CourseStatus | None = None,
        is_published: bool | None = None,
        category_id: UUID | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[CourseReadModel]:
        """Get all courses with optional filters."""
        stmt = select(CourseBase)

        if status is not None:
            stmt = stmt.where(CourseBase.status == status)

        if is_published is not None:
            stmt = stmt.where(CourseBase.is_published == is_published)

        if category_id is not None:
            stmt = stmt.join(CourseBase.categories).where(
                CategoryBase.category_id == category_id
            )

        stmt = (
            stmt.options(
                joinedload(CourseBase.sections),
                joinedload(CourseBase.categories),
                joinedload(CourseBase.tags),
                joinedload(CourseBase.acquired_skills),
                joinedload(CourseBase.lecturers),
            )
            .offset(skip)
            .limit(limit)
        )

        models = await self.executor.execute_scalar_many(stmt)
        return [CourseReadMapper.to_read_model(model) for model in models]

    async def search(
        self, query: str, skip: int = 0, limit: int = 50
    ) -> list[CourseReadModel]:
        """Full-text search for courses using PostgreSQL tsvector in SELECT."""
        vector = CourseBase.search_vector
        ts_query = func.plainto_tsquery("russian", query)

        rank = func.ts_rank(vector, ts_query)

        stmt = (
            select(CourseBase)
            .where(vector.op("@@")(ts_query))
            .order_by(rank.desc())
            .options(
                joinedload(CourseBase.sections),
                joinedload(CourseBase.categories),
                joinedload(CourseBase.tags),
                joinedload(CourseBase.acquired_skills),
                joinedload(CourseBase.lecturers),
            )
            .offset(skip)
            .limit(limit)
        )

        models = await self.executor.execute_scalar_many(stmt)
        return [CourseReadMapper.to_read_model(model) for model in models]

    async def filter(self, filter: SimpleCoursesFilter) -> list[CourseReadModel]:
        """Deterministic filtering.

        Returns top-N courses strictly matching filters.
        """
        stmt = select(CourseBase).distinct()

        stmt = stmt.where(
            CourseBase.status == filter.status,
            CourseBase.is_published == filter.is_published,
        )

        if filter.format is not None:
            stmt = stmt.where(CourseBase.format == filter.format)

        if filter.max_duration_hours is not None:
            stmt = stmt.where(CourseBase.duration_hours <= filter.max_duration_hours)

        if filter.certificate_required is True:
            stmt = stmt.where(CourseBase.certificate_type.isnot(None))

        if filter.categories:
            stmt = stmt.join(CourseBase.categories).where(
                CategoryBase.name.in_(filter.categories)
            )

        stmt = stmt.order_by(
            CourseBase.start_date.asc().nulls_last(),
            CourseBase.duration_hours.asc(),
        )


        stmt = (
            stmt.options(
                joinedload(CourseBase.sections),
                joinedload(CourseBase.categories),
                joinedload(CourseBase.tags),
                joinedload(CourseBase.acquired_skills),
                joinedload(CourseBase.lecturers),
            )
            .offset(filter.skip)
            .limit(filter.limit)
        )

        models = await self.executor.execute_scalar_many(stmt)
        return [CourseReadMapper.to_read_model(model) for model in models]

    async def filter_extended(self, filter: CoursesFilter) -> list[CourseReadModel]:
        stmt = select(CourseBase)

        # Флаги для отслеживания JOIN'ов
        categories_joined = False
        tags_joined = False

        # Base visibility filters
        if filter.status is not None:
            stmt = stmt.where(CourseBase.status == filter.status)
        if filter.is_published is not None:
            stmt = stmt.where(CourseBase.is_published == filter.is_published)

        if filter.search:
            stmt = stmt.filter(CourseBase.name.ilike(f"%{filter.search}%"))

        # Formats and education types
        if filter.formats:
            stmt = stmt.where(CourseBase.format.in_(filter.formats))
        if filter.education_types:
            stmt = stmt.where(CourseBase.education_format.in_(filter.education_types))

        # Tags
        if filter.tags:
            stmt = stmt.join(CourseBase.tags).where(TagBase.name.in_(filter.tags))
            tags_joined = True

        # Category ids
        if filter.category_ids:
            stmt = stmt.join(CourseBase.categories).where(
                CategoryBase.category_id.in_(filter.category_ids)
            )
            categories_joined = True

        # Price filters
        if filter.price_min is not None:
            stmt = stmt.where(CourseBase.cost >= filter.price_min)
        if filter.price_max is not None:
            stmt = stmt.where(CourseBase.cost <= filter.price_max)

        # Duration filters
        if filter.duration_min is not None:
            stmt = stmt.where(CourseBase.duration_hours >= filter.duration_min)
        if filter.duration_max is not None:
            stmt = stmt.where(CourseBase.duration_hours <= filter.duration_max)

        # Has discount
        if filter.has_discount is True:
            stmt = stmt.where(CourseBase.discounted_cost.isnot(None))

        # Upcoming: courses with start_date in the future
        if filter.is_upcoming is True:
            stmt = stmt.where(CourseBase.start_date > func.now())

        # Sorting
        order_by_cols: list[ColumnElement[Any]] = []

        sort_col = cast(
            dict[CourseSortField, ColumnElement[Any]],
            {
                CourseSortField.TITLE: CourseBase.name,
                CourseSortField.PRICE: CourseBase.cost,
                CourseSortField.DURATION: CourseBase.duration_hours,
            },
        ).get(filter.sort_field, CourseBase.start_date)

        if filter.sort_order == CourseSortOrder.DESC:
            order_by_cols.append(sort_col.desc())
        else:
            order_by_cols.append(sort_col.asc())

        # Default ordering to keep stable results
        order_by_cols.append(CourseBase.start_date.asc().nulls_last())
        order_by_cols.append(CourseBase.duration_hours.asc())

        stmt = stmt.order_by(*order_by_cols)

        # Eager loading: используем contains_eager для joined relationships
        options_list = [
            joinedload(CourseBase.sections),
            joinedload(CourseBase.acquired_skills),
            joinedload(CourseBase.lecturers),
        ]

        # Для categories и tags используем contains_eager если они уже joined
        if categories_joined:
            options_list.append(contains_eager(CourseBase.categories))
        else:
            options_list.append(joinedload(CourseBase.categories))

        if tags_joined:
            options_list.append(contains_eager(CourseBase.tags))
        else:
            options_list.append(joinedload(CourseBase.tags))

        stmt = stmt.options(*options_list).offset(filter.skip).limit(filter.limit)

        models = await self.executor.execute_scalar_many(stmt)
        return [CourseReadMapper.to_read_model(model) for model in models]
