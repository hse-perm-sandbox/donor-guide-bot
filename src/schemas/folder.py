from pydantic import BaseModel
from typing import Optional

from src.schemas.base import BaseDto
from src.schemas.question import QuestionDto


class FolderBase(BaseModel):
    """Базовая схема папки"""

    folder_name: str
    parent_id: Optional[int] = None
    is_active: bool = True


class FolderDto(BaseDto, FolderBase):
    """Схема папки с ID и метками времени"""

    pass


class FolderWithContentDto(FolderDto):
    subfolders: list["FolderDto"] = []
    questions: list["QuestionDto"] = []

    class Config:
        from_attributes = True
