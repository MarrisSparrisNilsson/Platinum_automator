import threading

import pyautogui

from src.core.App import app_context


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
            window_width, window_height = app_context.window_size
            dialog_p1 = (int(window_width * 0.032474226804123714), int(window_height * 0.802570093457944))
            dialog_p2 = (int(window_width * 0.4747422680412371), int(window_height * 0.9217289719626168))

            start_p = pyautogui.pixel(dialog_p2[0], dialog_p2[1])
            self.start_pixel = start_p
            self.dialog_point1 = dialog_p1
            self.dialog_point2 = dialog_p2

    def get_dialog_pixels(self):
        with self.lock:
            return self.start_pixel, self.dialog_point1, self.dialog_point2

    def get_poketch_colors(self):
        with self.lock:
            return self.poketch_colors


game_context = GameContext()
