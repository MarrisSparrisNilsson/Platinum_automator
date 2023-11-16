import threading
import json
import os
import time

from src.python_logic import detection, controls, file_manager
from src.python_logic.states.GameView import GameViewStateManager
from src.python_logic.states.Shutdown import ShutdownStateManager
from src.python_logic.states.Pause import PauseStateManager
from src.python_logic.states.Hunt import HuntStateManager


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
    # TODO: Detect Feebas and mark spot.

    # Walk i steps and turn towards i+1, then fish twice.
    # Array[0] is start point where you fish and then use surf.

    # Steps:
    # 1: Fish x2
    # 2: Take step, (Array[i])
    # 3: Turn towards next step if Array[i] != Array[i+1]

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
    file_path = os.path.join(script_directory, "../../resources/feebas.json")
    try:
        # Open the file
        with (open(file_path, "r+") as f):
            data = json.load(f)

            tiles = data["path"]
            found_date = data['found_date']
            latest_step = data['latest_step']
            todays_date = file_manager.get_date("%Y-%m-%d")
            if not found_date == todays_date:
                found_date = ""
                data['location'] = 0
                data['found_date'] = ""
                f.seek(0)
                json.dump(data, f, indent=2)

            turn_dir = ''

            start_pos = 0
            controls.switch_tab()
            if not latest_step == 0:
                while True:
                    try:
                        time.sleep(0.5)
                        ans = input(f"Are you at step {latest_step} and wish to continue from there? (y/n): ")
                        if ans == 'y':
                            start_pos = latest_step
                            break
                        elif ans == 'n':
                            latest_step = 0
                            break
                        else:
                            raise ValueError
                    except ValueError:
                        print("Invalid input, try again.")

            if found_date == "" and latest_step == 0:
                while True:
                    try:
                        time.sleep(0.5)
                        start_pos = int(input(f"Which tile do you wish to begin at? (0-{len(tiles) - 1}): "))
                        if start_pos > len(tiles) or start_pos < 0:
                            raise ValueError
                        break
                    except ValueError:
                        print("Invalid input, try again.")

            controls.switch_tab()
            controls.select_in_game_menu_action(3)  # Use repel

            walk_num = 1
            encounters = 2  # Number of desired encounters
            for step in range(latest_step + 1, len(tiles)):

                walk_dir = tiles[step]
                if step + 1 < len(tiles):
                    turn_dir = tiles[step + 1]
                    HuntStateManager.get_instance().set_facing_direction(walk_dir)

                if step >= start_pos:
                    print()
                    pause_main_event.set()  # Set internal flag to true
                    pause_main_state.set_main_state(pause_main_event)  # Resumes encounter detection
                    fishing(encounters)
                    time.sleep(2)

                PauseStateManager.get_instance().check_pause_state("Fishing is paused▶️", "Fishing and walking now continues🎣🪝")
                if ShutdownStateManager.get_instance().check_shutdown_state():
                    return

                # If Feebas was found
                if HuntStateManager.get_instance().get_target_pokemon_found():
                    break

                if step == 0:
                    controls.surf()
                    time.sleep(2.5)
                else:
                    print("\r", end=f"Step: {step}")
                    data['latest_step'] = step
                    f.seek(0)
                    json.dump(data, f, indent=2)
                    # Block walking at some locations where only turning is desired.
                    if take_step(step):
                        # print(f"Walk #{walk_num}: {walk_dir}")
                        # print(f"Turn: {turn_dir}")
                        controls.move(walk_dir, 1)
                        walk_num += 1
                    # else:
                    # print(f"Walk #{walk_num}: ")
                    # print(f"Turn: {turn_dir}")
                    if walk_num % 50 <= 10 and step >= 100:
                        time.sleep(0.15)
                        if detection.dialog_is_open():
                            pause_main_event.clear()  # Set internal flag to false
                            pause_main_state.set_main_state(pause_main_event)  # Pauses encounter detection
                            time.sleep(0.1)
                            controls.a_key()
                            controls.select_in_game_menu_action(3)
                            pause_main_event.set()  # Set internal flag to true
                            pause_main_state.set_main_state(pause_main_event)  # Resumes encounter detection

                if not turn_dir == walk_dir:
                    controls.move(turn_dir, 0)

            data['location'] = step
            data['found_date'] = todays_date
            f.seek(0)
            json.dump(data, f, indent=2)

    except KeyError:
        print("Something went wrong when accessing data from resource.")
    except json.decoder.JSONDecodeError:
        print("Something wrong with resource file.")

    # Feebas has been found
    fishing(True)


def take_step(step):
    if (step == 3 or step == 29 or step == 93 or step == 98 or
            step == 102 or step == 103 or step == 223 or
            step == 324 or step == 456 or step == 458 or
            step == 484 or step == 522 or step == 528):
        return False
    else:
        return True
