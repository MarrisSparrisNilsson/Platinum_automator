from src.automation.actions import fishing_hunt, soft_reset_hunt, egg_hunt, regular_hunt
from src.core.enums import HuntMode, FishingTypes, WalkTypes
from src.encounter_methods import fishing, regular

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
                "number": 1,
                "method_name": f"{FishingTypes.REGULAR.value}",
                "method": fishing.fishing,
                "args": True  # Continue infinitely
            },
            {
                "number": 2,
                "method_name": f"{FishingTypes.FEEBAS.value}",
                "method": fishing.feebas_fishing,
                "args": None
            }
        ]
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
                "number": 1,
                "method_name": f"{WalkTypes.RANDOM.value}",
                "method": regular.walk_random,
                "args": None
            },
            {
                "number": 2,
                "method_name": f"{WalkTypes.CIRCLES.value}",
                "method": regular.lets_try_spinning,
                "args": 1
            }
        ]
    }
}
