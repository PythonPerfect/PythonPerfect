"""final revision

Revision ID: 98519a88d44a
Revises: 0cd365d17cd8
Create Date: 2021-05-17 11:09:00.466482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98519a88d44a'
down_revision = '0cd365d17cd8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question__response', schema=None) as batch_op:
        batch_op.add_column(sa.Column('correct', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('result_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('results_fk', 'result', ['result_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question__response', schema=None) as batch_op:
        batch_op.drop_constraint('results_fk', type_='foreignkey')
        batch_op.drop_column('result_id')
        batch_op.drop_column('correct')

    # ### end Alembic commands ###
