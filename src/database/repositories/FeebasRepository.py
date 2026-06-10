from src.database.database import SessionLocal
from src.database.models import Feebas
from src.python_logic.file_manager import get_date

'''
THIS FILE CONTAINS DATABASE CRUD OPERATIONS FOR FEEBAS HUNT TRACKING
'''

# Single row table
SINGLETON_ID = 1


def init_feebas_tracking():
    # A temporary workspace for database operations.
    with SessionLocal() as session:
        feebas_state = session.get(Feebas, SINGLETON_ID)
        if feebas_state is None:
            feebas_state = Feebas(
                id=SINGLETON_ID,
                found_at=0,
                latest_tile=0,
                found_date="",
                current_date=get_date()
            )
            session.add(feebas_state)
            session.commit()
        else:
            print("Feebas tracking already initialized.")


def get_feebas_state():
    with SessionLocal() as session:
        return session.get(Feebas, 1)


def reset_feebas_state(date):
    with SessionLocal() as session:
        feebas_state = session.get(Feebas, SINGLETON_ID)
        feebas_state.latest_tile = 0
        feebas_state.found_at = 0
        feebas_state.current_date = date
        session.commit()


def increment_tile_count_tracking(amount: int = 1):
    with SessionLocal() as session:
        feebas_state = session.get(Feebas, SINGLETON_ID)
        feebas_state.latest_tile += amount
        session.commit()


def update_feebas_hunt_date():
    with SessionLocal() as session:
        feebas_state = session.get(Feebas, SINGLETON_ID)
        feebas_state.current_date = get_date()
        session.commit()


def update_feebas_found(tile: int):
    with SessionLocal() as session:
        feebas_state = session.get(Feebas, SINGLETON_ID)
        feebas_state.found_date = get_date()
        feebas_state.found_at = tile
        session.commit()
