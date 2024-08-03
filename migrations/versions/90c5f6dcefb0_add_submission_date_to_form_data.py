"""Add submission_date to form_data

Revision ID: 90c5f6dcefb0
Revises: 01b86f3d03b8
Create Date: 2024-08-03 21:54:00.123456

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '90c5f6dcefb0'
down_revision = '01b86f3d03b8'
branch_labels = None
depends_on = None

def upgrade():
    # Step 1: Add the column without NOT NULL constraint
    op.add_column('form_data', sa.Column('submission_date', sa.DateTime(), nullable=True))

    # Step 2: Update existing rows to have a default value
    op.execute(
        sa.text("UPDATE form_data SET submission_date = NOW() WHERE submission_date IS NULL")
    )

    # Step 3: Alter the column to set NOT NULL constraint
    op.alter_column('form_data', 'submission_date', existing_type=sa.DateTime(), nullable=False)

def downgrade():
    # Remove the column in downgrade
    op.drop_column('form_data', 'submission_date')
