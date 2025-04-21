from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import BaseModel


class Question(BaseModel):
    __tablename__ = "questions"

    question: Mapped[str]
    answer_text: Mapped[str | None]
    answer_picture_path: Mapped[str | None]
    answer_file_id: Mapped[str | None]
    folder_id: Mapped[int | None] = mapped_column(ForeignKey("folders.id"))
    is_active: Mapped[bool] = mapped_column(default=True)

    folder: Mapped["Folder"] = relationship("Folder", back_populates="questions", uselist=False)
