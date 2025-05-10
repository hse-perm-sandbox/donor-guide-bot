from src.database.seeds.folders import seed_folders
from src.database.seeds.questions import seed_questions

if __name__ == "__main__":
    seed_folders()
    seed_questions()