"""update search_vector for all courses

Revision ID: 0ebab11ac41b
Revises: d61f2103137c
Create Date: 2026-01-17 11:15:42.374815

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import func, literal_column, text
from sqlalchemy.dialects.postgresql import TSVECTOR


# revision identifiers, used by Alembic.
revision: str = "0ebab11ac41b"
down_revision: Union[str, Sequence[str], None] = "d61f2103137c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    conn = op.get_bind()

    # Tables
    course_table = sa.table(
        "courses",
        sa.column("course_id", sa.UUID),
        sa.column("name", sa.Text),
        sa.column("description", sa.Text),
        sa.column("search_vector", TSVECTOR),
    )

    course_section_table = sa.table(
        "course_sections",
        sa.column("course_id", sa.UUID),
        sa.column("name", sa.Text),
        sa.column("description", sa.Text),
    )

    course_skill_table = sa.table(
        "course_skills",
        sa.column("course_id", sa.UUID),
        sa.column("skill_id", sa.UUID),
    )

    skill_table = sa.table(
        "skills",
        sa.column("skill_id", sa.UUID),
        sa.column("name", sa.Text),
        sa.column("description", sa.Text),
    )

    # CTE: aggregated sections text
    sections_cte = (
        sa.select(
            course_section_table.c.course_id,
            func.coalesce(
                func.string_agg(
                    func.concat_ws(
                        " ",
                        course_section_table.c.name,
                        course_section_table.c.description,
                    ),
                    " ",
                ),
                "",
            ).label("sections_text"),
        )
        .group_by(course_section_table.c.course_id)
        .cte("sections_cte")
    )

    # CTE: aggregated skills text
    skills_cte = (
        sa.select(
            course_skill_table.c.course_id,
            func.coalesce(
                func.string_agg(
                    func.concat_ws(
                        " ",
                        skill_table.c.name,
                        skill_table.c.description,
                    ),
                    " ",
                ),
                "",
            ).label("skills_text"),
        )
        .select_from(
            course_skill_table.join(
                skill_table,
                course_skill_table.c.skill_id == skill_table.c.skill_id,
            )
        )
        .group_by(course_skill_table.c.course_id)
        .cte("skills_cte")
    )

    # correlated subqueries (LEFT JOIN semantics)
    sections_text_subq = (
        sa.select(sections_cte.c.sections_text)
        .where(sections_cte.c.course_id == course_table.c.course_id)
        .scalar_subquery()
    )

    skills_text_subq = (
        sa.select(skills_cte.c.skills_text)
        .where(skills_cte.c.course_id == course_table.c.course_id)
        .scalar_subquery()
    )

    # UPDATE all courses (idempotent)
    stmt = (
        sa.update(course_table)
        .values(
            search_vector=(
                func.setweight(
                    func.to_tsvector("russian", func.coalesce(course_table.c.name, "")),
                    literal_column("'A'"),
                )
                .op("||")(
                    func.setweight(
                        func.to_tsvector(
                            "russian", func.coalesce(course_table.c.description, "")
                        ),
                        literal_column("'B'"),
                    )
                )
                .op("||")(
                    func.setweight(
                        func.to_tsvector(
                            "russian",
                            func.coalesce(sections_text_subq, ""),
                        ),
                        literal_column("'C'"),
                    )
                )
                .op("||")(
                    func.setweight(
                        func.to_tsvector(
                            "russian",
                            func.coalesce(skills_text_subq, ""),
                        ),
                        literal_column("'D'"),
                    )
                )
            )
        )
        .execution_options(synchronize_session=False)
        .add_cte(sections_cte)
        .add_cte(skills_cte)
    )

    conn.execute(stmt)


def downgrade():
    conn = op.get_bind()
    course_table = sa.table("courses", sa.column("search_vector", TSVECTOR))
    conn.execute(sa.update(course_table).values(search_vector=text("''::tsvector")))
