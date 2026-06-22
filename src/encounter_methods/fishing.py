import threading
import json
import time

from pathlib import Path

from src.utils.helpers import get_date
from src.vision.game_ui_detector import check_repel_status
from src.database.repositories import FeebasRepository as feebas_state
from src.automation import controls, in_game_menu_controls
from src.vision import encounter_detector
from src.core.Game import game_context
from src.states.Shutdown import ShutdownStateManager
from src.states.Pause import PauseStateManager
from src.states.Hunt import HuntStateManager
from src.core.enums import InGameMenuSlots, UtilityItems, FeebasHuntConfig


def fishing(args):
    cast = [0]
    encounters = [0]
    while args is True or encounters[0] < args:  # args is bool or int

        PauseStateManager.get_instance().check_pause_state("Fishing is paused▶️", "Fishing now continues🎣🪝")
        if ShutdownStateManager.get_instance().check_shutdown_state():
            return

        if in_game_menu_controls.use_registered_key_item():
            encounter_detector.find_exclamation_mark(cast, encounters)
        else:
            shutdown_state = ShutdownStateManager.get_instance()
            shutdown_event = threading.Event()
            print("Incorrect fishing spot!❌")
            shutdown_event.clear()  # Reset the internal flag to false (Shutting down)
            shutdown_state.set_state(shutdown_event)  # Updating state


