from src.automation.actions import egg_hunt, fishing_hunt, regular_hunt, soft_reset_hunt
from src.core.enums import FishingTypes, HuntMode, WalkTypes
from src.encounter_methods import regular
from src.encounter_methods.Fishing import fishing
from src.encounter_methods.Fishing.Feebas import feebas

ACTION_TYPES = {
    HuntMode.POKERADAR.value: {
        "type": HuntMode.POKERADAR,
        "action": None,
        "method_required": True,
    },
    HuntMode.FISHING.value: {
        "type": HuntMode.FISHING,
        "action": fishing_hunt,
        "method_required": True,
        "methods": [
            {
                "method_name": FishingTypes.REGULAR.value,
                "method": fishing.fishing,
                "args": -1,  # Continue infinitely
            },
            {
                "method_name": FishingTypes.FEEBAS.value,
                "method": feebas.feebas_fishing,
                "args": 2,  # Fish 2 times per tile
            },
        ],
    },
    HuntMode.FOSSIL.value: {
        "type": HuntMode.FOSSIL,
        "action": None,
        "method_required": True,
    },
    HuntMode.SAFARI_ZONE.value: {
        "type": HuntMode.SAFARI_ZONE,
        "action": None,
        "method_required": True,
    },
    HuntMode.SOFT_RESET.value: {
        "type": HuntMode.SOFT_RESET,
        "action": soft_reset_hunt,
        "method_required": False,
    },
    HuntMode.EGG.value: {
        "type": HuntMode.EGG,
        "action": egg_hunt,
        "method_required": False,
    },
    HuntMode.REGULAR.value: {
        "type": HuntMode.REGULAR,
        "action": regular_hunt,
        "method_required": True,
        "methods": [
            {
                "method_name": WalkTypes.RANDOM.value,
                "method": regular.walk_random,
                "args": None,
            },
            {
                "method_name": WalkTypes.CIRCLES.value,
                "method": regular.lets_try_spinning,
                "args": 1,
            },
        ],
    },
}
