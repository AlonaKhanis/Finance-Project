"""Add first and last name , email is unique

Revision ID: 37d29ed8d2de
Revises: c47c13f6b798
Create Date: 2024-11-02 15:13:53.454109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37d29ed8d2de'
down_revision = 'c47c13f6b798'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add columns with a default value to avoid integrity errors
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.String(), nullable=False, server_default=''))
        batch_op.add_column(sa.Column('last_name', sa.String(), nullable=False, server_default=''))
        batch_op.create_unique_constraint('uq_users_email', ['email'])
        batch_op.drop_column('username')

    # Remove the server default after the columns have been populated
    op.alter_column('users', 'first_name', server_default=None)
    op.alter_column('users', 'last_name', server_default=None)


def downgrade() -> None:
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.VARCHAR(), nullable=False))
        batch_op.drop_constraint('uq_users_email', type_='unique')
        batch_op.drop_column('last_name')
        batch_op.drop_column('first_name')
