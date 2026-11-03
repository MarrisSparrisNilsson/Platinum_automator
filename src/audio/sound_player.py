import os

from src.definitions import SRC_DIR

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame


def play_sound(sound_file_name: str, volume: float = 0.1):
    # sound_file_name = "Level_up.mp3"
    if not sound_file_name.endswith(".mp3"):
        sound_file_name = sound_file_name + ".mp3"

    # Construct the file path
    sound_path = SRC_DIR / "assets/sfx" / sound_file_name

    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()
