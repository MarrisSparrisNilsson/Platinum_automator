from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.models import Base
from src.definitions import SRC_DIR

_db_name = "platinum_automator"
_db_file_path = SRC_DIR.parent / f"data/{_db_name}.db"
_DATABASE_URL = f"sqlite:///{str(_db_file_path)}"

# Run this once during startup.
_engine = create_engine(_DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False)


# From using your db init code:
def initialize_db():
    if not isinstance(_db_file_path, Path) or _db_name == "":
        raise ValueError("No save location provided for _db_file_path.")

    if not _db_file_path.exists():
        print("No existing DB. Initializing a new one.")
        _db_file_path.touch()

    Base.metadata.create_all(_engine)
    return _engine


def print_db_path():
    print(_db_file_path)
