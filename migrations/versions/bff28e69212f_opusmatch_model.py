"""Opusmatch model

Revision ID: bff28e69212f
Revises: 
Create Date: 2023-01-03 00:14:19.473705

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bff28e69212f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('jobs',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('discipline', sa.Enum('RN', 'LPN_LVN', 'PHYSICAL_THERAPIST', name='discipline'), nullable=False),
    sa.Column('specialty', sa.Enum('ICU', 'PCU', 'DIALYSIS', 'CVOR', name='specialty'), nullable=False),
    sa.Column('state', sa.Enum('CA', 'TX', 'NY', 'MN', name='state'), nullable=False),
    sa.Column('pay_amount', sa.Float(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_jobs'))
    )
    op.create_index(op.f('ix_jobs_id'), 'jobs', ['id'], unique=False)
    op.create_table('workers',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('discipline', sa.Enum('RN', 'LPN_LVN', 'PHYSICAL_THERAPIST', name='discipline'), nullable=False),
    sa.Column('specialties', sa.ARRAY(sa.Enum('ICU', 'PCU', 'DIALYSIS', 'CVOR', name='specialty')), nullable=False),
    sa.Column('preferred_working_states', sa.ARRAY(sa.Enum('CA', 'TX', 'NY', 'MN', name='state')), nullable=False),
    sa.Column('avg_weekly_pay_amount', sa.Float(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_workers'))
    )
    op.create_index(op.f('ix_workers_id'), 'workers', ['id'], unique=False)
    op.create_table('applicants',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('worker_id', sa.String(), nullable=False),
    sa.Column('job_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], name=op.f('fk_applicants_job_id_jobs')),
    sa.ForeignKeyConstraint(['worker_id'], ['workers.id'], name=op.f('fk_applicants_worker_id_workers')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_applicants'))
    )
    op.create_index(op.f('ix_applicants_id'), 'applicants', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_applicants_id'), table_name='applicants')
    op.drop_table('applicants')
    op.drop_index(op.f('ix_workers_id'), table_name='workers')
    op.drop_table('workers')
    op.drop_index(op.f('ix_jobs_id'), table_name='jobs')
    op.drop_table('jobs')
    # ### end Alembic commands ###
