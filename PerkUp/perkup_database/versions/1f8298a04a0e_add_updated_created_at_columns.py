"""Add updated/created at columns

Revision ID: 1f8298a04a0e
Revises: 7486d3048d29
Create Date: 2017-01-22 15:39:58.500628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f8298a04a0e'
down_revision = '7486d3048d29'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('organization', sa.Column('created_at', sa.DateTime()))
    op.add_column('organization', sa.Column('updated_at', sa.DateTime()))
    op.add_column('datasource', sa.Column('created_at', sa.DateTime()))
    op.add_column('datasource', sa.Column('updated_at', sa.DateTime()))
    op.add_column('user', sa.Column('created_at', sa.DateTime()))
    op.add_column('user', sa.Column('updated_at', sa.DateTime()))


def downgrade():
    op.drop_column('organization', 'created_at')
    op.drop_column('organization', 'updated_at')
    op.drop_column('datasource', 'created_at')
    op.drop_column('datasource', 'updated_at')
    op.drop_column('user', 'created_at')
    op.drop_column('user', 'updated_at')
