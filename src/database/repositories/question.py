from sqlalchemy.orm import Session

from src.database.models.question import Question
from src.database.repositories.base import BaseRepository
from src.schemas.question import QuestionBase, QuestionDto


class QuestionRepository(BaseRepository[Question]):
    def __init__(self, db: Session):
        super().__init__(Question, db)

    def get_by_folder(self, folder_id: int):
        return (
            self.db.query(self.model)
            .filter(self.model.folder_id == folder_id, self.model.is_active == True)
            .order_by(self.model.id)
            .all()
        )

    def get_by_id(self, question_id: int):
        return self.db.query(self.model).get(question_id)

    def get_active_by_folder(self, folder_id: int) -> list[Question]:
        return (
            self.db.query(self.model)
            .filter(self.model.folder_id == folder_id, self.model.is_active == True)
            .all()
        )

    def create(self, question_data: QuestionBase) -> QuestionDto:
        question = Question(**question_data.model_dump())
        self.db.add(question)
        self.db.commit()
        self.db.refresh(question)
        return QuestionDto.model_validate(question)
