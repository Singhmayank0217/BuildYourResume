"""Initial baseline migration

Creates users, resumes, resume_versions, ai_jobs, embeddings tables and links current_version_id after creation.
"""
from alembic import op
import sqlalchemy as sa

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('first_name', sa.String(length=120), nullable=False),
        sa.Column('last_name', sa.String(length=120), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('linkedin_url', sa.String(length=255), nullable=True),
        sa.Column('role', sa.String(length=32), nullable=False, server_default='user'),
    )
    op.create_unique_constraint('uq_users_email', 'users', ['email'])
    op.create_index('ix_users_email', 'users', ['email'], unique=False)

    op.create_table(
        'resumes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=True, index=False),
        sa.Column('filename', sa.String(), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'resume_versions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('resume_id', sa.Integer(), nullable=False),
        sa.Column('content', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('source', sa.String(), nullable=True),
        sa.Column('previous_version_id', sa.Integer(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
    )
    op.create_foreign_key('fk_resume_versions_resume', 'resume_versions', 'resumes', ['resume_id'], ['id'])

    op.create_table(
        'ai_jobs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('job_type', sa.String(), nullable=True),
        sa.Column('resume_version_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('provider', sa.String(), nullable=True),
        sa.Column('prompt', sa.Text(), nullable=True),
        sa.Column('result', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('finished_at', sa.DateTime(), nullable=True),
        sa.Column('dedup_key', sa.String(), nullable=True),
        sa.Column('idempotency_key', sa.String(), nullable=True),
        sa.Column('attempts', sa.Integer(), nullable=True),
        sa.Column('max_retries', sa.Integer(), nullable=True),
        sa.Column('last_error', sa.Text(), nullable=True),
        sa.Column('timeout_seconds', sa.Integer(), nullable=True),
    )
    op.create_foreign_key('fk_ai_jobs_resume_version', 'ai_jobs', 'resume_versions', ['resume_version_id'], ['id'])

    op.create_table(
        'embeddings',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('resume_version_id', sa.Integer(), nullable=False),
        sa.Column('vector', sa.JSON(), nullable=True),
        sa.Column('model', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )
    op.create_foreign_key('fk_embeddings_resume_version', 'embeddings', 'resume_versions', ['resume_version_id'], ['id'])

    op.add_column('resumes', sa.Column('current_version_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_resumes_current_version', 'resumes', 'resume_versions', ['current_version_id'], ['id'])


def downgrade():
    op.drop_constraint('fk_resumes_current_version', 'resumes', type_='foreignkey')
    op.drop_column('resumes', 'current_version_id')
    op.drop_table('embeddings')
    op.drop_table('ai_jobs')
    op.drop_table('resume_versions')
    op.drop_table('resumes')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_constraint('uq_users_email', 'users', type_='unique')
    op.drop_table('users')
