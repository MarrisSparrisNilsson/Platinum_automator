from enum import Enum


class EncounterTimeout(Enum):
    REGULAR = 4
    LEGENDARY = 3


class UtilityItems(Enum):
    NULL = "NULL"
    REPEL = "REPEL"
    SUPER_REPEL = "SUPER_REPEL"
    MAX_REPEL = "MAX_REPEL"
    BIKE = "BIKE"
    POKERADAR = "POKERADAR"
    OLD_ROD = "OLD_ROD"
    GOOD_ROD = "GOOD_ROD"
    SUPER_ROD = "SUPER_ROD"


class InGameMenuSlots(Enum):
    POKEDEX = 0
    POKEMON = 1
    BAG = 2
    TRAINER_CARD = 3
    SAVE = 4
    OPTIONS = 5
    EXIT = 6


class BagSlots(Enum):
    ITEMS = 0
    MEDICINE = 1
    POKE_BALLS = 2
    TM = 3
    BERRIES = 4
    MAIL = 5
    BATTLE_ITEMS = 6
    KEY_ITEMS = 7


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
