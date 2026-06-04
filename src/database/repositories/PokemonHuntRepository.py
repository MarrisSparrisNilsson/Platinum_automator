from src.database.database import SessionLocal
from src.database.models import Hunt
from src.python_logic.file_manager import get_date


'''
THIS FILE CONTAINS DATABASE CRUD OPERATIONS FOR POKEMON HUNTS
'''


def get_all_hunts() -> [Hunt]:
    with SessionLocal() as session:
        return session.query(Hunt).all()


def get_latest_hunt() -> Hunt:
    with SessionLocal() as session:
        return (
            session.query(Hunt)
            .order_by(Hunt.last_time_hunted_date.desc())
            .first()
        )


def get_hunt_by_id(hunt_id):
    with SessionLocal() as session:
        return (
            session.query(Hunt)
            .filter(Hunt.id == hunt_id)
            .first()
        )


def create_hunt(hunt: Hunt):
    with SessionLocal() as session:
        session.add(hunt)
        session.commit()


def update_encounters(hunt_id, total_encounters, target_encounters, last_hunted_date):
    with SessionLocal() as session:
        hunt = (
            session.query(Hunt)
            .filter(Hunt.id == hunt_id)
            .first()
        )
        if hunt is None:
            return False

        hunt.total_encounters = total_encounters
        hunt.target_pokemon_encounters = target_encounters
        hunt.last_time_hunted_date = last_hunted_date

        session.commit()

        return True


def increment_encounters(hunt_id: str, amount: int = 1):
    with SessionLocal() as session:
        hunt = (
            session.query(Hunt)
            .filter(Hunt.id == hunt_id)
            .first()
        )
        total_encounters = hunt.total_encounters + amount
        hunt.total_encounters = total_encounters

        session.commit()

        return total_encounters


def increment_target_encounters(hunt_id: str, amount: int = 1):
    with SessionLocal() as session:
        hunt = (
            session.query(Hunt)
            .filter(Hunt.id == hunt_id)
            .first()
        )
        target_encounters = hunt.target_pokemon_encounters + amount
        hunt.target_pokemon_encounters = target_encounters

        session.commit()

        return target_encounters


def finish_hunt(hunt_id):
    with SessionLocal() as session:
        hunt = (
            session.query(Hunt)
            .filter(Hunt.id == hunt_id)
            .first()
        )
        if hunt is None:
            return False

        hunt.finished = True
        hunt.end_date = get_date("YYYY-MM-DD HH:MM")
        session.commit()

        return True


def delete_hunt(hunt_id):
    with SessionLocal() as session:
        hunt = (
            session.query(Hunt)
            .filter(Hunt.id == hunt_id)
            .first()
        )
        if hunt is None:
            return False

        session.delete(hunt)
        session.commit()

        return True
