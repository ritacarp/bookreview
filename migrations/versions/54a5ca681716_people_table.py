"""people table

Revision ID: 54a5ca681716
Revises: 5f1bd77222a3
Create Date: 2020-06-23 18:02:52.471346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54a5ca681716'
down_revision = '5f1bd77222a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('people', 'comments',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('people', 'hash',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('people', 'hash',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('people', 'comments',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
