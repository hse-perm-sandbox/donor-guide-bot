from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models.folder import Folder
from src.database.models.question import Question
from src.database.repositories.base import BaseRepository
from src.schemas.folder import FolderBase, FolderDto, FolderWithContentDto


class FolderRepository(BaseRepository[Folder]):
    def __init__(self, db: Session):
        super().__init__(Folder, db)

    def get_by_parent(self, parent_id: int | None):
        return (
            self.db.query(self.model)
            .filter(self.model.parent_id == parent_id)
            .order_by(self.model.id)
            .all()
        )

    def get_by_id(self, folder_id: int):
        return self.db.query(self.model).get(folder_id)

    def get_by_name(self, folder_name: str) -> Folder | None:
        return self.db.query(self.model).filter(self.model.folder_name == folder_name).first()

    def create(self, folder_data: FolderBase) -> FolderDto:
        folder = Folder(**folder_data.model_dump())
        self.db.add(folder)
        self.db.commit()
        self.db.refresh(folder)
        return FolderDto.model_validate(folder)

    def get_folder_with_content(self, folder_id: int) -> FolderWithContentDto:
        """Получить каталог с активными подкаталогами и вопросами"""
        folder = (
            self.db.query(Folder)
            .options(
                joinedload(Folder.subfolders),
                joinedload(Folder.questions),
            )
            .filter(and_(Folder.id == folder_id, Folder.is_active == True))
            .first()
        )

        folder.subfolders = [sf for sf in folder.subfolders if sf.is_active]
        folder.questions = [q for q in folder.questions if q.is_active]

        return FolderDto.model_validate(folder)

    def get_root_folder_with_content(self) -> FolderWithContentDto:
        """
        Получает виртуальный корневой каталог, содержащий:
        - все каталоги без parent_id (is_active=True)
        - все вопросы без folder_id (is_active=True)
        """
        root_folders = (
            self.db.query(Folder)
            .filter(and_(Folder.parent_id.is_(None), Folder.is_active == True))
            .all()
        )

        root_questions = (
            self.db.query(Question)
            .filter(and_(Question.folder_id.is_(None), Question.is_active == True))
            .all()
        )

        return FolderWithContentDto.model_validate(
            {
                "id": 0,
                "folder_name": "Root",
                "parent_id": None,
                "is_active": True,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "subfolders": root_folders,
                "questions": root_questions,
            }
        )
