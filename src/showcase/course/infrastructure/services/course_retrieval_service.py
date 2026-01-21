"""Course retrieval: filtering by inferred params and fallback to shuffled catalog."""

import logging
import random

from showcase.course.application.interfaces.repositories.course_read_repository import (
    ICourseReadRepository,
    SimpleCoursesFilter,
)
from showcase.course.application.read_models.course_read_model import CourseReadModel

from .filter_inference_service import CourseFilterLLM


class CourseRetrievalService:
    """Fetches courses by inferred filter or provides fallback list."""

    def __init__(
        self,
        logger: logging.Logger,
        course_repository: ICourseReadRepository,
    ) -> None:
        self._logger = logger
        self._course_repository = course_repository

    async def filter_by_inference(
        self,
        filter_llm: CourseFilterLLM,
        available_category_names: set[str],
        limit: int,
        skip: int,
    ) -> list[CourseReadModel]:
        """Apply inferred filter and return courses.

        Return None if the query is indecisive or has no filter params (then use fallback).
        """
        if not filter_llm.is_decisive:
            self._logger.debug(
                "Skipping filter: indecisive query",
                extra={"service": "CourseRetrieval"},
            )
            return []

        has_params = (
            filter_llm.category_names
            or filter_llm.format
            or filter_llm.max_duration_hours
            or filter_llm.certificate_required
        )
        if not has_params:
            self._logger.debug(
                "Skipping filter: no filter params inferred",
                extra={"service": "CourseRetrieval"},
            )
            return []

        validated_categories = [
            c
            for c in (filter_llm.category_names or [])
            if c in available_category_names
        ]
        if filter_llm.category_names and not validated_categories:
            self._logger.warning(
                "All inferred categories invalid, using none",
                extra={
                    "service": "CourseRetrieval",
                    "inferred": filter_llm.category_names,
                    "available_count": len(available_category_names),
                },
            )

        simple_filter = SimpleCoursesFilter(
            categories=(
                validated_categories if filter_llm.category_names is not None else None
            ),
            format=filter_llm.format,
            max_duration_hours=filter_llm.max_duration_hours,
            certificate_required=filter_llm.certificate_required,
            limit=limit,
            skip=skip,
        )

        self._logger.info(
            "Filtering courses by inferred params",
            extra={
                "service": "CourseRetrieval",
                "categories": simple_filter.categories,
                "format": simple_filter.format.value if simple_filter.format else None,
                "max_duration_hours": simple_filter.max_duration_hours,
                "certificate_required": simple_filter.certificate_required,
                "limit": limit,
                "skip": skip,
            },
        )

        courses = await self._course_repository.filter(simple_filter)

        self._logger.info(
            "Filtered courses fetched",
            extra={
                "service": "CourseRetrieval",
                "count": len(courses),
                "course_ids": [str(c.course_id) for c in courses],
            },
        )

        return courses

    async def get_fallback_courses(self, limit: int) -> list[CourseReadModel]:
        """Return courses for fallback path: get_all + shuffle."""
        self._logger.info(
            "Fetching fallback courses (get_all + shuffle)",
            extra={"service": "CourseRetrieval", "limit": limit},
        )

        courses = await self._course_repository.get_all(limit=limit)
        rng = random.Random()
        rng.shuffle(courses)

        self._logger.info(
            "Fallback courses ready",
            extra={
                "service": "CourseRetrieval",
                "count": len(courses),
                "course_ids": [str(c.course_id) for c in courses],
            },
        )

        return courses
