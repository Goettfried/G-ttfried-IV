"""Create user table

Revision ID: 3010af71ffb7
Revises: 
Create Date: 2024-08-03 19:45:18.684205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3010af71ffb7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('form_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('phone', sa.String(length=50), nullable=True),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('submission_type', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=150), nullable=False),
    sa.Column('password_hash', sa.String(length=150), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('form_data')
    # ### end Alembic commands ###
