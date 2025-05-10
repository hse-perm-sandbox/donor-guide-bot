from src.database.database import get_session
from src.database.models.folder import Folder

def get_or_create_folder(session, name, parent_id=None):
    folder = (
        session.query(Folder)
        .filter_by(folder_name=name, parent_id=parent_id)
        .first()
    )
    if folder:
        return folder
    folder = Folder(folder_name=name, parent_id=parent_id)
    session.add(folder)
    session.commit()
    return folder

def seed_folders():
    session = next(get_session())

    bone = get_or_create_folder(session, "🧬 Донорство костного мозга")
    blood = get_or_create_folder(session, "🩸 Донорство крови")
    contacts = get_or_create_folder(session, "📞 Контакты фонда")

    bone_subs = [
        "📁 Что нужно знать",
        "📁 Как стать донором",
        "📁 Как проходит донация",
        "📁 Часто задаваемые вопросы",
    ]
    for name in bone_subs:
        get_or_create_folder(session, name, parent_id=bone.id)

    blood_subs = [
        "📁 Как подготовиться",
        "📁 После донации",
        "📁 Противопоказания",
        "📁 Часто задаваемые вопросы",
        "📁 Как это помогает",
        "📁 Узнать, нужны ли доноры"
    ]
    for name in blood_subs:
        get_or_create_folder(session, name, parent_id=blood.id)

    print("Папки успешно добавлены")

if __name__ == "__main__":
    seed_folders()
