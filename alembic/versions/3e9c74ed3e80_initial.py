"""initial

Revision ID: 3e9c74ed3e80
Revises: 
Create Date: 2023-03-21 13:19:02.987349

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e9c74ed3e80'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('statistics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('views', sa.Integer(), nullable=True),
    sa.Column('clicks', sa.String(), nullable=True),
    sa.Column('cost', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('statistics')
    # ### end Alembic commands ###
