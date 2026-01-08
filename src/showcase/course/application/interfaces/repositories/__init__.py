"""Course repository interfaces."""

from .course_read_repository import ICourseReadRepository
from .enrollment_repository import IEnrollmentRepository
from .skill_read_repository import ISkillReadRepository
from .tag_read_repository import ITagReadRepository


__all__ = [
    "ICourseReadRepository",
    "IEnrollmentRepository",
    "ISkillReadRepository",
    "ITagReadRepository",
]
