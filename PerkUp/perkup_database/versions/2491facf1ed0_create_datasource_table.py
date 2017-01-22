"""Create Datasource table

Revision ID: 2491facf1ed0
Revises: 8f9d0a9594bf
Create Date: 2017-01-22 11:27:32.196328

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey


# revision identifiers, used by Alembic.
revision = '2491facf1ed0'
down_revision = '8f9d0a9594bf'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
    	'datasource',
	    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
	    sa.Column('name', sa.String(200)),
	    sa.Column('host', sa.String(200)),
	    sa.Column('port', sa.Integer),
	    sa.Column('user', sa.String(200)),
	    sa.Column('schema', sa.String(200)),
	    sa.Column('password', sa.String(200)),
	    sa.Column('type', sa.Enum(
	        'Firebird',
	        'Microsoft SQL Server',
	        'MySQL',
	        'Oracle',
	        'PostgreSQL',
	        'Sybase',
	        name='type')),
	    sa.Column('ssh_server', sa.String(200)),
	    sa.Column('ssh_port', sa.String(6)),
	    sa.Column('ssh_user', sa.String(200)),
	    sa.Column('ssh_password', sa.String(200)),
	    sa.Column('ssh_key_pub', sa.Text),
	    sa.Column('ssh_key_pass_phrase', sa.String(200)),
	    #Foreign key
	    sa.Column('organization_id', sa.Integer, ForeignKey('organization.id')),
    )


def downgrade():
    op.drop_table('datasource')
