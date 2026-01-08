from showcase.course.application.read_models.enrollment_read_model import (
    EnrollmentReadModel,
)
from showcase.course.domain.entities.enrollment import Enrollment
from showcase.course.infrastructure.database.postgres.sqlalchemy.models.enrollment import (
    EnrollmentBase,
)


class EnrollmentMapper:
    @staticmethod
    def to_read_model(model: EnrollmentBase) -> EnrollmentReadModel:
        return EnrollmentReadModel(
            enrollment_id=model.enrollment_id,
            course_id=model.course_id,
            email=model.email,
            full_name=model.full_name,
            phone=model.phone,
            message=model.message,
            user_id=model.user_id,
            created_at=model.created_at,
        )

    @staticmethod
    def to_persistence(entity: Enrollment) -> EnrollmentBase:
        return EnrollmentBase(
            enrollment_id=entity.enrollment_id,
            course_id=entity.course_id,
            email=entity.email.value,
            full_name=entity.full_name,
            phone=entity.phone.value if entity.phone is not None else None,
            message=entity.message,
            user_id=entity.user_id,
            created_at=entity.created_at.value,
        )
