"""Init

Revision ID: 9ac67b97d638
Revises: 
Create Date: 2023-06-14 14:54:39.559768

"""
import csv

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '9ac67b97d638'
down_revision = None
branch_labels = None
depends_on = None

# get default tags
default_tags = []
with open('data/tags.csv', 'r') as file:
    tag_reader = csv.reader(file)
    for tag in tag_reader:
        default_tags.append({'name': tag[0]})


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    tag_table = op.create_table('tag',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=25), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.bulk_insert(tag_table, default_tags)
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=16), nullable=False),
    sa.Column('first_name', sa.String(length=20), nullable=True),
    sa.Column('last_name', sa.String(length=20), nullable=True),
    sa.Column('email', sqlalchemy_utils.types.email.EmailType(length=255), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('base_post',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('creation_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('type', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sign_up_verification',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('token', sa.UUID(), nullable=True),
    sa.Column('creation_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('is_used', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('link_post',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('annotation', sa.String(length=250), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['base_post.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tag_post_association',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['base_post.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tutorial_post',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('file', sa.LargeBinary(length=65536), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['base_post.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tutorial_post')
    op.drop_table('tag_post_association')
    op.drop_table('link_post')
    op.drop_table('sign_up_verification')
    op.drop_table('base_post')
    op.drop_table('user')
    op.drop_table('tag')
    # ### end Alembic commands ###
