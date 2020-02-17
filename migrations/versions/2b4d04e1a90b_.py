"""empty message

Revision ID: 2b4d04e1a90b
Revises: 
Create Date: 2020-02-09 19:50:52.433834

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b4d04e1a90b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('auth0_user_id', sa.String(), nullable=False),
    sa.Column('nickname', sa.String(length=12), nullable=False),
    sa.Column('picture_url', sa.String(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('auth0_user_id')
    )
    op.create_table('voices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=120), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('replying_to', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['replying_to'], ['voices.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('likes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('like', sa.Boolean(), nullable=True),
    sa.Column('voice_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['voice_id'], ['voices.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pictures',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('voice_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['voice_id'], ['voices.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pictures')
    op.drop_table('likes')
    op.drop_table('voices')
    op.drop_table('users')
    # ### end Alembic commands ###