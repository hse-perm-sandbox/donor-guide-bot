from pydantic import BaseModel
from typing import Optional

from src.schemas.base import BaseDto


class FolderBase(BaseModel):
    """Базовая схема папки"""

    folder_name: str
    parent_id: Optional[int] = None
    is_active: bool = True


class FolderDto(BaseDto, FolderBase):
    """Схема папки с ID и метками времени"""

    pass
