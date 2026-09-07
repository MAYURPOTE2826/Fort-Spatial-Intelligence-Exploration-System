import os
import sys
from pathlib import Path

# Add backend directory to path so we can import app modules
backend_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(backend_dir))

from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.database import SessionLocal
from app.models.rag import HistoricalDocument, DocumentChunk
from app.services.embedding_service import embedding_service

def ingest_directory(directory_path: str, language: str = "en"):
    path = Path(directory_path)
    if not path.exists():
        print(f"Directory {directory_path} not found.")
        return

    db = SessionLocal()
    
    # Configure text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=750,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )
    
    for file_path in path.glob("*.md"):
        print(f"Processing {file_path.name}...")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        title = file_path.stem.replace("_", " ").title()
        
        # Create HistoricalDocument record
        doc = HistoricalDocument(
            title=title,
            content=content,
            source_url=f"local://{file_path.name}",
            language=language
        )
        db.add(doc)
        db.flush() # flush to get doc.id
        
        # Split text
        chunks = text_splitter.split_text(content)
        
        for i, chunk_text in enumerate(chunks):
            # Generate embedding
            embedding = embedding_service.get_embedding(chunk_text)
            
            chunk_record = DocumentChunk(
                document_id=doc.id,
                chunk_index=i,
                content=chunk_text,
                embedding=embedding
            )
            db.add(chunk_record)
            
        db.commit()
        print(f"Ingested {file_path.name} with {len(chunks)} chunks.")
        
    db.close()
    print("Ingestion complete.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Ingest markdown documents into the RAG system.")
    parser.add_argument("--source", type=str, required=True, help="Directory containing markdown files")
    parser.add_argument("--language", type=str, default="en", help="Language of the documents")
    
    args = parser.parse_args()
    ingest_directory(args.source, args.language)
