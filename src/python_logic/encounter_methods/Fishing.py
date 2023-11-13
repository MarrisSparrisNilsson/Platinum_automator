import threading
import json
import os
import time

from src.python_logic import detection, controls
from src.python_logic.state.state_manager import ShutdownStateManager, PauseStateManager, HuntStateManager, DialogStateManager


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

    # Walk step i and turn towards i+1, then fish twice.
    # Array[0] is start point where you fish and then use surf.

    # Steps:
    # 1: Fish x2
    # 2: Take step, (Array[i])
    # 3: Turn towards next step if Array[i] != Array[i+1]

    # Map goes through every fishable water tile
    # Steps are determined by direction and edge that the path crosses.
    pause_main_event = threading.Event()
    pause_main_state = PauseStateManager.get_instance()

    DialogStateManager.get_instance().set_dialog_pixels()

    pause_main_event.clear()  # Set internal flag to false
    pause_main_state.set_main_state(pause_main_event)  # Pauses encounter detection

    # Get the script's directory
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # Construct the file path
    file_path = os.path.join(script_directory, "../../resources/feebas.json")
    # Open the file
    with (open(file_path, "r") as f):
        content = json.load(f)
        tiles = content["path"]

        turn_dir = ''
        # start_pos = len(tiles) - 1
        # start_pos = 50
        while True:
            try:
                time.sleep(1)
                controls.switch_tab()
                start_pos = int(input(f"Which tile do you wish to begin at? (0-{len(tiles) - 1}): "))
                if start_pos > len(tiles) or start_pos < 0:
                    raise ValueError
                controls.switch_tab()
                break
            except ValueError:
                print("Invalid input, try again.")

        controls.select_in_game_menu_action(3)  # Use repel

        walk_num = 1
        encounters = 2  # Number of desired encounters
        for step in range(len(tiles)):

            walk_dir = tiles[step]
            if step + 1 < len(tiles):
                turn_dir = tiles[step + 1]
                HuntStateManager.get_instance().set_facing_direction(walk_dir)

            if step >= start_pos:
                pause_main_event.set()  # Set internal flag to true
                pause_main_state.set_main_state(pause_main_event)  # Resumes encounter detection
                fishing(encounters)
                time.sleep(2)

            PauseStateManager.get_instance().check_pause_state("Fishing is paused▶️", "Fishing and walking now continues🎣🪝")
            if ShutdownStateManager.get_instance().check_shutdown_state():
                return

            if step == 0:
                controls.surf()
                time.sleep(2.5)
            else:
                print(f"\n{step}:")
                # Block walking at some locations where only turning is desired.
                if (not step == 3 and not step == 29 and not step == 93 and not step == 98 and
                        not step == 102 and not step == 103 and not step == 223 and
                        not step == 324 and not step == 456 and not step == 458 and
                        not step == 484 and not step == 522 and not step == 528):
                    print(f"Walk #{walk_num}: {walk_dir}")
                    print(f"Turn: {turn_dir}")
                    controls.move(walk_dir, 1)
                    walk_num += 1
                else:
                    print(f"Walk #{walk_num}: ")
                    print(f"Turn: {turn_dir}")
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
        print("Feebas hunt complete")
