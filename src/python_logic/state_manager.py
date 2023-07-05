import threading


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
            # with PauseStateManager._lock:
            if PauseStateManager._instance is None:
                PauseStateManager._instance = PauseStateManager()
        return PauseStateManager._instance

    def set_state(self, value):
        # with PauseStateManager._lock:
        self._state = value

    def get_state(self):
        # with PauseStateManager._lock:
        return self._state
