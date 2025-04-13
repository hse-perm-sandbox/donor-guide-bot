from datetime import datetime
from pydantic import BaseModel


class BaseDto(BaseModel):
    """Базовая схема с ID и метками времени"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
