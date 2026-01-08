"""Course read mapper implementation."""

from showcase.category.infrastructure.database.postgres.sqlalchemy.mappers import (
    CategoryReadMapper,
)
from showcase.course.application.read_models.course_read_model import (
    CourseReadModel,
    CourseSectionReadModel,
)
from showcase.course.infrastructure.database.postgres.sqlalchemy.mappers.skill_mapper import (
    SkillReadMapper,
)
from showcase.course.infrastructure.database.postgres.sqlalchemy.models import (
    CourseBase,
    CourseSectionBase,
)
from showcase.lecturer.infrastructure.database.postgres.sqlalchemy.mappers import (
    LecturerReadMapper,
)


class CourseReadMapper:
    """Maps ORM models to read models."""

    @staticmethod
    def section_to_read_model(model: CourseSectionBase) -> CourseSectionReadModel:
        """Map section ORM model to read model."""
        return CourseSectionReadModel(
            section_id=model.section_id,
            name=model.name,
            description=model.description,
            order_num=model.order_num,
            hours=model.hours,
        )

    @staticmethod
    def to_read_model(model: CourseBase) -> CourseReadModel:
        """Map ORM model to read model with enriched nested objects."""
        sections = [
            CourseReadMapper.section_to_read_model(section)
            for section in model.sections
        ]
        categories = [CategoryReadMapper.to_read_model(cat) for cat in model.categories]
        tags = [tag.name for tag in model.tags]
        skills = [
            SkillReadMapper.to_read_model(skill) for skill in model.acquired_skills
        ]
        lecturers = [
            LecturerReadMapper.to_read_model(lecturer) for lecturer in model.lecturers
        ]

        return CourseReadModel(
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
            categories=categories,
            tags=tags,
            acquired_skills=skills,
            lecturers=lecturers,
            sections=sections,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
