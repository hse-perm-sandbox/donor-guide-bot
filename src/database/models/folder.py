from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import BaseModel
from src.database.models.question import Question


class Folder(BaseModel):
    __tablename__ = "folders"

    folder_name: Mapped[str]
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("folders.id"), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    subfolders: Mapped[list["Folder"]] = relationship(
        "Folder",
        backref="parent",
        remote_side="Folder.id",
        cascade="all, delete-orphan",
        single_parent=True,
    )

    questions: Mapped[list["Question"]] = relationship(
        "Question",
        back_populates="folder",
        cascade="all, delete-orphan",
    )
