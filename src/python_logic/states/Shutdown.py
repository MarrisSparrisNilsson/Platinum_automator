import threading


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

    def check_shutdown_state(self):
        shutdown_event = self.get_state()
        if shutdown_event is not None:
            return True
        else:
            return False
