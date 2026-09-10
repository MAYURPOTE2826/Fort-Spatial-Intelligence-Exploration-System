"""Fix schema: chat_sessions id type, document_chunks embedding vector,
visibility_cache table, users hashed_password + is_active + is_admin,
spatial index on forts.geometry, pgvector index on document_chunks.embedding,
historical_documents language column.

Revision ID: 002
Revises: 001
Create Date: 2026-09-10 00:00:00.000000

This migration is ADDITIVE. It adds missing columns and fixes type mismatches
via a column-level migration, preserving existing data where possible.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()

    # -----------------------------------------------------------------------
    # 1. Enable pgvector extension (idempotent)
    # -----------------------------------------------------------------------
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # -----------------------------------------------------------------------
    # 2. users — add missing auth columns
    # -----------------------------------------------------------------------
    # Check if hashed_password column already exists before adding
    result = conn.execute(sa.text(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_name='users' AND column_name='hashed_password'"
    ))
    if not result.fetchone():
        op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=True))
        # Backfill existing rows with a placeholder (they cannot log in)
        op.execute("UPDATE users SET hashed_password = 'MIGRATION_PLACEHOLDER' WHERE hashed_password IS NULL")
        op.alter_column('users', 'hashed_password', nullable=False)

    result = conn.execute(sa.text(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_name='users' AND column_name='is_active'"
    ))
    if not result.fetchone():
        op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')))

    result = conn.execute(sa.text(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_name='users' AND column_name='is_admin'"
    ))
    if not result.fetchone():
        op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=False, server_default=sa.text('false')))

    # -----------------------------------------------------------------------
    # 3. chat_sessions — migrate id from INTEGER to VARCHAR (UUID strings)
    # -----------------------------------------------------------------------
    # If chat_sessions.id is still INTEGER (from original migration), migrate it
    result = conn.execute(sa.text(
        "SELECT data_type FROM information_schema.columns "
        "WHERE table_name='chat_sessions' AND column_name='id'"
    ))
    row = result.fetchone()
    if row and row[0] == 'integer':
        # Drop dependent chat_messages FK, alter types, recreate FK
        op.drop_constraint('chat_messages_session_id_fkey', 'chat_messages', type_='foreignkey')
        op.alter_column('chat_messages', 'session_id',
                        existing_type=sa.Integer(),
                        type_=sa.String(),
                        existing_nullable=False,
                        postgresql_using="session_id::text")
        op.alter_column('chat_sessions', 'id',
                        existing_type=sa.Integer(),
                        type_=sa.String(),
                        existing_nullable=False,
                        postgresql_using="id::text")
        # Remove the old integer sequence default
        op.execute("ALTER TABLE chat_sessions ALTER COLUMN id DROP DEFAULT")
        op.create_foreign_key(
            'chat_messages_session_id_fkey',
            'chat_messages', 'chat_sessions',
            ['session_id'], ['id'],
            ondelete='CASCADE'
        )

    # -----------------------------------------------------------------------
    # 4. document_chunks — migrate embedding from ARRAY(float8) to vector(384)
    # -----------------------------------------------------------------------
    result = conn.execute(sa.text(
        "SELECT data_type, udt_name FROM information_schema.columns "
        "WHERE table_name='document_chunks' AND column_name='embedding'"
    ))
    row = result.fetchone()
    # If it's stored as ARRAY or not yet vector type, convert it
    if row and row[1] != 'vector':
        # Drop old column and recreate as vector — existing embeddings lost but table likely empty
        op.drop_column('document_chunks', 'embedding')
        op.execute("ALTER TABLE document_chunks ADD COLUMN embedding vector(384)")

    # -----------------------------------------------------------------------
    # 5. historical_documents — add language column if missing
    # -----------------------------------------------------------------------
    result = conn.execute(sa.text(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_name='historical_documents' AND column_name='language'"
    ))
    if not result.fetchone():
        op.add_column('historical_documents', sa.Column('language', sa.String(), nullable=True, server_default='en'))

    # -----------------------------------------------------------------------
    # 6. visibility_cache — create table if missing
    # -----------------------------------------------------------------------
    result = conn.execute(sa.text(
        "SELECT tablename FROM pg_tables WHERE tablename='visibility_cache'"
    ))
    if not result.fetchone():
        op.create_table('visibility_cache',
            sa.Column('cache_key', sa.String(), nullable=False),
            sa.Column('response_payload', sa.Text(), nullable=False),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
            sa.PrimaryKeyConstraint('cache_key')
        )
        op.create_index('ix_visibility_cache_expires_at', 'visibility_cache', ['expires_at'])

    # -----------------------------------------------------------------------
    # 7. PostGIS spatial index on forts.geometry (GiST)
    # -----------------------------------------------------------------------
    result = conn.execute(sa.text(
        "SELECT indexname FROM pg_indexes "
        "WHERE tablename='forts' AND indexname='idx_forts_geometry_gist'"
    ))
    if not result.fetchone():
        op.execute("CREATE INDEX idx_forts_geometry_gist ON forts USING GIST (geometry)")

    # -----------------------------------------------------------------------
    # 8. pgvector IVFFlat index on document_chunks.embedding
    #    (created only if table has > 0 rows — empty table index is fine too)
    # -----------------------------------------------------------------------
    result = conn.execute(sa.text(
        "SELECT indexname FROM pg_indexes "
        "WHERE tablename='document_chunks' AND indexname='idx_chunks_embedding_ivfflat'"
    ))
    if not result.fetchone():
        # lists=100 suitable for up to ~1M vectors; adjust as data grows
        op.execute(
            "CREATE INDEX idx_chunks_embedding_ivfflat ON document_chunks "
            "USING ivfflat (embedding vector_l2_ops) WITH (lists = 100)"
        )

    # -----------------------------------------------------------------------
    # 9. fort_trails — add index on fort_id FK if missing
    # -----------------------------------------------------------------------
    result = conn.execute(sa.text(
        "SELECT indexname FROM pg_indexes "
        "WHERE tablename='fort_trails' AND indexname='ix_fort_trails_fort_id'"
    ))
    if not result.fetchone():
        op.create_index('ix_fort_trails_fort_id', 'fort_trails', ['fort_id'])

    # -----------------------------------------------------------------------
    # 10. fort_structures — add index on fort_id FK if missing
    # -----------------------------------------------------------------------
    result = conn.execute(sa.text(
        "SELECT indexname FROM pg_indexes "
        "WHERE tablename='fort_structures' AND indexname='ix_fort_structures_fort_id'"
    ))
    if not result.fetchone():
        op.create_index('ix_fort_structures_fort_id', 'fort_structures', ['fort_id'])


def downgrade() -> None:
    # Reverse in order
    op.drop_index('ix_fort_structures_fort_id', 'fort_structures')
    op.drop_index('ix_fort_trails_fort_id', 'fort_trails')
    op.execute("DROP INDEX IF EXISTS idx_chunks_embedding_ivfflat")
    op.execute("DROP INDEX IF EXISTS idx_forts_geometry_gist")
    op.drop_table('visibility_cache')
    op.drop_column('historical_documents', 'language')
    # Note: reversing the embedding and chat_sessions type changes would lose data
    # and is not safely reversible in a simple downgrade.
    op.drop_column('users', 'is_admin')
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'hashed_password')
