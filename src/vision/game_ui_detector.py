import time

import pyautogui

from src.automation import controls, in_game_menu_controls
from src.core.App import app_context
from src.core.enums import InGameMenuSlots, UtilityItems
from src.core.Game import game_context
from src.states.Pause import PauseStateManager


# Get the pixels
def get_pixel_coords(x_float, y_float):
    window_width, window_height = app_context.window_size
    x_coord = int(window_width * x_float)
    y_coord = int(window_height * y_float)

    return x_coord, y_coord


def check_repel_status():
    # time.sleep(0.2)
    if dialog_is_open():
        pause_encounter_pause_event = PauseStateManager.get_instance().get_encounter_pause_state()

        # Pause if not already paused
        if pause_encounter_pause_event.is_set():
            pause_encounter_pause_event.clear()  # Pauses encounter detection
        for i in range(3):
            time.sleep(0.1)
            controls.a_button()
        time.sleep(0.1)
        in_game_menu_controls.execute_inGame_menu_action(InGameMenuSlots.BAG, [UtilityItems.MAX_REPEL])
        return True
    return False


def dialog_is_open():
    start_p, dialog_p1, dialog_p2 = game_context.get_dialog_pixels()
    if pyautogui.pixelMatchesColor(dialog_p1[0], dialog_p1[1], (255, 255, 255)) and not pyautogui.pixelMatchesColor(
        dialog_p2[0], dialog_p2[1], start_p
    ):
        return True
    else:
        return False


def has_background_changed(x, y, pixel):
    pyautogui.moveTo(x, y)
    if not pyautogui.pixelMatchesColor(x, y, pixel):
        #  print(f"P: {pyautogui.pixel(x, y)}, {pixel}")
        pyautogui.moveTo(x, y)
        return True
    else:
        return False
