from sqlalchemy.orm import Session

from src.database.models.folder import Folder
from src.database.repositories.base import BaseRepository
from src.schemas.folder import FolderBase, FolderDto


class FolderRepository(BaseRepository[Folder]):
    def __init__(self, db: Session):
        super().__init__(Folder, db)

    def get_by_name(self, folder_name: str) -> Folder | None:
        return self.db.query(self.model).filter(self.model.folder_name == folder_name).first()

    def create(self, folder_data: FolderBase) -> FolderDto:
        folder = Folder(**folder_data.model_dump())
        self.db.add(folder)
        self.db.commit()
        self.db.refresh(folder)
        return FolderDto.model_validate(folder)
