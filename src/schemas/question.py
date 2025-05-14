from pydantic import BaseModel, ValidationError, model_validator
from typing import Optional

from src.schemas.base import BaseDto


class QuestionBase(BaseModel):
    """Базовая схема вопроса"""

    question: str
    answer_text: Optional[str] = None
    answer_picture_path: Optional[str] = None
    answer_file_id: Optional[str] = None
    folder_id: Optional[int] = None
    is_active: bool = True

    @model_validator(mode="after")
    def validate_answer_content(self):
        if self.answer_text is None and self.answer_picture_path is None:
            raise ValueError(
                "Хотя бы одно из полей (answer_text или answer_picture_path) должно быть заполнено"
            )
        return self


class QuestionDto(BaseDto, QuestionBase):
    """Схема вопроса с ID и метками времени"""

    pass


if __name__ == "__main__":
    question = QuestionBase(
        question="Как стать донором?", answer_text=None, answer_picture_path="/some/path.png"
    )
    print(question.model_dump_json())

    try:
        question = QuestionBase(
            question="Как стать донором?", answer_text=None, answer_picture_path=None
        )
    except ValidationError as e:
        print(e.errors())
