"""Course FastAPI controllers (CBV style)."""

from collections.abc import Sequence
from typing import Annotated
from uuid import UUID

from common.presentation.http.dto.response import IDResponse
from fastapi import APIRouter, Depends, Query, status
from fastapi_utils.cbv import cbv
from idp.identity.domain.value_objects.descriptor import IdentityDescriptor
from idp.identity.presentation.http.fastapi.auth import get_descriptor
from showcase.course.application.dtos.commands.create_course_command import (
    CreateCourseCommand,
    CreateCourseSectionDTO,
)
from showcase.course.application.dtos.commands.create_skill_command import (
    CreateSkillCommand,
)
from showcase.course.application.dtos.commands.create_tag_command import (
    CreateTagCommand,
)
from showcase.course.application.dtos.commands.enroll_user_command import (
    EnrollUserCommand,
)
from showcase.course.application.dtos.commands.update_course_command import (
    UpdateCourseCommand,
    UpdateCourseSectionDTO,
)
from showcase.course.application.dtos.commands.update_skill_command import (
    UpdateSkillCommand,
)
from showcase.course.application.dtos.commands.update_tag_command import (
    UpdateTagCommand,
)
from showcase.course.application.dtos.queries import (
    GetCourseByIdQuery,
    GetCoursesQuery,
    GetCoursesSearchQuery,
    GetSkillByIdQuery,
    GetSkillsQuery,
    GetTagByIdQuery,
    GetTagsQuery,
)
from showcase.course.application.interfaces.repositories.course_read_repository import (
    CoursesFilter,
)
from showcase.course.application.interfaces.services.recommendation_service import (
    GetRecommendationsDTO,
    IRecommendationService,
    RecommendationsDTO,
)
from showcase.course.application.interfaces.usecases.command.create_course_use_case import (
    ICreateCourseUseCase,
)
from showcase.course.application.interfaces.usecases.command.create_skill_use_case import (
    ICreateSkillUseCase,
)
from showcase.course.application.interfaces.usecases.command.create_tag_use_case import (
    ICreateTagUseCase,
)
from showcase.course.application.interfaces.usecases.command.delete_course_use_case import (
    IDeleteCourseUseCase,
)
from showcase.course.application.interfaces.usecases.command.delete_skill_use_case import (
    IDeleteSkillUseCase,
)
from showcase.course.application.interfaces.usecases.command.delete_tag_use_case import (
    IDeleteTagUseCase,
)
from showcase.course.application.interfaces.usecases.command.enroll_user_use_case import (
    IEnrollUserUseCase,
)
from showcase.course.application.interfaces.usecases.command.update_course_use_case import (
    IUpdateCourseUseCase,
)
from showcase.course.application.interfaces.usecases.command.update_skill_use_case import (
    IUpdateSkillUseCase,
)
from showcase.course.application.interfaces.usecases.command.update_tag_use_case import (
    IUpdateTagUseCase,
)
from showcase.course.application.interfaces.usecases.query import (
    IGetCourseByIdUseCase,
    IGetCoursesExtendedUseCase,
    IGetCoursesSearchUseCase,
    IGetCoursesUseCase,
    IGetSkillByIdUseCase,
    IGetSkillsUseCase,
    IGetTagByIdUseCase,
    IGetTagsUseCase,
)
from showcase.course.application.interfaces.usecases.query.list_enrollments_by_course_use_case import (
    IListEnrollmentsByCourseUseCase,
)
from showcase.course.application.read_models.course_read_model import CourseReadModel
from showcase.course.application.read_models.enrollment_read_model import (
    EnrollmentReadModel,
)
from showcase.course.application.read_models.skill_read_model import SkillReadModel
from showcase.course.application.read_models.tag_read_model import TagReadModel
from showcase.course.domain.value_objects import CourseStatus
from showcase.course.presentation.http.fastapi.dto.request import (
    CreateCourseRequest,
    CreateSkillRequest,
    CreateTagRequest,
    EnrollAuthenticatedRequest,
    EnrollRequest,
    UpdateCourseRequest,
    UpdateSkillRequest,
    UpdateTagRequest,
)


