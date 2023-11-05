import time
import keyboard
import random

from src.python_logic import detection


def walk_random(_):
    last_dir = 10  # Starts as a value with no direction representation

    while True:
        detection.check_pause_state("Walking is paused.", "Walking now continues:")

        if detection.check_shutdown_state():
            return

        random_dir = random.randint(0, 3)
        if last_dir == random_dir:
            print(f"Duplicate:   ({random_dir})")
            random_dir -= 1  # Prevents the same consecutive walking direction
        last_dir = random_dir

        random_steps = random.randint(1, 4)
        move(direction_int=random_dir, steps=random_steps)


def move(direction_int, steps=1):
    if detection.check_shutdown_state():
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
        time.sleep(0.1)
    # end = time.time()
    # print(f"Step active for: {end - start}s")


def lets_try_spinning(steps):
    print("Character is spinning")

    while True:
        for direction_int in range(4):
            detection.check_pause_state("Spinning is paused.", "Spinning now continues:")
            if detection.check_shutdown_state():
                return

            move(direction_int, steps)


def walk_straight_down(steps=1):
    start = time.time()
    keyboard.press('s')
    time.sleep(0.25 * steps)
    keyboard.release('s')
    end = time.time()
    print(end - start)
