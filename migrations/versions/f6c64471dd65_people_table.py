"""people table

Revision ID: f6c64471dd65
Revises: 
Create Date: 2020-06-19 08:31:10.357486

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f6c64471dd65'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('people')
    op.drop_table('books')
    op.drop_table('book_reviews')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book_reviews',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('people_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('book_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('review', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], name='book_reviews_book_id_fkey'),
    sa.ForeignKeyConstraint(['people_id'], ['people.id'], name='book_reviews_people_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='book_reviews_pkey')
    )
    op.create_table('books',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('isbn', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('author', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('year', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('review_count', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('average_score', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='books_pkey'),
    sa.UniqueConstraint('isbn', name='books_isbn_key')
    )
    op.create_table('people',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('firstname', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('lastname', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('hash', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('comments', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='people_pkey'),
    sa.UniqueConstraint('email', name='people_email_key'),
    sa.UniqueConstraint('username', name='people_username_key')
    )
    # ### end Alembic commands ###