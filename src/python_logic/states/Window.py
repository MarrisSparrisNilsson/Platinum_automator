import pygetwindow as pywindow
import threading


class WindowStateManager:
    _instance = None
    _window = None
    _window_size: (int, int) = (0, 0)
    _lock = threading.Lock()

    @staticmethod
    def get_instance():
        if WindowStateManager._instance is None:
            with WindowStateManager._lock:
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
                # print(f"\n{window.title} was detected!")
                try:
                    window = pywindow.getWindowsWithTitle(window.title)[0]
                    self._window = window
                    self._window_size = (window.width, window.height)
                    # print(self._window_size)
                    return
                except IndexError:
                    print("Something went wrong.")
                    exit()
        print("Desmume was not detected.")
        exit(-1)

    def get_window_size(self):
        return self._window_size

    def get_window(self):
        return self._window
