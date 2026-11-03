# core/application_context.py

import threading
import time

import pygetwindow as pywindow

from src.states.Shutdown import ShutdownStateManager


class ApplicationContext:
    def __init__(self):
        self.hunt_event = threading.Event()

        self.window: pywindow.Win32Window = None
        self.window_size = (0, 0)
        self.window_position = (0, 0)

        self._lock = threading.Lock()

    def is_hunt_paused(self):
        return self.hunt_event.is_set()

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
                    window: pywindow.Win32Window = pywindow.getWindowsWithTitle(window.title)[0]
                    with self._lock:
                        self.window = window
                        self.window_id = window._hWnd
                        self.window_size = (window.width, window.height)
                        self.window_position = (self.window.left, self.window.top)
                    return

                except IndexError:
                    raise RuntimeError("Failed to retrieve DeSmuME window.")

        raise RuntimeError("DeSmuME window was not detected.")

    def monitor_window(self):
        """
        Thread method for checking window properties and if focus is lost, then update and notify APP_CONTEXT when changes happen.
        """

        last_size = self.window_size
        last_position = self.window_position
        desmume_title = self.window.title

        window: pywindow.Win32Window = pywindow.getWindowsWithTitle(desmume_title)[0]
        # window.activate()
        window.moveTo(-6, 0)

        while not ShutdownStateManager.get_instance().is_shutting_down():

            window_title = pywindow.getActiveWindowTitle()

            # Desmume Window lost focus
            if window_title != desmume_title:
                print("Lost desmume focus")
                # pause_manager = PauseStateManager.get_instance()
                # Pause all I/O actions across program execution

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

        return self.window


app_context = ApplicationContext()
