# core/application_context.py

import threading
import time

import pygetwindow as pywindow


class ApplicationContext:
    def __init__(self):
        self.shutdown_event = threading.Event()
        self.hunt_event = threading.Event()
        self.encounter_detection_event = threading.Event()

        self.window = None
        self.window_size = (0, 0)
        self.window_position = (0, 0)

        self._lock = threading.Lock()

    def is_shutdown(self):
        return self.shutdown_event.is_set()

    def is_hunt_paused(self):
        return self.hunt_event.is_set()

    def is_encounter_detection_paused(self):
        return self.encounter_detection_event.is_set()

    def get_window(self):
        return self.window

    def set_window_state(self):
        """
        Find the DeSmuME window and update
        'self.window', 'self.window_position' and 'self.window_size'.
        """

        all_windows = pywindow.getAllWindows()

        for window in all_windows:
            title = window.title.upper()

            if "DESMUME" in title or "PAUSED" in title:
                try:
                    window = pywindow.getWindowsWithTitle(window.title)[0]
                    with self._lock:
                        self.window = window
                        self.window_size = (window.width, window.height)
                        self.window_position = (self.window.left, self.window.top)
                    return

                except IndexError:
                    raise RuntimeError("Failed to retrieve DeSmuME window.")

        raise RuntimeError("DeSmuME window was not detected.")

    def monitor_window(self):
        last_size = self.window_size
        last_position = self.window_position
        while not self.shutdown_event.is_set():

            if self.window:

                current_size = (self.window.width, self.window.height)
                current_position = (self.window.left, self.window.top)

                if current_size != last_size:
                    with self._lock:
                        self.window_size = current_size
                    print(f"Window resized from: {last_size} -> {current_size}")
                    last_size = current_size

                if current_position != last_position:
                    with self._lock:
                        self.window_position = current_position
                    print(f"Window moved from: {last_position} -> {current_position}")
                    last_position = current_position

            time.sleep(0.25)


app_context = ApplicationContext()
