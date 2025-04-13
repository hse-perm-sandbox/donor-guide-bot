from sqlalchemy.orm import Session

from src.database.models.user import User
from src.database.repositories.base import BaseRepository
from src.schemas.user import UserBase, UserDto


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_telegram_chat_id(self, telegram_chat_id: int) -> UserDto:
        return (
            self.db.query(self.model)
            .filter(self.model.telegram_chat_id == telegram_chat_id)
            .first()
        )

    def create_or_update(self, user_data: UserBase) -> UserDto:
        user = self.get_by_telegram_chat_id(user_data.telegram_chat_id)
        if user:
            for key, value in user_data.model_dump().items():
                setattr(user, key, value)
        else:
            user = User(**user_data.model_dump())
            self.db.add(user)
        self.db.commit()
        return UserDto.model_validate(user)
