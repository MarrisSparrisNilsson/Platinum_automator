# import pyautogui
import time
import keyboard


# import controls


def start_pokeradar_hunt():
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


def start_fishing_hunt():
    while True:
        # keyboard._listener()
        # while - begin
        # Press b
        # Look for:
        # if fish_on
        # -> spam press_a 3 times with 0.25 seconds between each and then wait for 10 seconds
        # -> Check if a shiny appeared
        #       -> quit()
        # -> else look for run button and then click
        # else no_fish
        # -> press_a
        # while - end

        return None


def start_soft_reset_hunt():
    return None


def watch_quit():
    keyboard.wait("esc")
    # if keyboard.is_pressed("esc"):
    print("Escape was pressed!")
    return True


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
    return direction


def lets_try_spinning(done):
    print("Character is spinning XO")
    move_dirs = ['a', 'w', 'd', 's']

    while not done[0]:

        for i in range(4):
            if done[0]:
                print(f"Break was fired at i={i}")
                break

            move(move_dirs[i], steps=2)
