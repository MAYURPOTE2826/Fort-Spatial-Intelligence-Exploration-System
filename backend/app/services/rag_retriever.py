from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.rag import DocumentChunk, HistoricalDocument
from app.services.embedding_service import embedding_service
from app.core.logging import logger


class RAGRetriever:
    def __init__(self):
        pass

    def retrieve_static(self, db: Session, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve relevant document chunks using pgvector similarity search."""
        try:
            query_embedding = embedding_service.get_embedding(query)
        except Exception as e:
            logger.warning(f"Failed to get embedding for query: {e}")
            return []

        try:
            results = (
                db.query(DocumentChunk, HistoricalDocument)
                .join(HistoricalDocument, DocumentChunk.document_id == HistoricalDocument.id)
                .order_by(DocumentChunk.embedding.l2_distance(query_embedding))
                .limit(top_k)
                .all()
            )
        except Exception as e:
            logger.warning(f"Vector similarity search failed (table may be empty or schema not ready): {e}")
            return []

        retrieved_context = []
        for chunk, doc in results:
            retrieved_context.append({
                "title": doc.title,
                "content": chunk.content,
                "source_url": doc.source_url,
                "language": getattr(doc, "language", "en"),
                "fort_id": doc.fort_id,
            })

        return retrieved_context

    def retrieve_spatial(
        self,
        db: Session,
        query: str,
        lat: Optional[float],
        lon: Optional[float],
        heading: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Retrieve visible forts from observer location and return structured context."""
        if lat is None or lon is None:
            return {
                "error": "Location data required for spatial queries.",
                "visible_forts": [],
                "context": [],
            }

        # Import here to avoid circular imports
        from app.services.visibility_service import VisibilityService

        try:
            visibility_response = VisibilityService.calculate_visibility_from_location(
                db=db,
                lat=lat,
                lon=lon,
                heading=heading,
                fov=None,
                radius_km=50,
                elevation=None,
                observer_height=1.7,
            )
        except Exception as e:
            logger.error(f"Spatial visibility query failed in RAG retriever: {e}")
            return {
                "error": f"Visibility calculation failed: {str(e)}",
                "visible_forts": [],
                "context": [],
            }

        visible_forts = []
        for fort in visibility_response.visible_forts:
            visible_forts.append({
                "name": fort.name,
                "distance": fort.distance_km,
                "id": fort.id,
                "direction": fort.direction,
                "bearing": fort.bearing_deg,
            })

        # Build a human-readable context string for the LLM
        context_lines = [f"Visible forts from observer location ({lat:.4f}, {lon:.4f}):"]
        for f in visible_forts:
            context_lines.append(
                f"  - {f['name']} ({f['direction']}, {f['distance']:.1f} km away)"
            )
        if not visible_forts:
            context_lines.append("  No forts are currently visible from this location.")

        return {
            "visible_forts": visible_forts,
            "context": [
                {
                    "title": "Live Visibility Data",
                    "content": "\n".join(context_lines),
                    "source_url": "system",
                }
            ],
        }

    def retrieve_hybrid(
        self,
        db: Session,
        query: str,
        lat: Optional[float],
        lon: Optional[float],
        heading: Optional[float] = None,
        top_k: int = 3,
    ) -> Dict[str, Any]:
        """Combine spatial visibility results with static RAG retrieval."""
        spatial_data = self.retrieve_spatial(db, query, lat, lon, heading)
        static_data = self.retrieve_static(db, query, top_k)

        combined_context = spatial_data.get("context", []) + static_data

        return {
            "visible_forts": spatial_data.get("visible_forts", []),
            "context": combined_context,
        }


rag_retriever = RAGRetriever()
