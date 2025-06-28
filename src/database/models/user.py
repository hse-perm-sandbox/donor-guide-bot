from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import BaseModel
from src.database.models.user_question import UserQuestion


class User(BaseModel):
    __tablename__ = "users"
    telegram_chat_id: Mapped[int] = mapped_column(BigInteger)
    telegram_username: Mapped[str]
    email: Mapped[str | None]
    user_questions: Mapped[list["UserQuestion"]] = relationship(
        "UserQuestion",
        back_populates="user",
        cascade="all, delete-orphan",
    )
