import threading

import pyautogui
import pygetwindow

from src.core.App import app_context
from src.window.game_object_region_definitions import UI_ELEMENT_PIXELS


class GameContext:
    def __init__(self):
        self.start_pixel = (0, 0, 0)
        # Colors from top to bottom
        self.poketch_colors = [(57, 82, 49), (115, 181, 115), (82, 132, 82)]
        self.dialog_point1: tuple[int, int] = (0, 0)
        self.dialog_point2: tuple[int, int] = (0, 0)

        self.lock = threading.Lock()

    def set_dialog_pixels(self):
        with self.lock:
            normalized_dialog_1 = normalize_pixel_coords(*UI_ELEMENT_PIXELS["dialog_1"])
            normalized_dialog_2 = normalize_pixel_coords(*UI_ELEMENT_PIXELS["dialog_2"])

            start_p = pyautogui.pixel(normalized_dialog_2[0], normalized_dialog_2[1])
            self.start_pixel = start_p
            self.dialog_point1 = normalized_dialog_1
            self.dialog_point2 = normalized_dialog_2

    def get_dialog_pixels(self):
        with self.lock:
            return self.start_pixel, self.dialog_point1, self.dialog_point2

    def get_poketch_colors(self):
        with self.lock:
            return self.poketch_colors


game_context = GameContext()


# Get the pixels
def normalize_pixel_coords(x: int, y: int):
    """
    Normalizes the pixel coordinates based on the current window size and position.
    """
    window: pygetwindow.Win32Window = app_context.get_window()
    w, h = window.size
    x_offset, y_offset = window.topleft

    standard_width = 1940
    standard_height = 856
    static_height = 80
    window_x_border = 7
    # y_coord = int(((y + y_offset) / 856) * h)
    reference_game_height = standard_height - static_height
    current_game_height = h - static_height

    x_coord = int(((x + x_offset + window_x_border) / standard_width) * w)
    y_coord = int(((y + y_offset - static_height) / reference_game_height) * current_game_height) + static_height

    return x_coord, y_coord


def normalize_region(region: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    """
    Normalizes the region coordinates based on the current window size and position,
    then checks if the utility item is present in that region.
    """
    window: pygetwindow.Win32Window = app_context.get_window()

    w, h = window.size
    x_offset, y_offset = window.topleft

    left, top, width, height = region

    static_height = 80
    standard_width = 1940
    standard_height = 856
    window_x_border = 7

    reference_game_height = standard_height - static_height
    current_game_height = h - static_height

    region: tuple[int, int, int, int] = (
        int(x_offset + left + window_x_border),
        int(y_offset + static_height + ((top - static_height) / reference_game_height) * current_game_height),
        int((width / standard_width) * w),
        int((height / reference_game_height) * current_game_height),
    )

    return region
