import json

import questionary
from questionary import Choice

from src.automation.action_registry import ACTION_TYPES
from src.core.enums import HuntMenu
from src.database.models import Hunt
from src.database.repositories import PokemonHuntRepository as hunt_db
from src.database.repositories.PokemonHuntRepository import (
    get_all_hunts,
)


def get_start_menu_choice():
    print()

    available_hunts = True if len(hunt_db.get_all_hunts_by_finish_status()) > 0 else False

    continue_hunt = [HuntMenu.CONTINUE] if hunt_db.get_latest_hunt() else []
    resume_hunt = [HuntMenu.RESUME] if available_hunts else []

    # fmt: off
    menu_options = (
        continue_hunt
        + resume_hunt
        + [HuntMenu.START]
        + ([HuntMenu.SHOW, HuntMenu.DELETE] if available_hunts else [])
        + [HuntMenu.QUIT]
    )

    choices = [Choice(f"{i}. {opt.value}", value=opt) for i, opt in enumerate(menu_options, start=1)]

    return questionary.select(message="Menu:", choices=choices).ask()


def get_actions_menu_choice():
    action_list = [v["type"] for v in ACTION_TYPES.values() if v["action"] is not None]

    choices = [Choice(f"{i+1}: {action_type.value} hunt", value=action_type) for i, action_type in enumerate(action_list)]
    choices.append(Choice(title=HuntMenu.BACK.value, value=HuntMenu.BACK))

    return questionary.select(
        message="Please select one of the following automation options:\n\nShiny hunting method:\n=======================",
        choices=choices,
    ).ask()

    # # "\n======================="
    # # "\n\nOther automations:"
    # # "\n======================="
    # # "\n8: "
    # print("=======================" "\n0: Quit")


def print_all_hunts(hunt: Hunt = None, formatted: bool = True, show_id=False):
    """
    :param hunt: Hunt object that is used to print a singular instance, else all hunts are displayed
    :param formatted: When True => Print clean, named dict attribute names and key names are formatted into title case.
                        When False => Print raw json object.
    :param show_id: Whether or not to display the id's for the DB entries.
    """
    if hunt:
        db_obj_print([hunt], formatted, show_id)
    else:
        hunts = get_all_hunts()
        if len(hunts) > 0:
            db_obj_print(hunts, formatted, show_id)
        else:
            print("No hunts recorded.")


def db_obj_print(hunts: list[Hunt], formatted=True, show_id=False):
    excluded_fields = set() if show_id else {"id"}

    if len(hunts) > 1:
        print(f"\n======================= Entries: {len(hunts)} =======================")
    else:
        print("\n")
    print("----------------------------------------------------------")

    for h in reversed(hunts):
        if formatted:
            for k, v in hunt_obj_to_dict(h, excluded_fields).items():
                formatted_key_name = str(k).replace("_", " ").title()
                print(f"{f'{formatted_key_name}:':26} {v}")
            print("----------------------------------------------------------")
        else:
            print_hunt_obj(h)


def hunt_obj_to_dict(obj, excluded_fields=None) -> dict:
    excluded_fields = excluded_fields or set()

    return {column.name: getattr(obj, column.name) for column in obj.__table__.columns if column.name not in excluded_fields}


def print_hunt_obj(obj: Hunt):
    print(json.dumps(hunt_obj_to_dict(obj), indent=2))


def print_map(grid):
    """
    Prints the grid map in the console
    :param grid: Grid map
    """
    for row in grid:
        print(" ".join(str(v) for v in row))


def generate_hunt_log(hunts: list[Hunt], select_hunt_message, display_finished_status=False):
    display_fields = {
        "pokemon_name": ("Pokémon", 10, "<", str),
        "start_date": ("Start Date", 19, "^", str),
        "last_time_hunted_date": ("Last Time Hunted", 19, "<", str),
        "hunt_mode": ("Hunt Mode", 12, "<", str),
        "total_encounters": ("Total Enc.", 11, "<", str),
        "target_pokemon_encounters": ("Target Enc.", 12, "<", str),
    }

    if display_finished_status:
        display_fields["finished"] = ("Finished", 5, "<", lambda value: str("✅" if value else "❌"))

    # Order of Magnitude capacity (filler space)
    hunt_OoM = 4

    # Generate header
    header = " ".join([f"{'#':<{hunt_OoM}}"] + [f"{name:{alignment}{width}}" for (name, width, alignment, _) in display_fields.values()])
    separator = "=" * len(header)

    # Generate select message
    # fmt: off
    active_hunts_header = (
        f"{select_hunt_message}"
        "\nActive Pokémon hunts:"
        f"\n   {separator}"
        f"\n   {header}"
        f"\n   {separator}"
    )

    # Generate choices
    hunt_log = [
        Choice(
            title=" ".join(
                [f"{i:<{hunt_OoM}}"] + [f"{convert(getattr(entry, field)):{alignment}{width}}" for field, (_, width, alignment, convert) in display_fields.items()]
            ),
            value=entry.id,
        )
        for i, entry in enumerate(hunts, start=1)
    ]

    hunt_log.append(Choice(HuntMenu.BACK.value, HuntMenu.BACK))

    return active_hunts_header, hunt_log
