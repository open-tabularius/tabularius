"""documents students tables

Revision ID: 495b3a1e2c79
Revises: bfbd34372393
Create Date: 2018-04-14 13:22:04.637588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '495b3a1e2c79'
down_revision = 'bfbd34372393'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ssn_id', sa.Integer(), nullable=True),
    sa.Column('ps_id', sa.Integer(), nullable=True),
    sa.Column('local_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_student_local_id'), 'student', ['local_id'], unique=True)
    op.create_index(op.f('ix_student_ps_id'), 'student', ['ps_id'], unique=True)
    op.create_index(op.f('ix_student_ssn_id'), 'student', ['ssn_id'], unique=True)
    op.create_table('document',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('upload_name', sa.String(length=64), nullable=True),
    sa.Column('file_name', sa.String(length=64), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('file', sa.LargeBinary(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_document_timestamp'), 'document', ['timestamp'], unique=False)
    op.create_index(op.f('ix_document_upload_name'), 'document', ['upload_name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_document_upload_name'), table_name='document')
    op.drop_index(op.f('ix_document_timestamp'), table_name='document')
    op.drop_table('document')
    op.drop_index(op.f('ix_student_ssn_id'), table_name='student')
    op.drop_index(op.f('ix_student_ps_id'), table_name='student')
    op.drop_index(op.f('ix_student_local_id'), table_name='student')
    op.drop_table('student')
    # ### end Alembic commands ###
