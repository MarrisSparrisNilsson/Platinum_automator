import pytest

import src.database.repositories.PokemonHuntRepository as hunt_db

# from definitions import SRC_DIR
from src.database.database import initialize_db

# db_path = SRC_DIR.parent / "data/platinum_automator.db"


@pytest.fixture
def init_db():
    initialize_db()


def test_print_hunts(init_db):
    print(hunt_db.get_all_hunts())


def test_increment_encounters(init_db):
    hunt_id = "5a4394c4-1be4-4c78-a6e2-2e8f189264a6"
    hunt = hunt_db.get_hunt_by_id(hunt_id)
    total_encounters = hunt.total_encounters

    amount = -1
    updated_encounters = hunt_db.increment_encounters(hunt_id, amount)
    print("\nUpdated_encounters:", total_encounters, "->", updated_encounters)

    assert total_encounters + amount == updated_encounters
