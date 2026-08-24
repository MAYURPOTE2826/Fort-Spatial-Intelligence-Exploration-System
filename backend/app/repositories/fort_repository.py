from sqlalchemy.orm import Session
from app.models.forts import Fort

class FortRepository:
    def get(self, db: Session, id: int):
        # Placeholder
        return None

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
        # Placeholder
        return []
