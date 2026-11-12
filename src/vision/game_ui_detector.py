from pathlib import Path

import pyautogui
import pytesseract

from src.core.Game import game_context


def dialog_is_open():
    start_p, dialog_p1, dialog_p2 = game_context.get_dialog_pixels()
    if pyautogui.pixelMatchesColor(dialog_p1[0], dialog_p1[1], (255, 255, 255)) and not pyautogui.pixelMatchesColor(
        dialog_p2[0], dialog_p2[1], start_p
    ):
        return True
    else:
        return False


def has_background_changed(x, y, pixel):
    if not pyautogui.pixelMatchesColor(x, y, pixel):
        #  print(f"P: {pyautogui.pixel(x, y)}, {pixel}")
        return True
    else:
        return False


def is_same_object_showing(obj_image_path, region):
    try:
        if pyautogui.locateCenterOnScreen(image=str(obj_image_path), region=region):
            return True
    except pyautogui.ImageNotFoundException:
        return False


def is_target_string_found(target_string: str, target_string_img_path: Path, accuracy=0.5):
    """
    Checks if the target string is found.
    """

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

    reading_configs = ["--psm 7", "--psm 8"]
    largest_match_count = 0
    target_string = target_string.lower().replace("_", " ")
    for i in range(len(reading_configs)):
        reading = pytesseract.image_to_string(str(target_string_img_path), config=reading_configs[i])
        reading = str(reading).strip().lower()

        # print(reading)

        if reading == target_string:
            return True
        # print(reading)
        matching_chars = 0
        i = 0
        while i < len(target_string) and i < len(reading):
            if reading[i] == target_string[i]:
                matching_chars += 1
            i += 1
        if matching_chars > largest_match_count:
            largest_match_count = matching_chars

    # If the words that are in order match and exceed the accuracy threshold:
    # => we assume we found the target string
    return True if largest_match_count / len(target_string) >= accuracy else False

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
