import time
import keyboard
import pyautogui

from src.python_logic import controls, detection
from src.python_logic.states.GameView import GameViewStateManager
from src.python_logic.states.Window import WindowStateManager
from src.python_logic.states.Shutdown import ShutdownStateManager


def hatch_egg():
    w, h = WindowStateManager.get_instance().get_window_size()
    x = int(w * 1 / 8)
    y = int(h * 1 / 3)
    pixel = pyautogui.pixel(x, y)

    """
    True is UP
    False is DOWN
    """
    previous_direction = True
    keyboard.press('w')
    while True:
        if ShutdownStateManager.get_instance().check_shutdown_state():
            return

        # === Scout timer ===
        if True:
            start_time = time.time()
            duration = 0
            while duration < 1:
                if ShutdownStateManager.get_instance().check_shutdown_state():
                    return
                pixel = pyautogui.pixel(x, y)
                end_time = time.time()
                duration = end_time - start_time
        # =====================

        print("Where we at?")
        pyautogui.moveTo(x, y)
        if detection.dialog_is_open():  # Egg hatching
            keyboard.release('w')
            keyboard.release('s')
            print("Egg is hatching!")
            controls.a_button()
            time.sleep(2)
            controls.a_button()
            print("Breeder mode ending...")
            return

        elif not detection.has_background_changed(x, y, pixel):
            pixel = pyautogui.pixel(x, y)
            previous_direction = not previous_direction
            if previous_direction:  # Then, go down
                print("Going down")
                # previous_direction = False
                keyboard.release('w')
                keyboard.press('s')
            else:  # Then, go up
                print("Going up")
                #                 previous_direction = True
                keyboard.release('s')
                keyboard.press('w')


def is_two_pokemon_inserted():
    w, h = WindowStateManager.get_instance().get_window_size()
    pokemon_coord1 = (int(w * 0.6108374384236454), int(h * 0.7206840390879479))
    pokemon_coord2 = (int(w * 0.8171544479860909), int(h * 0.7320846905537459))

    colors = GameViewStateManager.get_instance().get_poketch_colors()

    print("Checking status...")
    if pyautogui.pixelMatchesColor(pokemon_coord1[0], pokemon_coord1[1], colors[1]):
        print("Both pokemon are missing!")
        return False

    if pyautogui.pixelMatchesColor(pokemon_coord2[0], pokemon_coord2[1], colors[1]):
        print("Second pokemon is missing!")
        return False
    return True


# In Solaceon town we bike up and down and while refreshing the Poketch to see when an egg has appeared
def get_egg():
    w, h = WindowStateManager.get_instance().get_window_size()
    x = w * 1 / 8
    y = h * 1 / 3
    pixel = pyautogui.pixel(x, y)

    """
    True is UP
    False is DOWN
    """
    previous_direction = True
    while True:
        if ShutdownStateManager.get_instance().check_shutdown_state():
            return

        # === Scout timer ===
        if True:
            start_time = time.time()
            duration = 0
            while duration < 2:
                if ShutdownStateManager.get_instance().check_shutdown_state():
                    return
                end_time = time.time()
                duration = end_time - start_time
        # =====================

        # Refresh Pokétch
        controls.click_coord(w * 3 / 4, h / 2)
        # if detection.dialog_is_open():

        if not detection.has_background_changed(x, y, pixel):
            pixel = pyautogui.pixel(x, y)
            previous_direction = not previous_direction
            if previous_direction:  # Then, go down
                keyboard.release('w')
                keyboard.press('s')
            else:  # Then, go up
                keyboard.release('s')
                keyboard.press('w')


# x, y = controls.run_btn_coords()
#
# while True:
#     if ShutdownStateManager.get_instance().check_shutdown_state():
#         return
#
#     time.sleep(0.1)
#     if pyautogui.pixelMatchesColor(x, y, (41, 148, 206)):  # Blue run button
#         controls.click_coord(x, y)
#         w, h = WindowStateManager.get_instance().get_window_size()
#         start_time = time.time()
#         duration = 0
#         # While no black screen detected
#         while not pyautogui.pixelMatchesColor(int(w / 4), int(h / 2), (0, 0, 0)) and not pyautogui.pixelMatchesColor(int(w - (w / 4)), int(h / 2), (0, 0, 0)):
#             end_time = time.time()
#             duration = end_time - start_time
#
#             if duration > 6:
#                 break
#         if duration > 6:
#             print("Error: Unable to escape for some reason...")
#             sys.exit(0)
#         else:
#             print("Encounter ended.")
#             time.sleep(1.2)
#             break


# def look_for_egg():
