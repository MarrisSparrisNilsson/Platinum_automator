import time
import keyboard
import random

from src.python_logic import controls
from src.python_logic.states.Shutdown import ShutdownStateManager
from src.python_logic.states.Pause import PauseStateManager


def walk_random(_):
    last_dir = 10  # Starts as a value with no direction representation

    while True:
        PauseStateManager.get_instance().check_pause_state("Walking is paused.", "Walking now continues:")

        if ShutdownStateManager.get_instance().check_shutdown_state():
            return

        random_dir = random.randint(0, 3)
        if last_dir == random_dir:
            print(f"Duplicate:   ({random_dir})")
            random_dir -= 1  # Prevents the same consecutive walking direction
        last_dir = random_dir

        random_steps = random.randint(1, 4)
        controls.move(direction=random_dir, steps=random_steps)


def lets_try_spinning(steps):
    print("Character is spinning")

    while True:
        for direction_int in range(4):
            PauseStateManager.get_instance().check_pause_state("Spinning is paused.", "Spinning now continues:")
            if ShutdownStateManager.get_instance().check_shutdown_state():
                return

            controls.move(direction_int, steps)


def walk_straight_down(steps=1):
    start = time.time()
    keyboard.press('s')
    time.sleep(0.25 * steps)
    keyboard.release('s')
    end = time.time()
    print(end - start)
