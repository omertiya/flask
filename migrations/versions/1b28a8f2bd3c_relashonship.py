"""relashonship

Revision ID: 1b28a8f2bd3c
Revises: 2e52168551d8
Create Date: 2023-06-14 20:29:33.865387

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b28a8f2bd3c'
down_revision = '2e52168551d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('posts_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'user', ['posts_id'], ['id'])
        batch_op.drop_column('author')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author', sa.VARCHAR(length=255), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('posts_id')

    # ### end Alembic commands ###
