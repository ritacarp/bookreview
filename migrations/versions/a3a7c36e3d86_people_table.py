"""people table

Revision ID: a3a7c36e3d86
Revises: 4ea76d5faa43
Create Date: 2020-07-05 13:08:18.035567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3a7c36e3d86'
down_revision = '4ea76d5faa43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('people', sa.Column('first_name', sa.String(), nullable=True))
    op.add_column('people', sa.Column('last_name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('people', 'last_name')
    op.drop_column('people', 'first_name')
    # ### end Alembic commands ###