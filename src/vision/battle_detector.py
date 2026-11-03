import time

import pyautogui
import pytesseract

from src.core.App import app_context
from src.definitions import SRC_DIR
from src.states.Shutdown import ShutdownStateManager
from src.vision.game_ui_detector import has_background_changed

# TODO: Tesseract OCR
"""
Tesseract Page Segmentation Modes (PSM):
    0 = Orientation and script automation (OSD) only.
    1 = Automatic page segmentation with OSD.
    2 = Automatic page segmentation, but no OSD, or OCR. (not implemented)
    3 = Fully automatic page segmentation, but no OSD. (Default)
    4 = Assume a single column of text of variable sizes.
    5 = Assume a single uniform block of vertically aligned text.
    6 = Assume a single uniform block of text.
    7 = Treat the image as a single text line.
    8 = Treat the image as a single word.
    9 = Treat the image as a single word in a circle.
   10 = Treat the image as a single character.
   11 = Sparse text. Find as much text as possible in no particular order.
   12 = Sparse text with OSD.
   13 = Raw line. Treat the image as a single text line,
         bypassing hacks that are Tesseract-specific.
"""


def was_target_pokemon_found(pokemon_name: str):
    # Pokémon name coordinates:
    # (
    #     window.left + 9,
    #     int(window.height * 0.20327102803738317),
    #     int(window.width * 0.12474226804123711),
    #     int(window.height * (0.28085981308411217 - 0.20327102803738317))
    # )

    window = app_context.window

    pokemon_name_img_path = SRC_DIR / "assets/images/local/pokemon_name.png"
    pyautogui.screenshot(
        str(pokemon_name_img_path),
        region=(
            window.left + 9,
            int(window.height * 0.20327102803738317),
            int(window.width * 0.12474226804123711),
            int(window.height * (0.28085981308411217 - 0.20327102803738317)),
        ),
    )

    reading_configs = ["--psm 7", "--psm 8"]
    largest_match_count = 0
    for i in range(len(reading_configs)):
        matching_chars = 0
        reading = pytesseract.image_to_string(str(pokemon_name_img_path), config=reading_configs[i])
        if reading == pokemon_name:
            return True
        # print(reading)
        i = 0
        while i < len(pokemon_name) and i < len(reading):
            if reading[i] == pokemon_name[i]:
                matching_chars += 1
            i += 1
        if matching_chars > largest_match_count:
            largest_match_count = matching_chars

    # If 50% of the words that are in order match, we assume we found the target Pokémon
    return True if largest_match_count / len(pokemon_name) >= 0.5 else False

    # img = cv2.imread("../images/pokemon_name.png")
    # w, h, _ = img.shape
    #
    # boxes = pytesseract.image_to_boxes(img, config=read_name_config)
    #
    # string = ""
    # for box in boxes.splitlines():
    #     print(box)
    #     box = box.split(" ")
    #     print(box)
    #     string += box[0]
    #     img = cv2.rectangle(img, (int(box[1]), h - int(box[2])), (int(box[3]), h - int(box[4])), (255, 0, 0), 2)
    #
    # cv2.imshow("img", img)
    # cv2.waitKey(0)
    # pokemon_name = string
    # pokemon_name = pytesseract.image_to_string("../images/feebas_text.png", config=read_name_config)
    # print(pokemon_name)


def find_sparkles():
    window_width, window_height = app_context.window_size

    x1 = int(window_width * 0.2630359212050985)
    y1 = int(window_height * 0.27670250896057347)

    x2 = int(window_width * 0.36993047508690613)
    y2 = int(window_height * 0.6336917562724015)

    x3 = int(window_width * 0.45712630359212053)
    y3 = int(window_height * 0.2623655913978495)

    x4 = int(window_width * 0.3579142526071842)
    y4 = int(window_height * 0.1013620071684588)

    x5 = int(window_width * 0.45654692931633833)
    y5 = int(window_height * 0.5684587813620071)

    coords = [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5)]

    # time.sleep(1)  # Seconds until Pokémon stands still
    shiny_p1 = pyautogui.pixel(x1, y1)
    shiny_p2 = pyautogui.pixel(x2, y2)
    shiny_p3 = pyautogui.pixel(x3, y3)
    shiny_p4 = pyautogui.pixel(x4, y4)
    shiny_p5 = pyautogui.pixel(x5, y5)

    shiny_p = [shiny_p1, shiny_p2, shiny_p3, shiny_p4, shiny_p5]

    duration = 0
    print("\nSearching for sparkles...🔎")
    start_time = time.time()
    while duration < 2.2:  # Sparkles duration
        if ShutdownStateManager.get_instance().is_shutting_down():
            return

        for i in range(len(shiny_p)):
            x, y = coords[i]
            if has_background_changed(x, y, shiny_p[i]):
                return True

        end_time = time.time()
        duration = end_time - start_time
        # print(duration)

    print("No shiny this time...☹️\n")
    return False
