from uuid import UUID

from common.domain.interfaces.uuid_generator import IUUIDGenerator
from showcase.course.application.dtos.commands.create_course_command import (
    CreateCourseCommand,
)
from showcase.course.application.interfaces.repositories.course_repository import (
    ICourseRepository,
)
from showcase.course.application.interfaces.repositories.tag_repository import (
    ITagRepository,
)
from showcase.course.application.interfaces.usecases.command.create_course_use_case import (
    ICreateCourseUseCase,
)
from showcase.course.domain.entities.course import Course, CourseSection
from showcase.course.domain.entities.tag import Tag


class CreateCourseUseCase(ICreateCourseUseCase):
    def __init__(
        self,
        course_repository: ICourseRepository,
        uuid_generator: IUUIDGenerator,
        tag_repository: ITagRepository,
    ) -> None:
        self.uuid_generator = uuid_generator
        self.course_repository = course_repository
        self.tag_repository = tag_repository

    async def execute(self, command: CreateCourseCommand) -> UUID:
        # Map CreateCourseSectionDTO to domain CourseSection objects
        sections: list[CourseSection] = []
        if command.sections:
            sections = [
                CourseSection(
                    section_id=self.uuid_generator.create(),
                    name=sec.name,
                    description=sec.description,
                    order_num=sec.order_num,
                    hours=sec.hours,
                )
                for sec in command.sections
            ]

        tag_ids: list[UUID] = []
        if command.tags:
            existing_tags = await self.tag_repository.get_by_values(command.tags)
            existing_values = {t.value for t in existing_tags}

            new_tags: list[Tag] = []
            for v in command.tags:
                if v in existing_values:
                    continue
                new_tags.append(Tag(tag_id=self.uuid_generator.create(), value=v))

            await self.tag_repository.add_all(new_tags)

            tag_ids = [t.tag_id for t in [*existing_tags, *new_tags]]

        course = Course(
            course_id=self.uuid_generator.create(),
            name=command.name,
            description=command.description,
            format=command.format,
            duration_hours=command.duration_hours,
            cost=command.cost,
            discounted_cost=command.discounted_cost,
            start_date=command.start_date,
            certificate_type=command.certificate_type,
            status=command.status,
            is_published=command.is_published,
            sections=sections,
            category_ids=command.category_ids or [],
            tag_ids=tag_ids,
            acquired_skill_ids=command.acquired_skill_ids or [],
            lecturer_ids=command.lecturer_ids or [],
        )
        await self.course_repository.add(course)
        return course.course_id
