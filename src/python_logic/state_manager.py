import threading


class ExitStateManager:
    _instance = None
    _state = None
    _lock = threading.Lock()

    @staticmethod
    def get_instance():
        if ExitStateManager._instance is None:
            with ExitStateManager._lock:
                if ExitStateManager._instance is None:
                    ExitStateManager._instance = ExitStateManager()
        return ExitStateManager._instance

    def set_state(self, value):
        with ExitStateManager._lock:
            self._state = value

    def get_state(self):
        with ExitStateManager._lock:
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
