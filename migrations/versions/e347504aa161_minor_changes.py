"""Minor changes

Revision ID: e347504aa161
Revises: 11a16ad468b3
Create Date: 2021-05-12 14:56:47.646605

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e347504aa161'
down_revision = '11a16ad468b3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('content', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_content_title'), ['title'], unique=True)

    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_question_question'), ['question'], unique=True)

    with op.batch_alter_table('quiz', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_quiz_title'), ['title'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quiz', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_quiz_title'))

    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_question_question'))

    with op.batch_alter_table('content', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_content_title'))

    # ### end Alembic commands ###
