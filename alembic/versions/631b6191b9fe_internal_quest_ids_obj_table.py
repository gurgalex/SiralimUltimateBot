"""internal quest ids + obj table

Revision ID: 631b6191b9fe
Revises: eea64a3f9208
Create Date: 2021-12-14 07:25:00.304148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '631b6191b9fe'
down_revision = 'eea64a3f9208'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.execute("ALTER TABLE quest ADD COLUMN qid INTEGER NULL;")
    op.execute("CREATE UNIQUE INDEX ix_qid_uniq ON quest(qid);")

    op.execute("ALTER TABLE sprite_type ADD COLUMN description VARCHAR;")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sprite_type', schema=None) as batch_op:
        batch_op.drop_column('description')

    with op.batch_alter_table('quest', schema=None) as batch_op:
        batch_op.drop_constraint("ix_qid_uniq", type_='unique')
        batch_op.drop_column('qid')

    # ### end Alembic commands ###
