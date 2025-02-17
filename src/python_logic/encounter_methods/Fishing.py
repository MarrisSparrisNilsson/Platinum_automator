import threading
import json
import os
import time

from src.python_logic import detection, controls, file_manager, in_game_menu_controls
from src.python_logic.states.GameView import GameViewStateManager
from src.python_logic.states.Shutdown import ShutdownStateManager
from src.python_logic.states.Pause import PauseStateManager
from src.python_logic.states.Hunt import HuntStateManager
from src.python_logic.Enums import InGameMenuSlots, UtilityItems


def fishing(args):
    cast = [0]
    encounters = [0]
    while args is True or encounters[0] < args:  # args is bool or int

        PauseStateManager.get_instance().check_pause_state("Fishing is paused▶️", "Fishing now continues🎣🪝")

        if ShutdownStateManager.get_instance().check_shutdown_state():
            return

        if detection.use_selected_item():
            detection.find_exclamation_mark(cast, encounters)
        else:
            shutdown_state = ShutdownStateManager.get_instance()
            shutdown_event = threading.Event()
            print("Incorrect fishing spot!❌")
            shutdown_event.clear()  # Reset the internal flag to false (Shutting down)
            shutdown_state.set_state(shutdown_event)  # Updating state


def feebas_fishing(_):
    """
    Walk "i" steps and turn towards i+1, then fish twice.
    Array[0] is start point where you fish and then use surf.

    Steps:
    1: Fish x2
    2: Take step, (Array[i])
    3: Turn towards next step if Array[i] != Array[i+1]
    """

    # Map goes through every fishable water tile
    # Steps are determined by direction and edge of a tile that the path crosses.
    pause_main_event = threading.Event()
    pause_main_state = PauseStateManager.get_instance()

    GameViewStateManager.get_instance().set_dialog_pixels()

    pause_main_event.clear()  # Set internal flag to false
    pause_main_state.set_main_state(pause_main_event)  # Pauses encounter detection

    # Get the script's directory
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # Construct the file path
    feebas_resource_path = os.path.abspath(os.path.join(script_directory, "..", "..", "resources/feebas.json"))
    feebas_data_path = os.path.abspath(os.path.join(script_directory, "..", "..", "data/feebas.json"))
    # print(feebas_data_path)
    # print(feebas_resource_path)

    todays_date = file_manager.get_date("%Y-%m-%d")
    tiles = read_tiles(feebas_resource_path)
    verify_feebas_file(feebas_data_path)
    # TODO: Fix buggy resource file handling...
    try:
        with (open(feebas_data_path, "r+") as f):
            data = json.load(f)

            found_date = data['found_date']
            was_found_today = True
            # found_at = 0
            # If Feebas has not been found today
            if not found_date == todays_date:
                was_found_today = False
                data['found_at'] = 0
                data['found_date'] = ""
                fish_at_pos = data['latest_step']
                if not data['current_date'] == todays_date:
                    data['current_date'] = todays_date
                    data['latest_step'] = 0
                    print("\nTime is past midnight🌙"
                          "\nFarthest reached position has been set to 0")
                f.seek(0)
                json.dump(data, f, indent=2)
            else:
                fish_at_pos = data['found_at']
                print(f"FEEBAS was last seen at step {fish_at_pos}❗")

            controls.switch_tab()
            walk_to_pos, fish_at_pos = hunt_configuration(was_found_today, fish_at_pos, tiles)
            controls.switch_tab()

            # in_game_menu_controls.execute_inGame_menu_action(InGameMenuSlots.BAG, UtilityItems.MAX_REPEL)  # Use repel
            # in_game_menu_controls.execute_inGame_menu_action(InGameMenuSlots.BAG, UtilityItems.GOOD_ROD)  # Register Good Rod

            walk_num = 1
            encounters = 2  # Number of desired encounters
            walk_dir = tiles[0 if not walk_to_pos else fish_at_pos]
            HuntStateManager.get_instance().set_facing_direction(walk_dir)  # Set initial facing direction

            for tile in range(0 if fish_at_pos == 0 or walk_to_pos else fish_at_pos, len(tiles)):

                # if walk_to_pos else tile - 1
                print("\r", end=f"At tile: {tile}")
                walk_dir = tiles[tile]
                turn_dir = tiles[tile + 1 if ((tile + 1) < len(tiles)) else tile]
                print("\nWalk dir:", walk_dir, "\nTurn dir:", turn_dir)
                if tile == 0:
                    if not walk_to_pos:
                        pause_main_event.set()  # Set internal flag to true
                        pause_main_state.set_main_state(pause_main_event)  # Resumes encounter detection
                        fishing(encounters)
                        PauseStateManager.get_instance().check_pause_state("Fishing is paused▶️", "Fishing and walking now continues🎣🪝")
                        if ShutdownStateManager.get_instance().check_shutdown_state():
                            return

                    time.sleep(7)
                    controls.surf()
                    time.sleep(2.5)
                else:

                    '''
                    condition 1: Start fishing if current position index is grater or equal to assigned position 
                                 and NOT assigned to walk anywhere (walk_to_pos=False)                             
                    condition 2: Skip fishing as long as current position is less than assigned start position
                    '''
                    if (tile >= fish_at_pos and not walk_to_pos and not tile == 0) or (tile > fish_at_pos):
                        # When fish_at_pos is reached and is not start position
                        if tile == fish_at_pos and not fish_at_pos == 0:
                            walk_to_pos = False
                            print("\nFishing spot reached")
                        # Continue static fishing when found_at location is reached
                        if was_found_today:
                            break
                        # print()

                        pause_main_event.set()  # Set internal flag to true
                        pause_main_state.set_main_state(pause_main_event)  # Resumes encounter detection
                        fishing(encounters)
                        time.sleep(7)

                    # =================================================================

                    if not was_found_today and tile > data['latest_step']:
                        data['latest_step'] = tile
                    f.seek(0)
                    json.dump(data, f, indent=2)

                    # Block walking at some locations where only turning is desired.
                    if take_step(tile):
                        print(f"Walk #{walk_num}: {walk_dir}")
                        print(f"Turn: {turn_dir}")
                        controls.move(walk_dir, 1)  # Step
                        walk_num += 1
                        time.sleep(0.15)

                    # else:
                    # print(f"Walk #{walk_num}: ")
                    # print(f"Turn: {turn_dir}")
                    # if walk_num % 50 <= 10 and tile >= 100:
                    if detection.dialog_is_open():
                        pause_main_event.clear()  # Set internal flag to false
                        pause_main_state.set_main_state(pause_main_event)  # Pauses encounter detection
                        time.sleep(0.1)
                        controls.a_button()
                        in_game_menu_controls.execute_inGame_menu_action(InGameMenuSlots.BAG, UtilityItems.MAX_REPEL)
                        pause_main_event.set()  # Set internal flag to true
                        pause_main_state.set_main_state(pause_main_event)  # Resumes encounter detection

                    # Prevents double steps and overstepping
                    print("\n", turn_dir, walk_dir, not turn_dir == walk_dir)
                    if not turn_dir == walk_dir:
                        controls.move(turn_dir, 0)  # Turn
                    # =================================================================

                PauseStateManager.get_instance().check_pause_state("Fishing is paused▶️", "Fishing and walking now continues🎣🪝")
                if ShutdownStateManager.get_instance().check_shutdown_state():
                    return

                # If Feebas was found
                if HuntStateManager.get_instance().get_target_pokemon_found():
                    todays_date = file_manager.get_date("%Y-%m-%d")
                    was_found_today = True
                    break

            if was_found_today:
                data['found_at'] = tile - 1
                data['found_date'] = todays_date
            f.seek(0)
            json.dump(data, f, indent=2)

    # except KeyError:
    #     print("Something went wrong when accessing data from resource.")
    except json.decoder.JSONDecodeError:
        print("Something wrong with data file.")
        exit(-1)

    pause_main_event.set()  # Set internal flag to true
    pause_main_state.set_main_state(pause_main_event)  # Resumes encounter detection
    # Feebas has been found
    while True:
        if not todays_date == file_manager.get_date("%Y-%m-%d"):
            shutdown_state = ShutdownStateManager.get_instance()
            shutdown_event = threading.Event()
            print("\nTime is past midnight🌙"
                  "\nGo back to start position and try again.")
            shutdown_event.clear()  # Reset the internal flag to false (Shutting down)
            shutdown_state.set_state(shutdown_event)  # Updating state
            break
        else:
            fishing(1)


