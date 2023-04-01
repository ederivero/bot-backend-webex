"""initial migration

Revision ID: 78be3c9cd52d
Revises: 
Create Date: 2023-03-31 22:25:52.976951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78be3c9cd52d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groups',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('channel', sa.String(), nullable=False),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('channel')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('groups')
    # ### end Alembic commands ###
