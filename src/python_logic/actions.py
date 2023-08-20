import threading
import time
import keyboard
import random
import pyautogui

import detection
from state_manager import ShutdownStateManager, PauseStateManager, WindowStateManager
import controls


def pokeradar_hunt():
    # while not keyboard.is_pressed("q"):
    while True:
        # while - begin
        # Press b

        # --- Locate 1st grass patch to follow ---
        # Out of the maximum 4 patches that can spawn,
        # locate the furthest away grass patch of the same type (4 tiles away)
        # if it is an edge grass -> continue
        # elseif no grass patch of the same type was spotted 4 tiles away ->
        # - Find_safe_zone()
        # - Recharge_radar() (Run back and forth x steps in a safe direction and length until it's recharged.)
        # else -> break (Valid grass patch was located)

        # while - end

        # Walk into that grass patch

        # Faint pokemon

        return None


def fishing_hunt():
    detection.encounter_detection(search_encounter_func=fishing, end_encounter_func=flee_encounter)


def fishing():
    while True:
        pause_event = PauseStateManager.get_instance().get_state()

        if pause_event is not None:
            if not pause_event.is_set():
                print("Fishing is paused▶️")
                pause_event.wait()
                print("Fishing now continues🎣🪝")

        shutdown_event = ShutdownStateManager.get_instance().get_state()
        if shutdown_event is not None:
            break

        if controls.use_selected_item():
            detection.find_exclamation_mark()
        else:
            shutdown_state = ShutdownStateManager.get_instance()
            shutdown_event = threading.Event()
            print("Incorrect fishing spot!❌")
            shutdown_event.clear()  # Reset the internal flag to false (Shutting down)
            shutdown_state.set_state(shutdown_event)  # Updating state


def save_game():
    window_width, window_height = WindowStateManager.get_instance().get_window_size()
    save_p = (int(window_width * 0.3077319587628866), int(window_height * 0.6285046728971962))
    save_box_p = (int(window_width * 0.12061855670103093), int(window_height * 0.32710280373831774))
    start_save_box = pyautogui.pixel(save_box_p[0], save_box_p[1])

    controls.open_bag()

    while True:
        time.sleep(0.1)
        shutdown_event = ShutdownStateManager.get_instance().get_state()
        if shutdown_event is not None:
            return

        if pyautogui.pixelMatchesColor(save_p[0], save_p[1], (255, 107, 16)):
            while True:
                shutdown_event = ShutdownStateManager.get_instance().get_state()
                if shutdown_event is not None:
                    return

                controls.a_key()
                time.sleep(0.5)

                if pyautogui.pixelMatchesColor(save_box_p[0], save_box_p[1], start_save_box):
                    print("Game is saved!")
                    return
        else:
            controls.up()


def soft_reset_hunt():
    save_game()
    shutdown_event = ShutdownStateManager.get_instance().get_state()
    if shutdown_event is not None:
        return
    detection.encounter_detection(search_encounter_func=static_encounter, end_encounter_func=soft_reset)


def regular_hunt():
    detection.encounter_detection(search_encounter_func=walk_random, end_encounter_func=flee_encounter)


def watch_exit():
    shutdown_state = ShutdownStateManager.get_instance()
    shutdown_event = threading.Event()
    keyboard.wait("esc")
    print("\nEscape was pressed!🚨")
    shutdown_event.clear()  # Reset the internal flag to false (Shutting down)
    shutdown_state.set_state(shutdown_event)  # Updating state

    pause_main_event = PauseStateManager.get_instance().get_main_state()
    if pause_main_event is not None:
        pause_main_event.set()  # Signal main pause event to get out of wait state


