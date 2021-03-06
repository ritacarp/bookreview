"""books table

Revision ID: 83660dba68af
Revises: c7d2586dfaa2
Create Date: 2020-06-25 21:41:14.048414

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83660dba68af'
down_revision = 'c7d2586dfaa2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('amazon_lookup_id', sa.String(), nullable=True))
    op.drop_column('books', 'lookup_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('lookup_id', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('books', 'amazon_lookup_id')
    # ### end Alembic commands ###
