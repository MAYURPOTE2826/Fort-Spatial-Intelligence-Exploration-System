from sentence_transformers import SentenceTransformer
from typing import List

class EmbeddingService:
    def __init__(self):
        # We load the multilingual model on initialization
        self.model_name = "paraphrase-multilingual-MiniLM-L12-v2"
        self._model = None

    @property
    def model(self):
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def get_embedding(self, text: str) -> List[float]:
        """Get the embedding for a single text string."""
        embedding = self.model.encode(text)
        return embedding.tolist()

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for a list of text strings."""
        embeddings = self.model.encode(texts)
        return embeddings.tolist()

embedding_service = EmbeddingService()