def static_encounter():
    pause_main_state = PauseStateManager.get_instance()
    pause_main_event = threading.Event()
    while True:
        pause_main_event.clear()  # Pauses encounter detection
        pause_main_state.set_main_state(pause_main_event)

        soft_reset()

        start_time = time.time()
        duration = 0

        # Press "a" during startup
        while duration < 15:  # Time until encounter detection starts
            shutdown_event = ShutdownStateManager.get_instance().get_state()
            if shutdown_event is not None:
                return

            time.sleep(0.3)
            controls.a_key()
            end_time = time.time()
            duration = end_time - start_time

        pause_main_event.set()  # Resumes encounter detection
        pause_main_state.set_main_state(pause_main_event)

        # Press "a" until encounter starts
        while True:
            pause_event = PauseStateManager.get_instance().get_state()
            # If encounter is active
            if pause_event is not None:
                if not pause_event.is_set():
                    print("Button presses is paused.")
                    pause_event.wait()  # Wait for encounter to finish
                    print("\nButton presses now continues.")
                    break

            shutdown_event = ShutdownStateManager.get_instance().get_state()
            if shutdown_event is not None:
                return

            time.sleep(0.5)
            controls.a_key()


def soft_reset():
    # pyautogui.hotkey("ctrl", "r")
    keyboard.press("ctrl+r")
    time.sleep(0.1)
    keyboard.release("ctrl+r")


def flee_encounter():
    x, y = controls.run_btn_coords()

    while True:
        shutdown_event = ShutdownStateManager.get_instance().get_state()
        if shutdown_event is not None:
            break

        time.sleep(0.1)
        if pyautogui.pixelMatchesColor(x, y, (41, 148, 206)):  # Blue run button
            controls.click_coord(x, y)
            w, h = WindowStateManager.get_instance().get_window_size()
            time.sleep(3.5)
            if pyautogui.pixelMatchesColor(int(w / 4), int(h / 2), (0, 0, 0)):  # Black screen
                print("Encounter ended. Search continues...\n")
                time.sleep(1.2)
                break
            else:
                print("Error: Unable to escape for some reason...")
                exit()


def walk_random():
    last_dir = 10  # Starts as a value with no direction representation

    while True:
        shutdown_event = ShutdownStateManager.get_instance().get_state()
        pause_event = PauseStateManager.get_instance().get_state()

        if pause_event is not None:
            if not pause_event.is_set():
                print("Walking is paused.")
                pause_event.wait()
                print("Walking now continues:")

        if shutdown_event is not None:
            return

        random_dir = random.randint(0, 3)
        if last_dir == random_dir:
            print(f"Duplicate:   ({random_dir})")
            random_dir -= 1  # Prevents the same consecutive walking direction
        last_dir = random_dir

        random_steps = random.randint(1, 4)
        move(direction_int=random_dir, steps=random_steps)


def move(direction_int, steps=1):
    shutdown_event = ShutdownStateManager.get_instance().get_state()
    if shutdown_event is not None:
        return

    move_dirs = ['a', 'w', 'd', 's']
    print(f"{steps} step(s): {move_dirs[direction_int]} ({direction_int})")
    keyboard.press(move_dirs[direction_int])
    # start = time.time()
    if steps == 0:
        time.sleep(0.05)
    else:
        time.sleep(0.27 * steps)

    keyboard.release(move_dirs[direction_int])

    if steps == 0:
        time.sleep(0.5)
    else:
        time.sleep(0.2)
    # end = time.time()
    # print(f"Step active for: {end - start}s")


def lets_try_spinning():
    print("Character is spinning")

    while True:
        pause_event = PauseStateManager.get_instance().get_state()
        if pause_event is not None:
            if not pause_event.is_set():
                print("Spinning is paused.")
                pause_event.wait()
                print("Spinning now continues:")

        shutdown_event = ShutdownStateManager.get_instance().get_state()
        if shutdown_event is not None:
            break

        for dirs in range(4):
            shutdown_event = ShutdownStateManager.get_instance().get_state()
            if shutdown_event is not None:
                print(f"Break was fired at i={dirs}")
                break

            move(direction_int=dirs, steps=2)


def walk_straight_down(steps=1):
    start = time.time()
    keyboard.press('s')
    time.sleep(0.25 * steps)
    keyboard.release('s')
    end = time.time()
    print(end - start)
