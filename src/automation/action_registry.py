from src.automation.actions import egg_hunt, fishing_hunt, regular_hunt, soft_reset_hunt
from src.core.enums import FishingTypes, HuntMode, WalkTypes
from src.encounter_methods import regular
from src.encounter_methods.Fishing import fishing
from src.encounter_methods.Fishing.Feebas import feebas

ACTION_TYPES = {
    f"{HuntMode.POKERADAR.value}": {
        "action": None,
        "method_required": True,
    },
    f"{HuntMode.FISHING.value}": {
        "action": fishing_hunt,
        "method_required": True,
        "methods": [
            {
                "method_name": f"{FishingTypes.REGULAR.value}",
                "method": fishing.fishing,
                "args": -1,  # Continue infinitely
            },
            {
                "method_name": f"{FishingTypes.FEEBAS.value}",
                "method": feebas.feebas_fishing,
                "args": 2,  # Fish 2 times per tile
            },
        ],
    },
    f"{HuntMode.FOSSIL.value}": {
        "action": None,
        "method_required": True,
    },
    f"{HuntMode.SAFARI_ZONE.value}": {
        "action": None,
        "method_required": True,
    },
    f"{HuntMode.SOFT_RESET.value}": {
        "action": soft_reset_hunt,
        "method_required": False,
    },
    f"{HuntMode.EGG.value}": {
        "action": egg_hunt,
        "method_required": False,
    },
    f"{HuntMode.REGULAR.value}": {
        "action": regular_hunt,
        "method_required": True,
        "methods": [
            {
                "method_name": f"{WalkTypes.RANDOM.value}",
                "method": regular.walk_random,
                "args": None,
            },
            {
                "method_name": f"{WalkTypes.CIRCLES.value}",
                "method": regular.lets_try_spinning,
                "args": 1,
            },
        ],
    },
}
