"""Create datasources-tables table

Revision ID: 8cf92979bf8d
Revises: 1f8298a04a0e
Create Date: 2017-01-25 07:43:48.850235

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey


# revision identifiers, used by Alembic.
revision = '8cf92979bf8d'
down_revision = '1f8298a04a0e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
    	'datasource_table',
	    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
	    sa.Column('table_name', sa.Text),
	    sa.Column('table_structure', sa.Text),
	    sa.Column('serialized_table', sa.Text),
	    sa.Column('created_at', sa.DateTime()),
	    sa.Column('updated_at', sa.DateTime()),
	    #Foreign key
	    sa.Column('datasource_id', sa.Integer, ForeignKey('datasource.id')),
    )


def downgrade():
    op.drop_table('datasource_table')
