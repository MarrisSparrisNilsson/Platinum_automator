import threading
import time
import keyboard
import random

import detection
from state_manager import ShutdownStateManager, PauseStateManager
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
    detection.encounter_detection(search_encounter_func=fishing)


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

        controls.use_selected_item()
        detection.find_exclamation_mark()


def soft_reset_hunt():
    return None


def regular_hunt():
    detection.encounter_detection(search_encounter_func=walk_random)


def watch_exit():
    shutdown_state = ShutdownStateManager.get_instance()
    shutdown_event = threading.Event()
    keyboard.wait("esc")
    print("\nEscape was pressed!🚨")
    shutdown_event.clear()  # Reset the internal flag to false (Shutting down)
    shutdown_state.set_state(shutdown_event)  # Updating state


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
