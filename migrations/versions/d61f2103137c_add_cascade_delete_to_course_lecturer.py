"""add cascade delete to course lecturer

Revision ID: d61f2103137c
Revises: 4ef06b131b1f
Create Date: 2026-01-12 16:23:21.801546

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd61f2103137c'
down_revision: Union[str, Sequence[str], None] = '4ef06b131b1f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        'course_lecturers_course_id_fkey',
        'course_lecturers',
        type_='foreignkey'
    )

    op.create_foreign_key(
        'course_lecturers_course_id_fkey',
        'course_lecturers',
        'courses',
        ['course_id'],
        ['course_id'],
        ondelete='CASCADE'
    )

def downgrade() -> None:
    op.drop_constraint(
        'course_lecturers_course_id_fkey',
        'course_lecturers',
        type_='foreignkey'
    )

    op.create_foreign_key(
        'course_lecturers_course_id_fkey',
        'course_lecturers',
        'courses',
        ['course_id'],
        ['course_id']
    )