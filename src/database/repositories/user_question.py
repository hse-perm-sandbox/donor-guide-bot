from sqlalchemy.orm import Session

from src.database.models.user_question import UserQuestion
from src.database.repositories.base import BaseRepository
from src.schemas.user_question import (
    UserQuestionBase,
    UserQuestionDto,
)


class UserQuestionRepository(BaseRepository[UserQuestion]):
    def __init__(self, db: Session):
        super().__init__(UserQuestion, db)

    def create(self, question_data: UserQuestionBase) -> UserQuestionDto:
        question = UserQuestion(**question_data.model_dump())
        return UserQuestionDto.model_validate(super().create(question))
