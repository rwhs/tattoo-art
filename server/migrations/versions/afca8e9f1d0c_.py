"""empty message
Revision ID: afca8e9f1d0c
Revises: 3fa3cef41646
Create Date: 2019-12-01 21:25:54.307563
"""
from alembic import op
import sqlalchemy as sa

#5
# revision identifiers, used by Alembic.
revision = 'afca8e9f1d0c'
down_revision = '3fa3cef41646'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payment',
                    sa.Column('payment_intent_id',
                              sa.String(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('payment_intent_id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payment')
    # ### end Alembic commands ###
