"""Changed response from integer to string

Revision ID: 11a16ad468b3
Revises: 77b4b6ae646d
Create Date: 2021-05-12 14:36:08.757869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11a16ad468b3'
down_revision = '77b4b6ae646d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question__response', schema=None) as batch_op:
        batch_op.alter_column('response',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=32),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question__response', schema=None) as batch_op:
        batch_op.alter_column('response',
               existing_type=sa.String(length=32),
               type_=sa.INTEGER(),
               existing_nullable=True)

    # ### end Alembic commands ###
