from src.database.database import SessionLocal
from src.database.models import Hunt


def add_pokemon(name):
    with SessionLocal() as session:
        session.add(Hunt(name=name))
        session.commit()
