import threading
import pygetwindow as pywindow


class ShutdownStateManager:
    _instance = None
    _state = None
    _lock = threading.Lock()

    @staticmethod
    def get_instance():
        if ShutdownStateManager._instance is None:
            with ShutdownStateManager._lock:
                if ShutdownStateManager._instance is None:
                    ShutdownStateManager._instance = ShutdownStateManager()
        return ShutdownStateManager._instance

    def set_state(self, value):
        with ShutdownStateManager._lock:
            self._state = value

    def get_state(self):
        with ShutdownStateManager._lock:
            return self._state


class PauseStateManager:
    _instance = None
    _state = None
    _lock = threading.Lock()

    @staticmethod
    def get_instance():
        if PauseStateManager._instance is None:
            with PauseStateManager._lock:
                if PauseStateManager._instance is None:
                    PauseStateManager._instance = PauseStateManager()
        return PauseStateManager._instance

    def set_state(self, value):
        with PauseStateManager._lock:
            self._state = value

    def get_state(self):
        with PauseStateManager._lock:
            return self._state


class WindowStateManager:
    _instance = None
    _window = None
    _window_size = (0, 0)
    _lock = threading.Lock()

    @staticmethod
    def get_instance():
        if WindowStateManager._instance is None:
            # with WindowStateManager._lock:
            if WindowStateManager._instance is None:
                WindowStateManager._instance = WindowStateManager()
        return WindowStateManager._instance

    def set_state(self):
        # Find window dynamically
        all_w = pywindow.getAllWindows()
        for i in range(len(all_w)):
            window = all_w[i]
            print(window.title)
            window_u = str.upper(window.title)
            if window_u.find("DESMUME") != -1 or window_u.find("PAUSED") != -1:
                print(f"{window.title} was detected!")
                try:
                    window = pywindow.getWindowsWithTitle(window.title)[0]
                    self._window = window
                    self._window_size = (window.width, window.height)
                    return
                except IndexError:
                    print("Something went wrong.")
                    exit()
        print("Desmume was not detected.")

    def get_window_size(self):
        return self._window_size

    def get_window(self):
        return self._window
