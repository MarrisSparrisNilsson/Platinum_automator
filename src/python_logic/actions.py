# import pyautogui
import time
import keyboard
import random
# import contextvars

import detection


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


def regular_hunt(window, habitat, done):
    detection.encounter_detection(window.width, window.height, habitat, walk_random, done)
    return None


def watch_quit():
    keyboard.wait("esc")
    # if keyboard.is_pressed("esc"):
    print("Escape was pressed!")
    return True


def walk_random(done):
    move_dirs = ['a', 'w', 'd', 's']
    while not done[0]:
        random_dir = random.randint(0, 4)
        random_steps = random.randint(1, 4)
        move(move_dirs[random_dir], random_steps)


def move(direction, steps=1):
    keyboard.press(direction)
    # start = time.time()
    if steps == 0:
        time.sleep(0.05)
    else:
        time.sleep(0.27 * steps)
    keyboard.release(direction)

    if steps == 0:
        time.sleep(0.5)
    else:
        time.sleep(0.2)
    # end = time.time()
    # print(f"Step active for: {end - start}s")
    # return direction


def lets_try_spinning(done):
    print("Character is spinning")
    move_dirs = ['a', 'w', 'd', 's']

    while not done[0]:

        for i in range(4):
            if done[0]:
                print(f"Break was fired at i={i}")
                break

            move(move_dirs[i], steps=2)
