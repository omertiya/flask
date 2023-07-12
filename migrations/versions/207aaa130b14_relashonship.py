"""relashonship

Revision ID: 207aaa130b14
Revises: 1b28a8f2bd3c
Create Date: 2023-06-15 11:16:44.014447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '207aaa130b14'
down_revision = '1b28a8f2bd3c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_user_email'), ['email'])
        batch_op.create_unique_constraint(batch_op.f('uq_user_user_name'), ['user_name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_user_user_name'), type_='unique')
        batch_op.drop_constraint(batch_op.f('uq_user_email'), type_='unique')

    # ### end Alembic commands ###