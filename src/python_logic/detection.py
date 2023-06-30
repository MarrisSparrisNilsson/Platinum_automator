import pyautogui


def find_pause_and_resume():
    # screenshot = pyautogui.screenshot(region=(0, 0, 210, 100))
    # screenshot.save("../images/test.png")

    # pyautogui.moveTo(res)

    res = pyautogui.locateCenterOnScreen("../images/paused.png", region=(0, 0, 210, 100), confidence=0.9)
    if res is None:
        print("Pause button was not found.")
    else:
        pyautogui.click(res)
        print(res)
