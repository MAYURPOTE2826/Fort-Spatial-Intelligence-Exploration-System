from app.core.database import Base
from app.models.users import User
from app.models.forts import Fort, FortViewpoint, FortStructure, FortTrail, FortConnection
from app.models.terrain import TerrainTile
from app.models.rag import HistoricalDocument, DocumentChunk, ChatSession, ChatMessage
from app.models.visibility import VisibilityResult

# This ensures all models are imported and metadata is registered
# for Alembic autogenerate
