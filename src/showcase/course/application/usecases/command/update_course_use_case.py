from uuid import UUID

from common.domain.interfaces.uuid_generator import IUUIDGenerator
from showcase.course.application.dtos.commands.update_course_command import (
    UpdateCourseCommand,
)
from showcase.course.application.interfaces.repositories.course_repository import (
    ICourseRepository,
)
from showcase.course.application.interfaces.repositories.tag_repository import (
    ITagRepository,
)
from showcase.course.application.interfaces.usecases.command.update_course_use_case import (
    IUpdateCourseUseCase,
)
from showcase.course.domain.entities.course import CourseSection
from showcase.course.domain.entities.tag import Tag


class UpdateCourseUseCase(IUpdateCourseUseCase):
    def __init__(
        self,
        course_repository: ICourseRepository,
        uuid_generator: IUUIDGenerator,
        tag_repository: ITagRepository,
    ) -> None:
        self.course_repository = course_repository
        self.uuid_generator = uuid_generator
        self.tag_repository = tag_repository

    async def execute(self, command: UpdateCourseCommand) -> UUID:
        course = await self.course_repository.get_by_id(command.course_id)

        # Apply updates
        if command.name is not None:
            course.name = command.name
        if command.description is not None:
            course.description = command.description
        if command.format is not None:
            course.format = command.format
        if command.duration_hours is not None:
            course.duration_hours = command.duration_hours
        if command.cost is not None:
            course.cost = command.cost
        if command.discounted_cost is not None:
            course.discounted_cost = command.discounted_cost
        if command.start_date is not None:
            course.start_date = command.start_date
        if command.certificate_type is not None:
            course.certificate_type = command.certificate_type
        if command.status is not None:
            course.status = command.status
        if command.is_published is not None:
            course.is_published = command.is_published
        if command.sections is not None:
            # Map UpdateCourseSectionDTO to domain CourseSection objects
            # For updates: use provided section_id if available, else generate new
            updated_sections: list[CourseSection] = []
            for sec_dto in command.sections:
                # If section_id is provided (existing section), use it; otherwise generate new
                section_id = sec_dto.section_id or self.uuid_generator.create()
                existing_section = next(
                    (s for s in course.sections if s.section_id == section_id), None
                )

                # Use existing values if not provided in DTO
                name = (
                    sec_dto.name
                    if sec_dto.name is not None
                    else (existing_section.name if existing_section else "")
                )
                description = (
                    sec_dto.description
                    if sec_dto.description is not None
                    else (existing_section.description if existing_section else None)
                )
                order_num = (
                    sec_dto.order_num
                    if sec_dto.order_num is not None
                    else (existing_section.order_num if existing_section else 0)
                )
                hours = (
                    sec_dto.hours
                    if sec_dto.hours is not None
                    else (existing_section.hours if existing_section else None)
                )

                updated_sections.append(
                    CourseSection(
                        section_id=section_id,
                        name=name,
                        description=description,
                        order_num=order_num,
                        hours=hours,
                    )
                )
            course.sections = updated_sections
        if command.category_ids is not None:
            course.category_ids = command.category_ids

        if command.acquired_skill_ids is not None:
            course.acquired_skill_ids = command.acquired_skill_ids
        if command.lecturer_ids is not None:
            course.lecturer_ids = command.lecturer_ids

        if command.tags is not None:
            existing_tags = await self.tag_repository.get_by_values(command.tags)
            existing_values = {t.value for t in existing_tags}

            new_tags: list[Tag] = []
            for v in command.tags:
                if v in existing_values:
                    continue
                new_tags.append(Tag(tag_id=self.uuid_generator.create(), value=v))

            await self.tag_repository.add_all(new_tags)

            course.tag_ids = [t.tag_id for t in [*existing_tags, *new_tags]]

        await self.course_repository.update(course)
        return command.course_id
