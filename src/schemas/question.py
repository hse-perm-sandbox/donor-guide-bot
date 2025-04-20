from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from src.schemas.base import BaseDto


class QuestionBase(BaseModel):
    """Базовая схема вопроса"""

    question: str
    answer_text: str
    answer_picture_path: Optional[str] = None
    answer_file_id: Optional[str] = None
    folder_id: int
    is_active: bool = True


class QuestionDto(BaseDto, QuestionBase):
    """Схема вопроса с ID и метками времени"""

    pass
