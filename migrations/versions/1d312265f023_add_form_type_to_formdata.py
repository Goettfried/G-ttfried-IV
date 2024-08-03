from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = '1d312265f023'
down_revision = 'bfa09e020305'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('form_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('form_type', sa.String(length=50), nullable=True))

    # Update existing rows to have a default value
    op.execute('UPDATE form_data SET form_type = \'default_type\'')

    with op.batch_alter_table('form_data', schema=None) as batch_op:
        batch_op.alter_column('form_type', nullable=False)

def downgrade():
    with op.batch_alter_table('form_data', schema=None) as batch_op:
        batch_op.drop_column('form_type')