def feebas_fishing(_):
    """
    Start point is located in the top right corner of the lake
    where you fish and then use surf.

    Map goes through every fish-able water tile

    Walk 'i' steps and turn towards i+1, then fish twice.

    Steps:

    1: Fish x2

    2: Take step, (Path[i])

    3: Turn towards next step if Path[i] != Path[i+1]
    """

    # Steps are determined by direction and edge of a tile that the path crosses.
    pause_main_event = threading.Event()
    pause_main_state = PauseStateManager.get_instance()

    game_context.set_dialog_pixels()

    pause_main_event.clear()  # Set internal flag to false (Pause)
    pause_main_state.set_main_state(pause_main_event)  # Pauses encounter automation

    # Construct the file path
    feebas_resource_path = Path(__file__).parent.parent.parent / "resources/feebas.json"

    todays_date = get_date("%Y-%m-%d")
    tiles = read_tiles(feebas_resource_path)
    time.sleep(0.2)  # Wait for pause_main_state print

    feebas_info = feebas_state.get_feebas_state()
    found_date = feebas_info.found_date
    # If Feebas has not been found today (New day)
    if not found_date == todays_date:
        was_found_today = False

        feebas_state.reset_feebas_state(todays_date)
        print("\nNew day has begun!"
              "\nFarthest reached position has been set to 0")
        fish_at_pos = feebas_info.latest_tile
    else:
        was_found_today = True
        fish_at_pos = feebas_info.found_at
        print(f"FEEBAS was last seen at step {fish_at_pos}❗")

    controls.switch_tab()
    walk_to_pos, new_fish_at_pos = feebas_hunt_configuration(fish_at_pos, len(tiles))
    controls.switch_tab()

    in_game_menu_controls.execute_inGame_menu_action(InGameMenuSlots.BAG, UtilityItems.MAX_REPEL)  # Use repel
    in_game_menu_controls.execute_inGame_menu_action(InGameMenuSlots.BAG, UtilityItems.GOOD_ROD)  # Register Good Rod

    encounters = 2  # Number of desired encounters

    go_to_new_start_pos = fish_at_pos < new_fish_at_pos
    start_pos = 0 if new_fish_at_pos == 0 or walk_to_pos and not go_to_new_start_pos else fish_at_pos

    # Ensure player is turned in the right direction
    if start_pos == 0:
        controls.move(tiles[0], 0)
    else:
        HuntStateManager.get_instance().set_facing_direction(tiles[start_pos])  # Set initial facing direction

    for tile in range(start_pos, len(tiles)):
        # if not was_found_today and not walk_to_pos:
        #     data['latest_tile'] = tile
        # f.seek(0)
        # json.dump(data, f, indent=2)

        separator = '\n'
        print("\r", end=f"Fishing at tile: {tile}{separator if not walk_to_pos else ''}")

        # =================================================================
        '''
        NOTE 1: Start fishing if current position index is greater or equal to assigned position 
                     and therefore is NOT assigned to walk anywhere (walk_to_pos=False)                             
        NOTE 2: Skip fishing as long as current position is less than assigned start position
        '''
        if tile >= new_fish_at_pos:
            # When new_fish_at_pos is reached and is not start position
            if tile == new_fish_at_pos:
                walk_to_pos = False
                print("\nFishing spot reached")

            # Continue static fishing when found_at location is reached
            if was_found_today:
                break

            # controls.switch_tab_DEBUG()
            pause_main_event.set()  # Set internal flag to true
            pause_main_state.set_main_state(pause_main_event)  # Resumes encounter automation
            time.sleep(1)
            fishing(encounters)
            time.sleep(3)
            PauseStateManager.get_instance().check_pause_state("Fishing is paused▶️", "Fishing and walking now continues🎣🪝")
            # controls.switch_tab_DEBUG()

            # If Feebas was found
            was_found_today = HuntStateManager.get_instance().get_target_pokemon_found()
            if was_found_today:
                feebas_state.update_feebas_found(tile)
                break  # Break walking progression

        if ShutdownStateManager.get_instance().check_shutdown_state():
            return

        # =================================================================

        if tile == 0:
            controls.surf()
            time.sleep(1.5)
        else:

            walk_dir = tiles[tile]
            turn_dir = tiles[tile + 1 if (tile + 1) < len(tiles) else tile]

            if take_step(tile):
                controls.move(walk_dir, 1)  # Step

            # If a new repel was activated, and we should continue fishing instead of walking
            if check_repel_status() and not walk_to_pos:
                pause_main_event.set()  # Set internal flag to true
                pause_main_state.set_main_state(pause_main_event)  # Resumes encounter automation

            # Prevents double steps and overstepping
            if not take_step(tile) or not turn_dir == walk_dir:
                controls.move(turn_dir, 0)  # Turn

            if not was_found_today and not walk_to_pos:
                # data['latest_tile'] = tile + 1
                feebas_state.increment_tile_count_tracking()

            if ShutdownStateManager.get_instance().check_shutdown_state():
                return
            # =================================================================

    if was_found_today:
        pause_main_event.set()  # Set internal flag to true
        pause_main_state.set_main_state(pause_main_event)  # Resumes encounter automation
        # Feebas has been found (keep fishing)
        while True:
            if not todays_date == get_date("%Y-%m-%d"):
                shutdown_state = ShutdownStateManager.get_instance()
                shutdown_event = threading.Event()
                print("\nTime is past midnight🌙"
                      "\nGo back to start position and try again.")
                shutdown_event.clear()  # Reset the internal flag to false (Shutting down)
                shutdown_state.set_state(shutdown_event)  # Updating state
                return
            else:
                fishing(1)
    else:
        shutdown_state = ShutdownStateManager.get_instance()
        shutdown_event = threading.Event()
        print("\nAt the end of the path⛔\nNo Feebas found❌\nGo back to start position and try again!↩️")
        shutdown_event.clear()  # Reset the internal flag to false (Shutting down)
        shutdown_state.set_state(shutdown_event)  # Updating state
        pause_main_event.set()  # Get out of lock
        pause_main_state.set_main_state(pause_main_event)
        return


def read_tiles(feebas_resource_path):
    try:
        # Open the file
        with (open(feebas_resource_path, "r") as f):
            file = json.load(f)
            tiles = file["path"]
            return tiles
    except json.decoder.JSONDecodeError:
        print(f"Something went wrong with the resource file: {feebas_resource_path}")
        exit(-1)


def take_step(tile):
    """
    Blocks walking at some locations where only turning is desired.
    :param tile: Tile number along the predefined path.
    :return: False => Don't move. True => Move.
    """
    if (tile == 3 or tile == 29 or tile == 93 or
            tile == 98 or tile == 102 or tile == 222 or
            tile == 323 or tile == 455 or tile == 457 or
            tile == 483 or tile == 521 or tile == 527):
        return False
    else:
        return True