def verify_feebas_file(full_file_path):
    default_data = {
        "found_at": 0,
        "latest_step": 0,
        "found_date": "",
        "current_date": ""
    }
    # Ensure the file exists before checking its content
    if not os.path.exists(full_file_path) or os.stat(full_file_path).st_size == 0:
        with open(full_file_path, "w") as file:
            file.seek(0)
            json.dump(default_data, file, indent=2)
            print("File initialized with default structure.")
    else:
        with open(full_file_path, "r+") as file:
            try:
                data = json.load(file)
                missing = False
                for key in default_data.keys():
                    if key not in data:
                        missing = True
                        break

                if missing:
                    file.seek(0)
                    json.dump(default_data, file, indent=2)
                    print("File initialized with default structure.")
                else:
                    print("File contents OK")
            except json.decoder.JSONDecodeError:
                file.seek(0)
                json.dump(default_data, file, indent=2)
                print("File initialized with default structure.")


def read_tiles(feebas_resource_path):
    try:
        # Open the file
        with (open(feebas_resource_path, "r") as f):
            file = json.load(f)
            tiles = file["path"]
            return tiles
    except json.decoder.JSONDecodeError:
        print("Something wrong with resource file.")
        exit(-1)


def take_step(tile):
    if (tile == 3 or tile == 29 or tile == 93 or tile == 98 or
            tile == 102 or tile == 103 or tile == 223 or
            tile == 324 or tile == 456 or tile == 458 or
            tile == 484 or tile == 522 or tile == 528):
        return False
    else:
        return True


def hunt_configuration(was_found_today, fish_at_pos, tiles):
    walk_to_pos = False
    fap = fish_at_pos
    if not fap == 0:
        while True:
            try:
                time.sleep(0.5)

                ans = input(f"Are you at tile {fap} and wish to continue from there? (y/n): ")
                if ans == 'y':
                    walk_to_pos = False
                    break
                elif ans == 'n':
                    if was_found_today:
                        ans = input(f"Go from start position (0) to tile {fap} and continue from there? (y/n): ")
                        if ans == 'y':
                            walk_to_pos = True
                            break
                        elif not ans == 'n':
                            raise ValueError
                    fap = 0
                    print("(Assuming you are at tile 0)")
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Invalid input, try again.")

    if not was_found_today and fap == 0:
        while True:
            try:
                time.sleep(0.5)
                fap = int(input(f"Which tile do you wish to begin at? (0-{len(tiles) - 1}): "))
                if fap < 0 or len(tiles) < fap:
                    raise ValueError
                if fap > 0:
                    walk_to_pos = True
                break
            except ValueError:
                print("Invalid input, try again.")

    return walk_to_pos, fap
