# External modules
import sys

import pyautogui
import time
import random
import keyboard
import multiprocessing as mp
import threading as thread

# Local modules
import controls
import actions


# res = pyautogui.locateCenterOnScreen("../images/main_py.png", confidence=0.9)
# print(res)

# pyautogui.moveTo(res)
# def on_key_press(event):
#     if event.name == 'esc':
#         actions.watch_quit()


def main():
    print("--- Hello PyAutoGUI! ---")
    steps = random.randint(1, 10)
    print(f"Character is taking: {steps} steps")
    done = [False]
    try:

        # watch_quit_process = mp.Process(target=actions.watch_quit)
        # spinning_action = mp.Process(target=actions.lets_try_spinning)
        t1 = thread.Thread(target=actions.lets_try_spinning, args=(done,), daemon=True)
        # t2 = thread.Thread(target=actions.watch_quit, daemon=True)

        # window_title = "Desmume"
        # win = pyautogui.getWindowsWithTitle(window_title)[0]
        # win.activate()

        print("\nSwitching tab")
        time.sleep(0.5)
        controls.switch_tab()
        time.sleep(2)

        t1.start()
        done[0] = actions.watch_quit()

        # t2.start()

        t1.join()

        # watch_quit_process.start()
        # spinning_process.start()

        # controls.activate_run()
        # for i in range(10):
        # start = time.time()
        # controls.down()
        # time.sleep(0.25 * steps)
        # keyboard.release('s')
        # end = time.time()
        # print(end - start)
        # print(f"{i + 1}: {end - start}")

    except KeyboardInterrupt:
        print("Keyboard listener was interrupted")
    # actions.lets_try_spinning()s

    # quit()
    # sys.exit()
    # pyautogui.hotkey("ctrl", "t")


if __name__ == '__main__':
    # keyboard.on_press_key("esc", on_key_press)

    main()
