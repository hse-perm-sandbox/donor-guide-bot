from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

from src.schemas.base import BaseDto


class UserBase(BaseModel):
    """Базовая схема пользователя"""

    telegram_chat_id: int
    telegram_username: str
    email: Optional[EmailStr] = None


class UserDto(BaseDto, UserBase):
    """Базовая схема с ID и метками времени"""

    pass
