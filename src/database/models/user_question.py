from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import BaseModel


class UserQuestion(BaseModel):
    __tablename__ = "user_questions"
    question_text: Mapped[str]
    sent: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="user_questions", uselist=False)
