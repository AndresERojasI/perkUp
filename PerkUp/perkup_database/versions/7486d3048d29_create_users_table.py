"""Create Users table

Revision ID: 7486d3048d29
Revises: 2491facf1ed0
Create Date: 2017-01-22 11:36:17.375367

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey


# revision identifiers, used by Alembic.
revision = '7486d3048d29'
down_revision = '2491facf1ed0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
    	'user',
	    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
	    sa.Column('name', sa.String(50)),
	    sa.Column('last_name', sa.String(50)),
	    sa.Column('email', sa.String(100)),
	    sa.Column('password', sa.String(100)),
	    sa.Column('username', sa.String(50)),
	    sa.Column('avatar', sa.String(100)),
	    #Foreign key
	    sa.Column('organization_id', sa.Integer, ForeignKey('organization.id'))
    )


def downgrade():
    op.create_table('user')
