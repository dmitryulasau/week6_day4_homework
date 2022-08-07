"""empty message

Revision ID: 9d8f7eb1af94
Revises: 
Create Date: 2021-11-30 18:06:24.835962

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d8f7eb1af94'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=False)
    op.create_table('recipe',
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('body', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('recipe_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recipe')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
