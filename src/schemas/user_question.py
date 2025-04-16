from pydantic import BaseModel
from src.schemas.base import BaseDto


class UserQuestionBase(BaseModel):
    """Базовая схема вопроса пользователя (без ID и временных меток)"""

    question_text: str
    sent: bool = False
    user_id: int


class UserQuestionDto(BaseDto, UserQuestionBase):
    """Основная схема вопроса с ID и метками времени"""

    pass
