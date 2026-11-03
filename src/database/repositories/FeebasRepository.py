from src.database.database import SessionLocal
from src.database.models import Feebas
from src.utils.helpers import get_date

"""
THIS FILE CONTAINS DATABASE CRUD OPERATIONS FOR FEEBAS HUNT TRACKING
"""

# Single row table
SINGLETON_ID = 1


def init_feebas_tracking():
    with SessionLocal() as session:
        feebas_state = session.get(Feebas, SINGLETON_ID)
        if feebas_state is None:
            feebas_state = Feebas(
                id=SINGLETON_ID,
                found_at=0,
                latest_tile=0,
                furthest_tile_reached_today=0,
                found_date="",
                current_date=get_date(),
                non_cleared_tiles=[],
            )
            session.add(feebas_state)
            session.commit()
        else:
            print("Feebas tracking already initialized.")


def get_feebas_state():
    with SessionLocal() as session:
        feebas_state = session.get(Feebas, SINGLETON_ID)
        if feebas_state is None:
            raise ValueError("Feebas state does not exist in database!")

        return {column.name: getattr(feebas_state, column.name) for column in Feebas.__table__.columns}


def reset_feebas_state(date):
    with SessionLocal() as session:
        feebas_state = session.get(Feebas, SINGLETON_ID)

        if feebas_state is None:
            raise ValueError("Feebas state does not exist in database!")

        feebas_state.latest_tile = 0
        feebas_state.non_cleared_tiles = []

        if feebas_state.current_date != date:
            feebas_state.furthest_tile_reached_today = 0

        feebas_state.found_at = 0
        feebas_state.current_date = date
        session.commit()
        return {column.name: getattr(feebas_state, column.name) for column in Feebas.__table__.columns}


def increment_tile_count_tracking(tile, tile_ranges: list[tuple[int, int]]):
    with SessionLocal() as session:
        feebas_state = session.get(Feebas, SINGLETON_ID)

        if feebas_state is None:
            raise ValueError("Feebas state does not exist in database!")

        feebas_state.latest_tile = tile
        feebas_state.non_cleared_tiles = tile_ranges

        # print("Latest_tile:", feebas_state.latest_tile)
        # print("Tile:", tile)
        # print(f"{tile} > {feebas_state.furthest_tile_reached_today}:", tile > feebas_state.furthest_tile_reached_today)
        feebas_state.furthest_tile_reached_today = (
            tile if tile > feebas_state.furthest_tile_reached_today else feebas_state.furthest_tile_reached_today
        )
        session.commit()


# def update_feebas_hunt_date():
#     with SessionLocal() as session:
#         feebas_state = session.get(Feebas, SINGLETON_ID)
#         feebas_state.current_date = get_date()
#         session.commit()


def update_feebas_found(tile: int):
    with SessionLocal() as session:
        feebas_state = session.get(Feebas, SINGLETON_ID)
        if feebas_state is None:
            raise ValueError("Feebas state does not exist in database!")

        feebas_state.found_date = get_date()
        feebas_state.found_at = tile
        session.commit()


def delete_feebas_info():
    with SessionLocal() as session:
        feebas_state = session.get(Feebas, SINGLETON_ID)

        if feebas_state is None:
            raise ValueError("Feebas state does not exist in database!")

        session.delete(feebas_state)
        session.commit()

        return True
