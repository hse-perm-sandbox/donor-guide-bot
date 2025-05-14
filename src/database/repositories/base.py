from typing import Generic, List, TypeVar

from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, model: T, db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, id: int) -> T:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self) -> List[T]:
        return self.db.query(self.model).all()

    def create(self, obj: T) -> T:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
