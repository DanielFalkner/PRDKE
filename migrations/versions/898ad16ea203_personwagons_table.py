"""personwagons table

Revision ID: 898ad16ea203
Revises: 6df328274315
Create Date: 2021-12-22 12:56:52.947878

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '898ad16ea203'
down_revision = '6df328274315'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('personwagon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('seats', sa.Integer(), nullable=False),
    sa.Column('max_weight', sa.Integer(), nullable=False),
    sa.Column('width', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('personwagon')
    # ### end Alembic commands ###