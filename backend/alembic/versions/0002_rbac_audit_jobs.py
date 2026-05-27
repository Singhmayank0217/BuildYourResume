"""RBAC and audit/job tracking schema

Adds user roles, audit logs, and supporting indexes for job provenance.
"""
from alembic import op
import sqlalchemy as sa

revision = '0002_rbac_audit_jobs'
down_revision = '0001_initial'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    user_columns = [col['name'] for col in inspector.get_columns('users')]
    if 'role' not in user_columns:
        op.add_column('users', sa.Column('role', sa.String(length=32), nullable=False, server_default='user'))
    op.create_index('ix_users_role', 'users', ['role'], unique=False)

    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('resume_id', sa.Integer(), nullable=True),
        sa.Column('resume_version_id', sa.Integer(), nullable=True),
        sa.Column('event_type', sa.String(length=64), nullable=False),
        sa.Column('actor_id', sa.Integer(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], name='fk_audit_logs_resume'),
        sa.ForeignKeyConstraint(['resume_version_id'], ['resume_versions.id'], name='fk_audit_logs_resume_version'),
    )
    op.create_index('ix_audit_logs_resume_id', 'audit_logs', ['resume_id'], unique=False)
    op.create_index('ix_audit_logs_resume_version_id', 'audit_logs', ['resume_version_id'], unique=False)
    op.create_index('ix_audit_logs_created_at', 'audit_logs', ['created_at'], unique=False)

    op.create_index('ix_ai_jobs_status', 'ai_jobs', ['status'], unique=False)
    op.create_index('ix_ai_jobs_dedup_key', 'ai_jobs', ['dedup_key'], unique=False)
    op.create_index('ix_ai_jobs_idempotency_key', 'ai_jobs', ['idempotency_key'], unique=False)
    op.create_index('ix_ai_jobs_resume_version_id', 'ai_jobs', ['resume_version_id'], unique=False)


def downgrade():
    op.drop_index('ix_ai_jobs_resume_version_id', table_name='ai_jobs')
    op.drop_index('ix_ai_jobs_idempotency_key', table_name='ai_jobs')
    op.drop_index('ix_ai_jobs_dedup_key', table_name='ai_jobs')
    op.drop_index('ix_ai_jobs_status', table_name='ai_jobs')

    op.drop_index('ix_audit_logs_created_at', table_name='audit_logs')
    op.drop_index('ix_audit_logs_resume_version_id', table_name='audit_logs')
    op.drop_index('ix_audit_logs_resume_id', table_name='audit_logs')
    op.drop_table('audit_logs')

    op.drop_index('ix_users_role', table_name='users')
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    user_columns = [col['name'] for col in inspector.get_columns('users')]
    if 'role' in user_columns:
        op.drop_column('users', 'role')
