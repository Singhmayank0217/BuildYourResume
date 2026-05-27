import pytest


@pytest.mark.integration
@pytest.mark.migration
def test_expected_tables_and_indexes_exist(db_connection):
    expected_tables = {
        "users",
        "resumes",
        "resume_versions",
        "ai_jobs",
        "audit_logs",
        "embeddings",
    }

    with db_connection.cursor() as cur:
        cur.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            """
        )
        tables = {row[0] for row in cur.fetchall()}

        missing = expected_tables - tables
        assert not missing, f"Missing expected tables: {missing}"

        cur.execute(
            """
            SELECT indexname
            FROM pg_indexes
            WHERE schemaname = 'public' AND tablename = 'ai_jobs'
            """
        )
        index_names = {row[0] for row in cur.fetchall()}

        assert "ix_ai_jobs_status" in index_names
        assert "ix_ai_jobs_idempotency_key" in index_names
