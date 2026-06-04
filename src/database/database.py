from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

path = Path().cwd().parent.parent / "data/platinum_automator.db"
DATABASE_URL = f"sqlite:///{path}"
# Run this once during startup.
engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# From using your db init code:
# def initialize_database():
#     Base.metadata.create_all(engine)
#
# main():
#     initialize_database()
# I get:
# sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) unable to open database file.
