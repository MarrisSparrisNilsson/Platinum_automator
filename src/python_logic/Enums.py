from enum import Enum


class EncounterTimeout(Enum):
    REGULAR = 4
    LEGENDARY = 3


class HuntMode(Enum):
    REGULAR = "Regular"
    POKERADAR = "Pokeradar"
    SOFT_RESET = "Soft Reset"
    FISHING = "Fishing"
    FOSSIL = "Fossil"
    SAFARI_ZONE = "Safari zone"
    EGG = "Egg"


class WalkTypes(Enum):
    RANDOM = "Walk random"
    CIRCLES = "Walk in circles"
    UP_DOWN = "Walk up and down"
    LEFT_RIGHT = "Walk left and right"


class FishingTypes(Enum):
    REGULAR = "Regular fishing"
    FEEBAS = "Feebas hunt"
