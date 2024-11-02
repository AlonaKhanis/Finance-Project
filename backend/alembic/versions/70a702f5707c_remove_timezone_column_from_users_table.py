"""Remove timezone column from users table

Revision ID: 70a702f5707c
Revises: a5cfbf9cdf76
Create Date: 2024-11-02 14:12:27.950396

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision = '70a702f5707c'
down_revision = 'a5cfbf9cdf76'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Check if the 'timezone' column exists before attempting to drop it
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    columns = [col['name'] for col in inspector.get_columns('users')]
    if 'timezone' in columns:
        op.drop_column('users', 'timezone')


def downgrade() -> None:
    # Add the 'timezone' column back in the downgrade
    op.add_column('users', sa.Column('timezone', sa.String(), nullable=True))