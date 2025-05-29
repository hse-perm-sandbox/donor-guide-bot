from src.database.database import get_session
from src.database.models.question import Question
from src.database.models.folder import Folder
from src.database.seeds.questions_data import questions_data

def get_folder_id(session, folder_name: str, parent_name: str | None = None) -> int:
    query = session.query(Folder).filter(Folder.folder_name == folder_name)
    if parent_name is not None:
        parent_folder = session.query(Folder).filter(Folder.folder_name == parent_name).first()
        if not parent_folder:
            raise ValueError(f"Родительская папка '{parent_name}' не найдена")
        query = query.filter(Folder.parent_id == parent_folder.id)
    else:
        query = query.filter(Folder.parent_id.is_(None))

    folder = query.first()
    if not folder:
        raise ValueError(f"Папка '{folder_name}' не найдена")
    return folder.id

def seed_questions():
    session = next(get_session())
    for item in questions_data:
        folder_id = get_folder_id(session, item["folder"], item.get("parent"))
        exists = session.query(Question).filter_by(
            question=item["question"],
            folder_id=folder_id
        ).first()
        if exists:
            continue
        q = Question(
            question=item["question"],
            answer_text=item["answer"],
            folder_id=folder_id,
            answer_picture_path = item.get("picture_name") or None,
            answer_file_id=None,
            is_active=True,
        )
        session.add(q)
    session.commit()
    print("Вопросы добавлены")

if __name__ == "__main__":
    seed_questions()