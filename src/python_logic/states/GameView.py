import threading
import pyautogui

from src.python_logic.states.Window import WindowStateManager


# Get the pixels
def get_pixel_coords(x_float, y_float):
    window_width, window_height = WindowStateManager.get_instance().get_window_size()
    x_coord = int(window_width * x_float)
    y_coord = int(window_height * y_float)

    return x_coord, y_coord


class GameViewStateManager:
    _instance = None
    _start_pixel = (0, 0, 0)
    # Top to bottom
    _poketch_colors = [(57, 82, 49), (115, 181, 115), (82, 132, 82)]
    _dialog_point1: (int, int) = (0, 0)
    _dialog_point2: (int, int) = (0, 0)
    _lock = threading.Lock()

    @staticmethod
    def get_instance():
        if GameViewStateManager._instance is None:
            with GameViewStateManager._lock:
                if GameViewStateManager._instance is None:
                    GameViewStateManager._instance = GameViewStateManager()
        return GameViewStateManager._instance

    def set_dialog_pixels(self):
        with GameViewStateManager._lock:
            window_width, window_height = WindowStateManager.get_instance().get_window_size()
            dialog_p1 = (int(window_width * 0.032474226804123714), int(window_height * 0.802570093457944))
            dialog_p2 = (int(window_width * 0.4747422680412371), int(window_height * 0.9217289719626168))

            start_p = pyautogui.pixel(dialog_p2[0], dialog_p2[1])
            self._start_pixel = start_p
            self._dialog_point1 = dialog_p1
            self._dialog_point2 = dialog_p2

    def get_dialog_pixels(self):
        with GameViewStateManager._lock:
            return self._start_pixel, self._dialog_point1, self._dialog_point2

    def get_poketch_colors(self):
        with GameViewStateManager._lock:
            return self._poketch_colors
