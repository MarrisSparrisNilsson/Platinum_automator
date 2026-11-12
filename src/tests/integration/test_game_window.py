"""
This test file is used to write test for the EMULATION WINDOW as well as IN-GAME OBSERVATIONS.

This may include INTEGRATION AND UNIT TESTS.
"""

import threading as thread
import time

import keyboard
import pyautogui
import pytest
from pygetwindow import Win32Window

from src.automation import controls
from src.automation.actions import watch_exit
from src.core.App import app_context
from src.core.Game import normalize_pixel_coords, normalize_region
from src.states.Shutdown import ShutdownStateManager
from src.vision.encounter_detector import get_encounter_pixels
from src.window.focus import set_window_focus
from src.window.game_object_region_definitions import UI_ELEMENT_PIXELS, UI_ELEMENTS


@pytest.fixture
def window_state_init():
    app_context.set_window_state()
    print()

    return app_context.get_window()


@pytest.mark.integration
def test_window_state_init(window_state_init):
    window = window_state_init

    assert window is not None


@pytest.mark.integration
def test_set_window_focus(window_state_init):
    """
    Test will NOT pass in debug mode when DESMUME window CANNOT be IS_ACTIVE == TRUE
    """
    set_window_focus()

    window: Win32Window = app_context.get_window()

    desmume_app = "DESMUME" in window.title.upper() or "PAUSED" in window.title.upper()

    window_focus = desmume_app and window.isActive
    if window_focus:
        print("DESMUME got focus")
        controls.switch_tab()

    assert window_focus == True


# def test_window_focus_thread(window_state_init):


@pytest.mark.integration
def test_monitor_window_move(window_state_init):
    window: Win32Window = window_state_init
    start_left_pos = window.left
    start_top_pos = window.top

    """NOTE: Use 'esc' button to exit the loop inside monitor_window to finish the test."""
    esc_btn = thread.Thread(target=watch_exit, daemon=True)
    esc_btn.start()
    window.activate()
    window = app_context.monitor_window()
    controls.switch_tab()

    assert (start_left_pos != window.left) or (start_top_pos != window.top)


def capture_pixel_info(x: int = 0, y: int = 0):
    if x > 0 and y > 0:
        pixel = pyautogui.pixel(x, y)
    else:
        mouse = pyautogui.position()
        print(mouse)
        x = int(mouse.x)
        y = int(mouse.y)
        pixel = pyautogui.pixel(x, y)

    window: Win32Window = app_context.get_window()

    w, h = window.size
    print(x, y)

    print(f"Pixel RGB: {pixel}")
    pyautogui.moveTo(x, y)

    percent_w = x / w
    print(f"W: {percent_w}")
    percent_h = y / h
    print(f"H: {percent_h}")
    print()

    x_offset, y_offset = window.topleft
    print(f"Window size: [{w} x {h}]")
    print(f"Window position: ({x_offset},{y_offset})")

    return x, y


@pytest.mark.integration
def test_get_screen_pixels_from_float(window_state_init):
    window: Win32Window = window_state_init
    window.activate()
    time.sleep(1)

    float_x = 0.25
    float_y = 0.42757009345794394
    # float_y = 0.18574766355140188 + (0 * (0.24065420560747663 - 0.12967289719626168))

    # 0.077588785046729

    # x = int((window.left + 9) + (window.width * 0.12474226804123711))
    # y = int(window.height * 0.20327102803738317 + window.height * (0.077588785046729))

    x = int(window.width * float_x)
    y = int(window.height * float_y)

    """NOTE: Use 'esc' button to exit the loop inside monitor_window to finish the test."""
    # esc_btn = thread.Thread(target=watch_exit, daemon=True)
    # esc_btn.start()

    capture_pixel_info(x, y)

    assert True


@pytest.mark.integration
def test_get_screen_pixels_from_mouse(window_state_init, MULTI_PIXEL_TEST=False):
    window: Win32Window = window_state_init
    window.activate()
    time.sleep(1)

    """NOTE: Use 'esc' button to exit the loop inside monitor_window to finish the test."""

    if MULTI_PIXEL_TEST:
        esc_btn = thread.Thread(target=watch_exit, daemon=True)
        esc_btn.start()

        while True:
            time.sleep(0.5)

            print("Move mouse to pixel to capture and press 'k' key.")
            keyboard.wait("k")
            if ShutdownStateManager.get_instance().is_shutting_down():
                break
            capture_pixel_info()
    else:
        watch_exit()
        capture_pixel_info()

    assert True


@pytest.mark.integration
def test_normalize_pixel_coords(
    window_state_init,
    LOOP=False,
    OFFSET=True,
    X_OFFSET=False,
):
    window: Win32Window = window_state_init
    window.activate()
    time.sleep(1)

    if LOOP:
        """LOOP PIXELS"""
        pixel_list = []
        for p in pixel_list:
            x, y = p
            capture_pixel_info(x, y)
            time.sleep(2)
    else:
        """NOTE: Select a pixel on the screen to test the normalization of pixel coordinates."""
        if OFFSET:
            offset = UI_ELEMENT_PIXELS["list_item_border_y_offset"]
            section = 4
            x = UI_ELEMENT_PIXELS["registered_item"][0] + (section * offset if X_OFFSET else 0)
            y = UI_ELEMENT_PIXELS["registered_item"][1] + (section * offset if not X_OFFSET else 0)
        else:
            x = UI_ELEMENT_PIXELS["bag_section_coord"][0]
            y = UI_ELEMENT_PIXELS["bag_section_coord"][1]

        x, y = normalize_pixel_coords(x, y)
        capture_pixel_info(x, y)

    """NOTE: Use 'esc' button to exit the loop inside monitor_window to finish the test."""
    # esc_btn = thread.Thread(target=watch_exit, daemon=True)
    # esc_btn.start()

    assert True


@pytest.mark.integration
def test_normalize_region_from_coords(window_state_init):
    window: Win32Window = window_state_init
    window.activate()
    time.sleep(1)

    """NOTE: Select a pixel on the screen to test the normalization of pixel coordinates."""

    region = normalize_region(region=UI_ELEMENTS["pokemon_name"])

    left, top, width, height = region

    pixel_list = [
        (left, top),
        (left + width, top),
        (left + width, top + height),
        (left, top + height),
    ]

    time_out = 0.01
    for _ in range(8):
        for pixel in pixel_list:
            pyautogui.moveTo(*pixel)
            time.sleep(time_out)

    window: Win32Window = app_context.get_window()

    # print()
    w, h = window.size
    x_offset, y_offset = window.topleft
    print(f"Window size: {w}x{h}")
    print(f"Window position: {x_offset},{y_offset}")

    assert True


@pytest.mark.integration
def test_get_all_pixels(window_state_init):
    window: Win32Window = window_state_init
    window.activate()
    time.sleep(1)

    print()
    for name, p in UI_ELEMENT_PIXELS.items():
        if type(p) is not int:
            x, y = p
            print(name, f"({x}, {y})")
            keyboard.wait("esc")

            pyautogui.moveTo(x, y)

    assert True
