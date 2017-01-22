"""Create organization table

Revision ID: 8f9d0a9594bf
Revises: 
Create Date: 2017-01-21 14:37:30.942610

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f9d0a9594bf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
    	'organization',
	    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
	    sa.Column('name', sa.String(50)),
	    sa.Column('logo', sa.String(100)),
	    sa.Column('address', sa.String(100)),
	    sa.Column('unique_domain', sa.String(50)),
	    sa.Column('lat_lang', sa.String(50))
    )

def downgrade():
    op.drop_table('organization')