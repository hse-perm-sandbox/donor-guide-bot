from sqlalchemy.orm import Session

from src.database.models.user import User
from src.database.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_telegram_chat_id(self, telegram_chat_id: int) -> User:
        return (
            self.db.query(self.model)
            .filter(self.model.telegram_chat_id == telegram_chat_id)
            .first()
        )

    def create_or_update(self, telegram_chat_id: int, **kwargs) -> User:
        user = self.get_by_telegram_chat_id(telegram_chat_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
        else:
            user = User(telegram_chat_id=telegram_chat_id, **kwargs)
            self.db.add(user)
        self.db.commit()
        return user
