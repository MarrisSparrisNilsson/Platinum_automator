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

    pause_main_event.clear()  # Set internal flag to false (Pause)
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
    time.sleep(0.2)  # Wait for pause_main_state print
    try:
        with (open(feebas_data_path, "r+") as f):
            data = json.load(f)

            found_date = data['found_date']
            # If Feebas has not been found today
            if not found_date == todays_date:
                was_found_today = False
                data['found_at'] = 0
                data['found_date'] = ""
                fish_at_pos = data['latest_tile']
                if not data['current_date'] == todays_date:
                    data['current_date'] = todays_date
                    data['latest_tile'] = 0
                    print("\nNew day has begun!"
                          "\nFarthest reached position has been set to 0")
                f.seek(0)
                json.dump(data, f, indent=2)
            else:
                was_found_today = True
                fish_at_pos = data['found_at']
                print(f"FEEBAS was last seen at step {fish_at_pos}❗")

            controls.switch_tab()
            walk_to_pos, new_fish_at_pos = hunt_configuration(fish_at_pos, len(tiles))
            controls.switch_tab()

            # in_game_menu_controls.execute_inGame_menu_action(InGameMenuSlots.BAG, UtilityItems.MAX_REPEL)  # Use repel
            # in_game_menu_controls.execute_inGame_menu_action(InGameMenuSlots.BAG, UtilityItems.GOOD_ROD)  # Register Good Rod

            # walk_num = 1
            encounters = 2  # Number of desired encounters
            # turn_dir = tiles[0 if fish_at_pos == 0 else fish_at_pos]
            # turn_dir = tiles[0 if fish_at_pos == 0 and not walk_to_pos and not tiles[fish_at_pos + 1] == tiles[fish_at_pos] else fish_at_pos]

            # fish_at_pos == 0 or walk_to_pos
            # edge_case = False
            # if fish_at_pos == 0 and not walk_to_pos:
            #     turn_dir = tiles[0]
            #     # fish_at_pos = 0
            # elif tiles[fish_at_pos] == tiles[fish_at_pos - 1] and not walk_to_pos:
            #     turn_dir = tiles[fish_at_pos + 2]
            #     edge_case = True
            #     # fish_at_pos = fish_at_pos + 2
            # else:
            #     turn_dir = tiles[fish_at_pos]
            # fish_at_pos = fish_at_pos + 1
            # walk_dir = ''
            go_to_new_start_pos = fish_at_pos < new_fish_at_pos
            start_pos = 0 if new_fish_at_pos == 0 or walk_to_pos and not go_to_new_start_pos else fish_at_pos
            init_turn_dir = tiles[start_pos]
            # init_turn_dir = tiles[start_pos + 1 if ((start_pos + 1) < len(tiles)) else start_pos]
            HuntStateManager.get_instance().set_facing_direction(init_turn_dir)  # Set initial facing direction
            # - 1 if new_pos else tile
            for tile in range(start_pos, len(tiles)):
                if not was_found_today:
                    data['latest_tile'] = tile
                f.seek(0)
                json.dump(data, f, indent=2)

                # if walk_to_pos else tile - 1
                separator = '\n'
                print("\r", end=f"Fishing at tile: {tile}{separator if not walk_to_pos else ''}")
                # print()
                # print("\nWalk dir:", walk_dir, "\nTurn dir:", turn_dir)

                # =================================================================
                '''
                NOTE 1: Start fishing if current position index is greater or equal to assigned position 
                             and therefore is NOT assigned to walk anywhere (walk_to_pos=False)                             
                NOTE 2: Skip fishing as long as current position is less than assigned start position
                '''
                # if (tile >= new_fish_at_pos and not walk_to_pos and not tile == 0) or (tile > new_fish_at_pos):
                # if new_tile >= new_fish_at_pos or not walk_to_pos:
                if tile >= new_fish_at_pos:
                    # When new_fish_at_pos is reached and is not start position
                    if tile == new_fish_at_pos:
                        walk_to_pos = False
                        print("\nFishing spot reached")
                        time.sleep(1)
                    # print()

                    # Continue static fishing when found_at location is reached
                    if was_found_today:
                        break

                    pause_main_event.set()  # Set internal flag to true
                    pause_main_state.set_main_state(pause_main_event)  # Resumes encounter detection
                    time.sleep(1)
                    fishing(encounters)
                    time.sleep(3)
                    PauseStateManager.get_instance().check_pause_state("Fishing is paused▶️", "Fishing and walking now continues🎣🪝")

                    # If Feebas was found
                    if HuntStateManager.get_instance().get_target_pokemon_found():
                        todays_date = file_manager.get_date("%Y-%m-%d")
                        was_found_today = True
                        break

                if ShutdownStateManager.get_instance().check_shutdown_state():
                    return

                # =================================================================

                if tile == 0:
                    # if not walk_to_pos:
                    #     pause_main_event.set()  # Set internal flag to true
                    #     pause_main_state.set_main_state(pause_main_event)  # Resumes encounter detection
                    #     fishing(encounters)
                    #     time.sleep(5)
                    #     PauseStateManager.get_instance().check_pause_state("Fishing is paused▶️", "Fishing and walking now continues🎣🪝")
                    #     if ShutdownStateManager.get_instance().check_shutdown_state():
                    #         return

                    # time.sleep(12)
                    controls.surf()
                    time.sleep(2.5)
                else:
                    # if new_fish_at_pos > 0:
                    #     walk_dir = tiles[tile + 1 if not edge_case else tile + 2]
                    #     turn_dir = tiles[tile + 2 if not edge_case else tile + 3]
                    # else:
                    # pos =
                    # walk_dir = tiles[tile + 1 if new_pos else tile]
                    # turn_dir = tiles[tile + 2 if (tile + 2) < len(tiles) and new_pos else tile + 1]
                    # turn_dir = tiles[new_tile]

                    # turn_dir = tiles[new_tile + 1]

                    # Block walking at some locations where only turning is desired.
                    walk_dir = tiles[tile]
                    turn_dir_count = tile + 1
                    turn_dir = tiles[turn_dir_count if turn_dir_count < len(tiles) and go_to_new_start_pos else tile]
                    # if tile == fish_at_pos:
                    if take_step(tile):
                        # walk_dir = tiles[tile + 1 if (tile + 1) < len(tiles) else tile]
                        # print(f"Walk #{walk_num}: {walk_dir}")
                        # print(f"Turn: {turn_dir}")

                        controls.move(walk_dir, 1)  # Step

                        # else:
                    # elif take_step(tile):
                    # walk_dir = tiles[tile]
                    # turn_dir = tiles[tile + 1 if (tile + 1) < len(tiles) and new_pos else tile]
                    # controls.move(walk_dir, 1)  # Step

                    # else:
                    #     walk_dir = tiles[tile]
                    #     turn_dir = tiles[tile + 1 if (tile + 1) < len(tiles) and new_pos else tile]
                    # walk_num += 1
                    # time.sleep(0.15)

                    # else:
                    # print(f"Walk #{walk_num}: ")
                    # print(f"Turn: {turn_dir}")
                    # if walk_num % 50 <= 10 and tile >= 100:
                    # time.sleep(0.15)

                    # If a new repel was activated, and we should not continue walking
                    if detection.check_repel_status():
                        if not walk_to_pos:
                            pause_main_event.set()  # Set internal flag to true
                            pause_main_state.set_main_state(pause_main_event)  # Resumes encounter detection

                    # Prevents double steps and overstepping
                    # print("\n", turn_dir, walk_dir, not turn_dir == walk_dir)
                    if not take_step(tile) or not turn_dir == walk_dir:
                        controls.move(turn_dir, 0)  # Turn
                        # init_turn_dir = None
                    # =================================================================

            if was_found_today:
                data['found_at'] = tile - 1
                # data['latest_tile'] = tile
                data['found_date'] = todays_date
            f.seek(0)
            json.dump(data, f, indent=2)

    # except KeyError:
    #     print("Something went wrong when accessing data from resource.")
    except json.decoder.JSONDecodeError:
        print("Something wrong with data file.")
        exit(-1)

    if was_found_today:
        pause_main_event.set()  # Set internal flag to true
        pause_main_state.set_main_state(pause_main_event)  # Resumes encounter detection
        # Feebas has been found (keep fishing)
        while True:
            if not todays_date == file_manager.get_date("%Y-%m-%d"):
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


