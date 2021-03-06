"""cat food amount

Revision ID: 030155dfb703
Revises: 5974a42c769d
Create Date: 2020-04-25 14:07:00.347277

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '030155dfb703'
down_revision = '5974a42c769d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cat', sa.Column('feeding_amount', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cat', 'feeding_amount')
    # ### end Alembic commands ###
