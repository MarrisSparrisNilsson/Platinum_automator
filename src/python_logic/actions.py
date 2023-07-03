# import pyautogui
import threading
import time
import keyboard
import random
# import contextvars

import detection
from state_manager import ExitStateManager, PauseStateManager


# import controls


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
    while True:
        # while - begin
        # Press b
        # Look for:
        # if fish_on
        # -> spam press_a 2 or 3 times with 0.25 seconds between each and then wait for 5 seconds
        # -> Check if a shiny appeared with rate of 0.1 seconds
        #       -> quit()
        # -> else look for run button and then click
        # else no_fish
        # -> press_a
        # while - end

        return None


def soft_reset_hunt():
    return None


def regular_hunt(window, habitat):
    detection.encounter_detection(window.width, window.height, habitat, search_encounter_func=walk_random)


def watch_exit():
    shutdown_state = ExitStateManager.get_instance()
    shutdown_event = threading.Event()
    keyboard.wait("esc")
    # if keyboard.is_pressed("esc"):
    print("Escape was pressed!")
    shutdown_event.set()
    shutdown_state.set_state(shutdown_event)
    # shutdown_state.set_state(True)
    # return True


def walk_random():
    shutdown_event = ExitStateManager.get_instance().get_state()
    pause_event = PauseStateManager.get_instance().get_state()

    last_dir = 0
    # while not exit_state.get_state() and not pause_state.get_state():
    while True:

        with pause_event:
            pause_event.wait()

        with shutdown_event:
            if shutdown_event.is_set():
                break

        random_dir = random.randint(0, 3)
        if last_dir == random_dir:
            print(f"Duplicate:   ({random_dir})")
            random_dir -= 1
        last_dir = random_dir

        random_steps = random.randint(1, 4)
        move(direction_int=random_dir, steps=random_steps)
    keyboard.unhook_all()


def move(direction_int, steps=1):
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
    # return direction


def lets_try_spinning():
    print("Character is spinning")
    # move_dirs = ['a', 'w', 'd', 's']
    exit_state = PauseStateManager.get_instance()
    is_exiting = exit_state.get_state()

    while not is_exiting:

        for dirs in range(4):
            if is_exiting:
                print(f"Break was fired at i={dirs}")
                break

            move(direction_int=dirs, steps=2)
