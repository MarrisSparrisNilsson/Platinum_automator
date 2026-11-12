import threading as thread
import time

import emoji
import questionary
from questionary import Choice

from src.automation import actions
from src.automation.action_registry import ACTION_TYPES
from src.core.enums import HuntMenu, HuntMode
from src.database.models import Hunt
from src.database.repositories import PokemonHuntRepository as hunt_db
from src.database.repositories.PokemonHuntRepository import get_latest_hunt
from src.states.Hunt import HuntStateManager
from src.UI.CLI.cli_helpers import (
    generate_hunt_log,
    get_actions_menu_choice,
    get_start_menu_choice,
    print_all_hunts,
    print_hunt_obj,
)
from src.utils.helpers import get_date


def select_menu_option() -> thread.Thread:
    hunt_manager = HuntStateManager.get_instance()

    while True:
        try:
            option = get_start_menu_choice()

            match option:
                case HuntMenu.CONTINUE:
                    hunt = get_latest_hunt()
                    print_all_hunts(hunt)

                    do_proceed = questionary.confirm("Do you want to continue this hunt?", auto_enter=False).ask()
                    if do_proceed:

                        date_match: int = str(hunt.last_time_hunted_date).find(get_date("%Y-%m-%d"))
                        if date_match != -1:
                            hunt_manager.set_was_hunted_today(True)

                        hunt_mode = hunt.hunt_mode
                        hunt_method = hunt.hunt_method

                        hunt_manager.set_hunt_state(
                            hunt_id=hunt.id,
                            pokemon_name=hunt.pokemon_name,
                            hunt_mode=hunt_mode,
                            hunt_method=hunt_method,
                            is_practice=hunt.is_practice or False,
                        )
                        return load_action(hunt_mode, hunt_method)

                case HuntMenu.RESUME:
                    hunt = select_hunt("Please select one hunt to resume:")
                    if hunt == HuntMenu.BACK:
                        continue

                    hunt_mode = hunt.hunt_mode
                    hunt_method = hunt.hunt_method

                    hunt_manager.set_hunt_state(
                        hunt_id=hunt.id,
                        pokemon_name=hunt.pokemon_name,
                        hunt_mode=hunt_mode,
                        hunt_method=hunt_method,
                        is_practice=hunt.is_practice or False,
                    )
                    return load_action(hunt_mode, hunt_method)

                case HuntMenu.START:
                    pokemon_name = questionary.text(message="Which Pokémon are you hunting?:").ask()

                    action_thread = select_action()
                    if action_thread is None:
                        continue

                    is_practice = questionary.confirm("Is this a practice run? (Default=False)", default=False).ask()
                    hunt_manager.set_hunt_state(pokemon_name, is_practice=is_practice)

                    # Create new hunt and add to DB
                    hunt_id, pokemon_name, hunt_mode, hunt_method, is_practice = hunt_manager.get_hunt_state()

                    hunt = Hunt(
                        id=hunt_id,
                        pokemon_name=pokemon_name,
                        hunt_mode=hunt_mode,
                        hunt_method=hunt_method,
                        start_date=get_date("%Y-%m-%d %H:%M"),
                        is_practice=is_practice,
                    )
                    hunt_db.create_hunt(hunt)
                    # print(f"Beginning {hunt_mode} hunt!")
                    return action_thread

                case HuntMenu.SHOW:
                    hunt = select_hunt("Select one to inspect:", display_finished_status=True)
                    # hunt_db.get_all_hunts_by_finish_status()

                    # print_all_hunts()

                case HuntMenu.DELETE:
                    hunt = select_hunt("Please select one record to be deleted:", False)
                    if hunt == HuntMenu.BACK:
                        continue

                    for i in range(3):
                        emphasis = " REALLY" if i == 1 and i > 0 else " 100%"
                        ans = questionary.confirm(
                            f"Are you{'' if i == 0 else emphasis} sure you want to delete this {hunt.pokemon_name} hunt?",
                            default=False,
                            auto_enter=False,
                        ).ask()
                        if not ans:
                            raise PermissionError("Deletion canaled.")

                    if hunt_db.delete_hunt(hunt.id):
                        print(f"{hunt.pokemon_name} hunt: id({hunt.id}) was deleted.")
                    else:
                        print("Deletion failed.")

                case HuntMenu.QUIT:
                    exit(0)
                case _:
                    print("Invalid option, try again.")

        except FileExistsError:
            print("No save data available.")
        except (ValueError, AttributeError, PermissionError) as e:
            print(e)
        time.sleep(0.2)


def select_hunt(select_hunt_message: str, hide_raw_details=True, display_finished_status=False) -> Hunt | None:
    # fmt: off
    hunts: list[Hunt] = (hunt_db.get_all_hunts_by_finish_status() 
                        if not display_finished_status 
                        else hunt_db.get_all_hunts())

    if not len(hunts) > 0:
        print("No hunts recorded.")
        return HuntMenu.BACK

    active_hunts_header, hunt_log = generate_hunt_log(hunts, select_hunt_message, display_finished_status)

    hunt_id = questionary.select(
        message=active_hunts_header,
        choices=hunt_log,
        show_selected=True,
    ).ask()

    if hunt_id == HuntMenu.BACK:
        return HuntMenu.BACK
    else:
        if not hide_raw_details:
            hunt = hunt_db.get_hunt_by_id(hunt_id)
            print_hunt_obj(hunt)
        return hunt_db.get_hunt_by_id(hunt_id)


def select_action() -> thread.Thread | None:
    hunt_manager = HuntStateManager.get_instance()
    action = method = args = None

    try:
        hunt_mode: HuntMenu | HuntMode = get_actions_menu_choice()

        if hunt_mode == HuntMenu.BACK:
            return None

        method, args, method_name = select_search_func(hunt_mode.value)
        hunt_manager.set_hunt_mode(hunt_mode.value, method_name)

        action = ACTION_TYPES[hunt_mode.value]["action"]

        if action is not None:

            return thread.Thread(
                target=action,
                name="___action_thread___",
                args=[method, args],
                daemon=True,
            )
        raise ValueError("The selected action could not be found.")

    except ValueError as e:
        print(e)
        return None


def select_search_func(hunt_mode: str) -> tuple[str, any, str]:
    methods = ACTION_TYPES[hunt_mode]["methods"]

    ans = questionary.select(
        message="Please select any of the search methods:",
        choices=[Choice(title=f"{num+1}: {method['method_name']}", value=num) for num, method in enumerate(methods)],
    ).ask()

    method = methods[ans]["method"]
    args = methods[ans]["args"]
    method_name = methods[ans]["method_name"]

    if method is None:
        raise ValueError("This method is currently unavailable, try again.")
    else:
        return method, args, method_name


def load_action(hunt_mode, hunt_method) -> thread.Thread:
    action = ACTION_TYPES[hunt_mode]["action"]
    method = None
    args = None
    method_name = ""

    if ACTION_TYPES[hunt_mode]["method_required"]:
        for method_obj in ACTION_TYPES[hunt_mode]["methods"]:
            if method_obj["method_name"] == hunt_method:
                method = method_obj["method"]
                args = method_obj["args"]
                method_name = method_obj["method_name"]

        if method is None:
            method, args, method_name = select_search_func(hunt_mode)

    HuntStateManager.get_instance().set_hunt_mode(hunt_mode, method_name)
    return thread.Thread(
        target=action,
        name="___action_thread___",
        args=[method, args],
        daemon=False,
    )
