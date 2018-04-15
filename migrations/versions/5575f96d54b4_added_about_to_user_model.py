"""added about to user model

Revision ID: 5575f96d54b4
Revises: 75225001c09f
Create Date: 2018-04-15 09:53:57.130015

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5575f96d54b4'
down_revision = '75225001c09f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user',
                  sa.Column('about', sa.String(length=300), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'about')
    # ### end Alembic commands ###