def verify_feebas_file(full_file_path):
    default_data = {
        "found_at": 0,
        "latest_tile": 0,
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
    if (tile == 3 or tile == 29 or tile == 93 or
            tile == 98 or tile == 102 or tile == 222 or
            tile == 323 or tile == 455 or tile == 457 or
            tile == 483 or tile == 521 or tile == 527):
        return False
    else:
        return True


def hunt_configuration(fish_at_pos, tot_tiles):
    menu_options = hunt_configuration_menu(fish_at_pos, tot_tiles)

    while True:
        print("Hunt Configuration:")
        print(f"Last position: {fish_at_pos}")
        for i in range(len(menu_options)):
            print(f"{i + 1}. {menu_options[i]}")

        try:
            option = int(input("#: "))

            # Correct and clean up option-selection for some values of fish_at_pos
            if fish_at_pos == 0:
                if option == 2 or option == 3:
                    option = 4
                if option == 3:
                    option = 5
            elif fish_at_pos == 529:
                if option == 4:
                    option = 5

            match option:
                case 1:
                    walk_to_pos = False
                    fap = 0
                    return walk_to_pos, fap
                case 2:
                    walk_to_pos = False
                    fap = fish_at_pos
                    return walk_to_pos, fap
                case 3:
                    walk_to_pos = True
                    fap = fish_at_pos
                    return walk_to_pos, fap
                case 4:
                    walk_to_pos = True
                    while True:
                        try:
                            option = int(input(f"Pick a new start point to fish at ({fish_at_pos + 1}-{tot_tiles - 1}) or -1 to Exit: "))
                            if option < fish_at_pos or option > tot_tiles - 1:  # Out of bounds
                                raise ValueError
                            elif option == -1:
                                break
                            else:
                                fap = option
                                return walk_to_pos, fap
                        except ValueError:
                            print("Invalid input, try again.")
                case 5:
                    exit(1)
                case _:
                    print("Invalid input, try again.")
            print()
        except ValueError:
            print("Invalid input, try again.")
        except UnicodeDecodeError:
            exit(0)


def hunt_configuration_menu(fish_at_pos, tot_tiles):
    last_tile = f"Go from {fish_at_pos} to fish at <New_Pos>:({fish_at_pos + 1}-{tot_tiles - 1})"
    if fish_at_pos > 0:
        if fish_at_pos == 529:
            menu_options = [
                "Start fishing at tile 0",
                f"Start fishing at tile {fish_at_pos}",
                f"Go from 0 to fish at {fish_at_pos}",
                "Quit"
            ]
        else:
            menu_options = ["Start fishing at tile 0",
                            f"Start fishing at tile {fish_at_pos}",
                            f"Go from 0 to fish at {fish_at_pos}",
                            last_tile,
                            "Quit"]
    else:
        menu_options = [
            "Start fishing at tile 0",
            last_tile,
            "Quit"
        ]

    return menu_options
