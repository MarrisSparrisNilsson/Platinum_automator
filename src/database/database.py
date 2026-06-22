from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from src.database.models import Base

_db_name = "platinum_automator"
_path = Path().cwd().parent / f"data/{_db_name}.db"
_DATABASE_URL = f"sqlite:///{_path}"

# Run this once during startup.
_engine = create_engine(_DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False)


# From using your db init code:
def initialize_db():
    file_path = Path(_path)
    if not file_path.exists():
        print("No existing DB. Initializing a new one.")
        file_path.touch()

    Base.metadata.create_all(_engine)


def print_db_path():
    file_path = Path(_path)
    print(file_path)