course_router = APIRouter(prefix="/courses", tags=["courses"])
skills_router = APIRouter(prefix="/skills", tags=["skills"])
tags_router = APIRouter(prefix="/tags", tags=["tags"])
recommendations_router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@cbv(course_router)
class CourseController:
    """Controller (CBV) for course endpoints using fastapi_utils.cbv."""

    get_courses_use_case: IGetCoursesUseCase = Depends()
    get_course_by_id_use_case: IGetCourseByIdUseCase = Depends()
    get_courses_search_use_case: IGetCoursesSearchUseCase = Depends()
    enroll_user_use_case: IEnrollUserUseCase = Depends()
    list_enrollments_use_case: IListEnrollmentsByCourseUseCase = Depends()
    create_course_use_case: ICreateCourseUseCase = Depends()
    update_course_use_case: IUpdateCourseUseCase = Depends()
    get_courses_extended_use_case: IGetCoursesExtendedUseCase = Depends()
    delete_course_use_case: IDeleteCourseUseCase = Depends()

    @course_router.get("/")
    async def list_courses(
        self,
        status: Annotated[CourseStatus | None, Query()] = None,
        is_published: Annotated[bool | None, Query()] = None,
        category_id: Annotated[UUID | None, Query()] = None,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=1000)] = 100,
    ) -> list[CourseReadModel]:
        """Get all courses with optional filters."""
        return await self.get_courses_use_case.execute(
            GetCoursesQuery(
                status=status,
                is_published=is_published,
                category_id=category_id,
                skip=skip,
                limit=limit,
            )
        )

    @course_router.get("/search")
    async def search(
        self,
        q: Annotated[str, Query(min_length=1)],
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=1000)] = 50,
    ) -> list[CourseReadModel]:
        """Full-text search for courses."""
        return await self.get_courses_search_use_case.execute(
            query=GetCoursesSearchQuery(query=q, skip=skip, limit=limit)
        )

    @course_router.get("/filter")
    async def filter_extended(self, filter: CoursesFilter) -> list[CourseReadModel]:
        """Filter endpoint for extended search."""
        return await self.get_courses_extended_use_case.execute(filter)

    @course_router.get("/{course_id}")
    async def get_course_by_id(self, course_id: UUID) -> CourseReadModel:
        """Get a course by ID."""
        return await self.get_course_by_id_use_case.execute(
            GetCourseByIdQuery(course_id=course_id)
        )

    @course_router.post("/")
    async def create_course(self, request: CreateCourseRequest) -> IDResponse:
        """Create a new course."""
        sections = [
            CreateCourseSectionDTO(
                name=s.name,
                description=s.description,
                order_num=s.order_num,
                hours=s.hours,
            )
            for s in request.sections
        ]
        command = CreateCourseCommand(
            name=request.name,
            description=request.description,
            format=request.format,
            education_format=request.education_format,
            certificate_type=request.certificate_type,
            cost=request.cost,
            discounted_cost=request.discounted_cost,
            duration_hours=request.duration_hours,
            start_date=request.start_date,
            end_date=request.end_date,
            status=request.status,
            is_published=request.is_published,
            locations=request.locations,
            sections=sections,
            tags=request.tags,
            acquired_skill_ids=request.acquired_skill_ids,
            category_ids=request.category_ids,
            lecturer_ids=request.lecturer_ids,
        )
        course_id = await self.create_course_use_case.execute(command)
        return IDResponse.from_uuid(course_id)

    @course_router.put("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def update_course(
        self, course_id: UUID, request: UpdateCourseRequest
    ) -> None:
        """Update an existing course."""
        sections = [
            UpdateCourseSectionDTO(
                name=s.name,
                description=s.description,
                order_num=s.order_num,
                hours=s.hours,
            )
            for s in request.sections
        ]
        command = UpdateCourseCommand(
            course_id=course_id,
            name=request.name,
            description=request.description,
            format=request.format,
            education_format=request.education_format,
            certificate_type=request.certificate_type,
            cost=request.cost,
            discounted_cost=request.discounted_cost,
            duration_hours=request.duration_hours,
            start_date=request.start_date,
            end_date=request.end_date,
            status=request.status,
            is_published=request.is_published,
            locations=request.locations,
            sections=sections,
            tags=request.tags,
            acquired_skill_ids=request.acquired_skill_ids,
            category_ids=request.category_ids,
            lecturer_ids=request.lecturer_ids,
        )
        await self.update_course_use_case.execute(command)

    @course_router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_course(self, course_id: UUID) -> None:
        """Delete a course."""
        await self.delete_course_use_case.execute(course_id)

    @course_router.post("/{course_id}/enrollments")
    async def enroll(self, course_id: UUID, request: EnrollRequest) -> IDResponse:
        """Enroll a user into a course (public endpoint)."""
        enrollment_id = await self.enroll_user_use_case.execute(
            EnrollUserCommand(
                course_id=course_id,
                email=request.email,
                full_name=request.full_name,
                phone=request.phone,
                message=request.message,
                user_id=None,
            )
        )
        return IDResponse.from_uuid(enrollment_id)

    @course_router.post("/{course_id}/enrollments/authenticated")
    async def enroll_authenticated(
        self,
        course_id: UUID,
        request: EnrollAuthenticatedRequest,
        descriptor: Annotated[IdentityDescriptor, Depends(get_descriptor)],
    ) -> IDResponse:
        """Enroll a user into a course (public endpoint)."""
        enrollment_id = await self.enroll_user_use_case.execute(
            EnrollUserCommand(
                course_id=course_id,
                email=descriptor.username,
                full_name=request.full_name,
                phone=request.phone,
                message=request.message,
                user_id=descriptor.identity_id,
            )
        )
        return IDResponse.from_uuid(enrollment_id)

    @course_router.get("/{course_id}/enrollments")
    async def list_enrollments(
        self,
        course_id: UUID,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=1000)] = 100,
    ) -> Sequence[EnrollmentReadModel]:
        """List enrollments for a course (admin use)."""
        return await self.list_enrollments_use_case.execute(
            course_id=course_id, skip=skip, limit=limit
        )


