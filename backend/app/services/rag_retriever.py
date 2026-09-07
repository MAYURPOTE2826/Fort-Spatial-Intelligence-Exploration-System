from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.rag import DocumentChunk, HistoricalDocument
from app.services.embedding_service import embedding_service
from app.services.visibility_service import visibility_service

class RAGRetriever:
    def __init__(self):
        pass

    def retrieve_static(self, db: Session, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        query_embedding = embedding_service.get_embedding(query)
        
        # Use pgvector's l2_distance to find similar chunks
        results = (
            db.query(DocumentChunk, HistoricalDocument)
            .join(HistoricalDocument, DocumentChunk.document_id == HistoricalDocument.id)
            .order_by(DocumentChunk.embedding.l2_distance(query_embedding))
            .limit(top_k)
            .all()
        )
        
        retrieved_context = []
        for chunk, doc in results:
            retrieved_context.append({
                "title": doc.title,
                "content": chunk.content,
                "source_url": doc.source_url,
                "language": doc.language,
                "distance": float(chunk.embedding.l2_distance(query_embedding)) if hasattr(chunk.embedding, 'l2_distance') else 0.0
            })
            
        return retrieved_context

    def retrieve_spatial(self, db: Session, query: str, lat: float, lon: float, heading: Optional[float] = None) -> Dict[str, Any]:
        if lat is None or lon is None:
            return {"error": "Location data required for spatial queries.", "visible_forts": [], "context": []}
            
        visibility_results = visibility_service.calculate_visibility(db, lat, lon)
        
        visible_forts = []
        for fort in visibility_results:
            if fort.get("is_visible"):
                visible_forts.append({
                    "name": fort.get("fort_name", "Unknown"),
                    "distance": fort.get("distance_km", 0),
                    "id": fort.get("fort_id")
                })
                
        # We can also fetch some basic facts about these forts from the DB if needed,
        # but for now, we just pass the names and distances to the LLM.
        context_str = f"Visible forts from user's location ({lat}, {lon}):\n"
        for f in visible_forts:
            context_str += f"- {f['name']} (Distance: {f['distance']:.2f} km)\n"
            
        return {
            "visible_forts": visible_forts,
            "context": [{"title": "Live Visibility Data", "content": context_str, "source_url": "System"}]
        }

    def retrieve_hybrid(self, db: Session, query: str, lat: float, lon: float, heading: Optional[float] = None, top_k: int = 3) -> Dict[str, Any]:
        spatial_data = self.retrieve_spatial(db, query, lat, lon, heading)
        static_data = self.retrieve_static(db, query, top_k)
        
        combined_context = spatial_data.get("context", []) + static_data
        
        return {
            "visible_forts": spatial_data.get("visible_forts", []),
            "context": combined_context
        }

rag_retriever = RAGRetriever()
