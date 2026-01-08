"""Course write repository implementation."""

from uuid import UUID

from common.infrastructure.database.postgres.sqlalchemy.executor import QueryExecutor
from showcase.course.application.interfaces.repositories.course_repository import (
    ICourseRepository,
)
from showcase.course.domain.entities.course import Course, CourseSection
from showcase.course.infrastructure.database.postgres.sqlalchemy.models.course import (
    CourseBase,
    CourseCategoryBase,
    CourseLecturerBase,
    CourseSectionBase,
    CourseSkillBase,
    CourseTagBase,
)
from sqlalchemy import delete, select
from sqlalchemy.orm import joinedload


class CourseRepository(ICourseRepository):
    """Write repository for courses."""

    def __init__(self, executor: QueryExecutor) -> None:
        self.executor = executor

    async def get_by_id(self, course_id: UUID) -> Course:
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
        return self._to_domain(model)

    async def add(self, course: Course) -> None:
        """Add a new course."""
        model = self._to_persistence(course)
        await self.executor.add(model)
        await self._add(course)

    async def delete(self, course_id: UUID) -> None:
        """Delete a course and its associations by ID."""
        # Finally delete the course record
        await self.executor.execute(
            delete(CourseBase).where(CourseBase.course_id == course_id)
        )

    async def update(self, course: Course) -> None:
        """Update an existing course."""
        model = self._to_persistence(course)

        # Delete all associations before update
        await self.executor.execute(
            delete(CourseSectionBase).where(
                CourseSectionBase.course_id == course.course_id
            )
        )
        await self.executor.execute(
            delete(CourseCategoryBase).where(
                CourseCategoryBase.course_id == course.course_id
            )
        )
        await self.executor.execute(
            delete(CourseTagBase).where(CourseTagBase.course_id == course.course_id)
        )
        await self.executor.execute(
            delete(CourseSkillBase).where(CourseSkillBase.course_id == course.course_id)
        )
        await self.executor.execute(
            delete(CourseLecturerBase).where(
                CourseLecturerBase.course_id == course.course_id
            )
        )
        await self.executor.save(model)
        await self._add(course)

    async def _add(self, course: Course) -> None:
        """Add sections and associations for course."""
        # Add sections
        await self.executor.add_all(
            [
                CourseSectionBase(
                    section_id=sec.section_id,
                    course_id=course.course_id,
                    name=sec.name,
                    description=sec.description,
                    order_num=sec.order_num,
                    hours=sec.hours,
                )
                for sec in course.sections
            ]
        )
        # Add category associations
        await self.executor.add_all(
            [
                CourseCategoryBase(course_id=course.course_id, category_id=cid)
                for cid in course.category_ids
            ]
        )
        # Add tag associations
        await self.executor.add_all(
            [
                CourseTagBase(course_id=course.course_id, tag_id=tid)
                for tid in course.tag_ids
            ]
        )
        # Add skill associations
        await self.executor.add_all(
            [
                CourseSkillBase(course_id=course.course_id, skill_id=sid)
                for sid in course.acquired_skill_ids
            ]
        )
        # Add lecturer associations
        await self.executor.add_all(
            [
                CourseLecturerBase(course_id=course.course_id, lecturer_id=lid)
                for lid in course.lecturer_ids
            ]
        )

    @staticmethod
    def _to_domain(model: CourseBase) -> Course:
        """Map ORM model to domain entity."""
        # Map sections from ORM to domain CourseSection objects
        sections = [
            CourseSection(
                section_id=sec.section_id,
                name=sec.name,
                description=sec.description,
                order_num=sec.order_num,
                hours=sec.hours,
            )
            for sec in model.sections
        ]

        return Course(
            course_id=model.course_id,
            name=model.name,
            description=model.description,
            format=model.format,
            duration_hours=model.duration_hours,
            cost=model.cost,
            discounted_cost=model.discounted_cost,
            start_date=model.start_date,
            certificate_type=model.certificate_type,
            status=model.status,
            is_published=model.is_published,
            sections=sections,
            category_ids=[cat.category_id for cat in model.categories],
            tag_ids=[tag.tag_id for tag in model.tags],
            acquired_skill_ids=[skill.skill_id for skill in model.acquired_skills],
            lecturer_ids=[lec.lecturer_id for lec in model.lecturers],
        )

    @staticmethod
    def _to_persistence(entity: Course) -> CourseBase:
        """Map domain entity to ORM model."""
        return CourseBase(
            course_id=entity.course_id,
            name=entity.name,
            description=entity.description,
            format=entity.format,
            duration_hours=entity.duration_hours,
            cost=entity.cost,
            discounted_cost=entity.discounted_cost,
            start_date=entity.start_date,
            certificate_type=entity.certificate_type,
            status=entity.status,
            is_published=entity.is_published,
        )
