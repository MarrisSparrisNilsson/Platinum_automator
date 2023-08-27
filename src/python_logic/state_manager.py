import threading
import uuid

import pygetwindow as pywindow
import file_manager


class ShutdownStateManager:
    _instance = None
    _state: threading.Event = None
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
    _state: threading.Event = None
    _main_state: threading.Event = None
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

    def set_main_state(self, value):
        with PauseStateManager._lock:
            self._main_state = value

    def get_main_state(self):
        with PauseStateManager._lock:
            return self._main_state


class WindowStateManager:
    _instance = None
    _window = None
    _window_size: (int, int) = (0, 0)
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
        # print("Scanning open windows:")
        for i in range(len(all_w)):
            window = all_w[i]
            # print(window.title)
            window_u = str.upper(window.title)
            if window_u.find("DESMUME") != -1 or window_u.find("PAUSED") != -1:
                print(f"\n{window.title} was detected!")
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


class HuntStateManager:
    _instance = None
    _hunt_id: str = str(uuid.uuid4())
    _pokemon_name: str = ""
    _hunt_mode: str = ""
    _encounters: int = 0
    # _hunt_index: int
    _finished: bool = False
    _is_practice: bool = False
    _lock = threading.Lock()

    @staticmethod
    def get_instance():
        if HuntStateManager._instance is None:
            with HuntStateManager._lock:
                if HuntStateManager._instance is None:
                    HuntStateManager._instance = HuntStateManager()
        return HuntStateManager._instance

    def set_hunt_state(self, hunt_id=str(uuid.uuid4()), pokemon_name="Unknown", hunt_mode="", encounters=0, is_practice=False):
        with HuntStateManager._lock:
            self._hunt_id = hunt_id
            self._pokemon_name = pokemon_name
            self._hunt_mode = hunt_mode
            self._encounters = encounters
            self._is_practice = is_practice

    def set_hunt_mode(self, hunt_mode):
        with HuntStateManager._lock:
            self._hunt_mode = hunt_mode

    def get_encounters(self):
        with HuntStateManager._lock:
            return self._encounters

    def increment_encounters(self):
        with HuntStateManager._lock:
            self._encounters += 1

    def finish_hunt(self, is_finished=False):
        with HuntStateManager._lock:
            if not self._is_practice:
                file_manager.save_hunt(self._hunt_id, self._pokemon_name, self._hunt_mode, self._encounters, is_finished)
            else:
                return self._encounters