@cbv(skills_router)
class SkillController:
    """Controller (CBV) for skill endpoints using fastapi_utils.cbv."""

    get_skills_use_case: IGetSkillsUseCase = Depends()
    get_skill_by_id_use_case: IGetSkillByIdUseCase = Depends()
    create_skill_use_case: ICreateSkillUseCase = Depends()
    update_skill_use_case: IUpdateSkillUseCase = Depends()
    delete_skill_use_case: IDeleteSkillUseCase = Depends()

    @skills_router.get("/")
    async def list_skills(
        self,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=1000)] = 100,
    ) -> list[SkillReadModel]:
        """Get all skills."""
        query = GetSkillsQuery(skip=skip, limit=limit)
        return await self.get_skills_use_case.execute(query)

    @skills_router.get("/{skill_id}")
    async def get_skill_by_id(self, skill_id: UUID) -> SkillReadModel:
        """Get a skill by ID."""
        query = GetSkillByIdQuery(skill_id=skill_id)
        return await self.get_skill_by_id_use_case.execute(query)

    @skills_router.post("/")
    async def create_skill(self, request: CreateSkillRequest) -> IDResponse:
        """Create a new skill."""
        command = CreateSkillCommand(
            name=request.name,
            description=request.description,
        )
        skill_id = await self.create_skill_use_case.execute(command)
        return IDResponse.from_uuid(skill_id)

    @skills_router.put("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def update_skill(self, skill_id: UUID, request: UpdateSkillRequest) -> None:
        """Update an existing skill."""
        command = UpdateSkillCommand(
            skill_id=skill_id,
            name=request.name,
            description=request.description,
        )
        await self.update_skill_use_case.execute(command)

    @skills_router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_skill(self, skill_id: UUID) -> None:
        await self.delete_skill_use_case.execute(skill_id)


@cbv(tags_router)
class TagController:
    """Controller (CBV) for tag endpoints using fastapi_utils.cbv."""

    get_tags_use_case: IGetTagsUseCase = Depends()
    get_tag_by_id_use_case: IGetTagByIdUseCase = Depends()
    create_tag_use_case: ICreateTagUseCase = Depends()
    update_tag_use_case: IUpdateTagUseCase = Depends()
    delete_tag_use_case: IDeleteTagUseCase = Depends()

    @tags_router.get("/")
    async def list_tags(
        self,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=1000)] = 100,
    ) -> list[TagReadModel]:
        """Get all tags."""
        query = GetTagsQuery(skip=skip, limit=limit)
        return await self.get_tags_use_case.execute(query)

    @tags_router.get("/{tag_id}")
    async def get_tag_by_id(self, tag_id: UUID) -> TagReadModel:
        """Get a tag by ID."""
        query = GetTagByIdQuery(tag_id=tag_id)
        return await self.get_tag_by_id_use_case.execute(query)

    @tags_router.post("/")
    async def create_tag(self, request: CreateTagRequest) -> IDResponse:
        """Create a new tag."""
        command = CreateTagCommand(name=request.name)
        tag_id = await self.create_tag_use_case.execute(command)
        return IDResponse.from_uuid(tag_id)

    @tags_router.put("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def update_tag(self, tag_id: UUID, request: UpdateTagRequest) -> None:
        """Update an existing tag."""
        command = UpdateTagCommand(tag_id=tag_id, name=request.name)
        await self.update_tag_use_case.execute(command)

    @tags_router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_tag(self, tag_id: UUID) -> None:
        await self.delete_tag_use_case.execute(tag_id)


@cbv(recommendations_router)
class RecommendationController:
    service: IRecommendationService = Depends()

    @recommendations_router.get("/")
    async def recommend_courses(
        self,
        q: Annotated[str, Query(min_length=1)],
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=25)] = 10,
    ) -> RecommendationsDTO:
        """Get courses recommendation by query."""
        return await self.service.recommend(
            GetRecommendationsDTO(query=q, skip=skip, limit=limit)
        )
