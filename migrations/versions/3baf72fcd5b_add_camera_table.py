"""add camera table

Revision ID: 3baf72fcd5b
Revises: 467f350b6905
Create Date: 2016-03-03 16:59:40.263178

"""

# revision identifiers, used by Alembic.
revision = '3baf72fcd5b'
down_revision = '467f350b6905'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cameras',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cameraName', sa.String(length=10), nullable=True),
    sa.Column('resolution', sa.Enum('low', 'medium', 'high'), nullable=True),
    sa.Column('vflip', sa.Boolean(), nullable=True),
    sa.Column('hflip', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_cameras_cameraName', 'cameras', ['cameraName'], unique=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_cameras_cameraName', 'cameras')
    op.drop_table('cameras')
    ### end Alembic commands ###
