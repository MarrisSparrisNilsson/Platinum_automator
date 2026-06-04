from sqlalchemy.orm import declarative_base
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import Date

Base = declarative_base()


class Hunt(Base):
    __tablename__ = "hunts"

    id = Column(String, primary_key=True)
    pokemon_name = Column(String, nullable=False)
    hunt_mode = Column(String, nullable=False)
    hunt_method = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    last_time_hunted_date = Column(String, default="")
    end_date = Column(String, default="")
    total_encounters = Column(Integer, default=0)
    target_pokemon_encounters = Column(Integer, default=0)
    is_practice = Column(Boolean, default=False)
    finished = Column(Boolean, default=False)


class Feebas(Base):
    __tablename__ = "feebas"

    id = Column(Integer, primary_key=True)

    found_at = Column(Integer, nullable=False, default=0)
    latest_tile = Column(Integer, nullable=False, default=0)
    found_date = Column(String)
    current_date = Column(String, nullable=False)
