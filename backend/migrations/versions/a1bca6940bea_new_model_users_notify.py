"""new model users_notify

Revision ID: a1bca6940bea
Revises: e2af2cafa5a2
Create Date: 2025-07-07 15:17:41.579387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1bca6940bea'
down_revision: Union[str, Sequence[str], None] = 'e2af2cafa5a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_notify',
    sa.Column('notify_id', sa.UUID(), nullable=False),
    sa.Column('user_uuid', sa.UUID(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('is_read', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['user_uuid'], ['users.uuid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('notify_id')
    )
    op.create_index('idx_notify_user_uuid', 'users_notify', ['user_uuid'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_notify_user_uuid', table_name='users_notify')
    op.drop_table('users_notify')
    # ### end Alembic commands ###