def feebas_hunt_configuration(fish_at_pos: int, tot_tiles: int) -> (bool, int):
    """
    Prints the hunt configuration options and returns hunt configurations based on user input.

    :param fish_at_pos: Current position on the tile path
    :param tot_tiles: Total fish-able tiles in the pond
    :return: Walk_to_pos (bool), fish_at_pos (int)
    """
    menu_options = feebas_hunt_configuration_menu(
        fish_at_pos,
        tot_tiles
    )

    while True:

        print("\nHunt Configuration:")
        print(f"Last position: {fish_at_pos}")

        for i, (_, text) in enumerate(menu_options, start=1):
            print(f"{i}: {text}")

        print("-1: Quit")

        selected = get_menu_choice(menu_options)

        match selected:
            case -1:
                shutdown()

            case FeebasHuntConfig.START:
                return False, 0

            case FeebasHuntConfig.CURRENT_POS:
                return False, fish_at_pos

            case FeebasHuntConfig.START_TO_POS:
                return True, fish_at_pos

            case FeebasHuntConfig.POS_TO_NEW:

                new_pos = get_new_position(
                    fish_at_pos,
                    tot_tiles
                )

                if new_pos is not None:
                    return True, new_pos

            case _:
                print("Invalid option.")


def get_menu_choice(valid_options: list) -> int:
    choice_map = {
        i: option
        for i, (option, _) in enumerate(valid_options, start=1)
    }

    while True:
        try:
            option = int(input("#: ").strip())
        except ValueError:
            print("Please enter a number.")
            continue

        # Shutdown
        if option == -1:
            return -1

        if option not in choice_map:
            print("Invalid option.")
            continue

        selected = choice_map[option]
        return selected


def get_new_position(start_pos: int, total_tiles: int) -> int | None:
    while True:
        try:
            option = int(
                input(
                    f"Pick a new start point "
                    f"({start_pos + 1}-{total_tiles - 1}) "
                    f"or -1 to cancel: "
                )
            )

            if option == -1:
                return None

            if start_pos < option < total_tiles:
                return option

            print("Position out of range.")

        except ValueError:
            print("Please enter a valid number.")


def shutdown():
    pause_main_state = PauseStateManager.get_instance()
    pause_main_event = threading.Event()

    shutdown_state = ShutdownStateManager.get_instance()
    shutdown_event = threading.Event()

    pause_main_event.set()
    shutdown_event.clear()

    pause_main_state.set_main_state(pause_main_event)
    shutdown_state.set_state(shutdown_event)

    print("Shutting down")
    raise SystemExit(0)


def feebas_hunt_configuration_menu(fish_at_pos, tot_tiles):
    """
    Function that formats menu options for Feebas fishing based on the current position.

    :param fish_at_pos: Current tile position
    :param tot_tiles: Total fish-able tiles in the pond
    :return: List of menu options
    """

    next_pos = fish_at_pos + 1
    last_pos = tot_tiles - 1
    full_span = f"{next_pos} - {last_pos}"
    destination = f"{full_span if not next_pos == last_pos else next_pos}"

    current_pos = f"Start fishing at tile {fish_at_pos}"
    start_to_tile_option = f"Go from 0 to fish at {fish_at_pos}"
    select_new_tile_option = f"Go from {fish_at_pos} to fish at <New_Pos>:({destination})"

    menu_options = [(FeebasHuntConfig.START, "Start fishing at tile 0")]

    if fish_at_pos > 0:
        menu_options.append((FeebasHuntConfig.CURRENT_POS, current_pos))

        menu_options.append((FeebasHuntConfig.START_TO_POS, start_to_tile_option))

    if fish_at_pos < tot_tiles - 1:
        menu_options.append((FeebasHuntConfig.POS_TO_NEW, select_new_tile_option))

    return menu_options
