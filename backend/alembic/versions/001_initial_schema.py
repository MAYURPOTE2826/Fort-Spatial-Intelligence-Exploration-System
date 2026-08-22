"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2026-08-19 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import geoalchemy2

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Ensure PostGIS is enabled
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis;")

    # 1. users
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # 2. forts
    op.create_table('forts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('marathi_name', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('geometry', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'), nullable=False),
    sa.Column('elevation', sa.Float(), nullable=True),
    sa.Column('district', sa.String(), nullable=True),
    sa.Column('difficulty', sa.String(), nullable=True),
    sa.Column('best_season', sa.String(), nullable=True),
    sa.Column('history', sa.Text(), nullable=True),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('source', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_forts_district'), 'forts', ['district'], unique=False)
    op.create_index(op.f('ix_forts_id'), 'forts', ['id'], unique=False)
    op.create_index(op.f('ix_forts_name'), 'forts', ['name'], unique=False)

    # 3. fort_viewpoints
    op.create_table('fort_viewpoints',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fort_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('geometry', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'), nullable=False),
    sa.Column('elevation', sa.Float(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['fort_id'], ['forts.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fort_viewpoints_id'), 'fort_viewpoints', ['id'], unique=False)

    # 4. fort_structures
    op.create_table('fort_structures',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fort_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('geometry', geoalchemy2.types.Geometry(geometry_type='GEOMETRY', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['fort_id'], ['forts.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fort_structures_id'), 'fort_structures', ['id'], unique=False)

    # 5. fort_trails
    op.create_table('fort_trails',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fort_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('difficulty', sa.String(), nullable=True),
    sa.Column('geometry', geoalchemy2.types.Geometry(geometry_type='LINESTRING', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'), nullable=False),
    sa.Column('distance_km', sa.Float(), nullable=True),
    sa.Column('estimated_time_hours', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['fort_id'], ['forts.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fort_trails_id'), 'fort_trails', ['id'], unique=False)

    # 6. fort_connections
    op.create_table('fort_connections',
    sa.Column('source_fort_id', sa.Integer(), nullable=False),
    sa.Column('target_fort_id', sa.Integer(), nullable=False),
    sa.Column('distance_km', sa.Float(), nullable=True),
    sa.Column('bearing_deg', sa.Float(), nullable=True),
    sa.Column('visibility_status', sa.String(), nullable=True),
    sa.Column('visibility_score', sa.Float(), nullable=True),
    sa.Column('last_calculated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['source_fort_id'], ['forts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['target_fort_id'], ['forts.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('source_fort_id', 'target_fort_id')
    )

    # 7. terrain_tiles
    op.create_table('terrain_tiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tile_name', sa.String(), nullable=False),
    sa.Column('zoom_level', sa.Integer(), nullable=False),
    sa.Column('geometry', geoalchemy2.types.Geometry(geometry_type='POLYGON', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'), nullable=False),
    sa.Column('file_path', sa.String(), nullable=False),
    sa.Column('resolution_m', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_terrain_tiles_id'), 'terrain_tiles', ['id'], unique=False)
    op.create_index(op.f('ix_terrain_tiles_tile_name'), 'terrain_tiles', ['tile_name'], unique=True)

    # 8. historical_documents
    op.create_table('historical_documents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('source_url', sa.String(), nullable=True),
    sa.Column('fort_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['fort_id'], ['forts.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_historical_documents_id'), 'historical_documents', ['id'], unique=False)

    # 9. document_chunks
    op.create_table('document_chunks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('document_id', sa.Integer(), nullable=False),
    sa.Column('chunk_index', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('embedding', postgresql.ARRAY(sa.Float()), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['document_id'], ['historical_documents.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_document_chunks_id'), 'document_chunks', ['id'], unique=False)

    # 10. chat_sessions
    op.create_table('chat_sessions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chat_sessions_id'), 'chat_sessions', ['id'], unique=False)

    # 11. chat_messages
    op.create_table('chat_messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('heading', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['chat_sessions.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chat_messages_id'), 'chat_messages', ['id'], unique=False)

    # 12. visibility_results
    op.create_table('visibility_results',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('observer_lat', sa.Float(), nullable=False),
    sa.Column('observer_lon', sa.Float(), nullable=False),
    sa.Column('observer_elevation', sa.Float(), nullable=False),
    sa.Column('fort_id', sa.Integer(), nullable=False),
    sa.Column('visibility_status', sa.String(), nullable=False),
    sa.Column('visibility_score', sa.Float(), nullable=False),
    sa.Column('calculated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['fort_id'], ['forts.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_visibility_results_expires_at'), 'visibility_results', ['expires_at'], unique=False)
    op.create_index(op.f('ix_visibility_results_fort_id'), 'visibility_results', ['fort_id'], unique=False)
    op.create_index(op.f('ix_visibility_results_id'), 'visibility_results', ['id'], unique=False)
    op.create_index(op.f('ix_visibility_results_observer_lat'), 'visibility_results', ['observer_lat'], unique=False)
    op.create_index(op.f('ix_visibility_results_observer_lon'), 'visibility_results', ['observer_lon'], unique=False)


def downgrade() -> None:
    op.drop_table('visibility_results')
    op.drop_table('chat_messages')
    op.drop_table('chat_sessions')
    op.drop_table('document_chunks')
    op.drop_table('historical_documents')
    op.drop_table('terrain_tiles')
    op.drop_table('fort_connections')
    op.drop_table('fort_trails')
    op.drop_table('fort_structures')
    op.drop_table('fort_viewpoints')
    op.drop_table('forts')
    op.drop_table('users')
