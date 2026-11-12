import time

import pyautogui

from src.core.Game import normalize_pixel_coords, normalize_region
from src.definitions import SRC_DIR
from src.states.Shutdown import ShutdownStateManager
from src.utils.helpers import is_target_string_found
from src.vision.game_ui_detector import has_background_changed
from src.window.game_object_region_definitions import UI_ELEMENT_PIXELS, UI_ELEMENTS


def was_target_pokemon_found(pokemon_name: str):
    pokemon_name_img_path = SRC_DIR / "assets/images/local/pokemon_name.png"

    region = normalize_region(region=UI_ELEMENTS["pokemon_name"])
    pyautogui.screenshot(str(pokemon_name_img_path), region)

    # # If 50% of the words that are in order match, we assume we found the target Pokémon
    return is_target_string_found(
        pokemon_name,
        pokemon_name_img_path,
        0.5,
    )


def find_sparkles():
    # LOOK FOR SHINY SPARKLES AT THESE POINTS
    coords = [
        normalize_pixel_coords(*UI_ELEMENT_PIXELS["sparkle_1"]),
        normalize_pixel_coords(*UI_ELEMENT_PIXELS["sparkle_2"]),
        normalize_pixel_coords(*UI_ELEMENT_PIXELS["sparkle_3"]),
        normalize_pixel_coords(*UI_ELEMENT_PIXELS["sparkle_4"]),
        normalize_pixel_coords(*UI_ELEMENT_PIXELS["sparkle_5"]),
    ]

    # time.sleep(1)  # Seconds until Pokémon stands still

    # DEFAULT PIXELS
    shiny_p = [
        pyautogui.pixel(*coords[0]),
        pyautogui.pixel(*coords[1]),
        pyautogui.pixel(*coords[2]),
        pyautogui.pixel(*coords[3]),
        pyautogui.pixel(*coords[4]),
    ]

    duration = 0
    print("\nSearching for sparkles...🔎")
    start_time = time.time()
    while duration < 2.2:  # Sparkles duration
        if ShutdownStateManager.get_instance().is_shutting_down():
            return

        for i in range(len(shiny_p)):
            x, y = coords[i]
            pyautogui.moveTo(x, y)
            if has_background_changed(x, y, shiny_p[i]):
                return True

        end_time = time.time()
        duration = end_time - start_time
        # print(duration)

    print("No shiny this time...☹️\n")
    return False
