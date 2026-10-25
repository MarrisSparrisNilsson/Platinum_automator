import json

import numpy as np

from src.definitions import SRC_DIR

# from pathlib import Path


def take_step(tile):
    """
    Blocks walking at some locations where only turning is desired.
    :param tile: Tile number along the predefined path.
    :return: False => Don't move. True => Move.
    """
    blocked = {3, 29, 93, 98, 102, 222, 323, 455, 457, 483, 521, 527}
    return False if tile in blocked else True


def read_feebas_tile_map(tile_map: str = "feebas_tile_map") -> tuple:
    """
    Read the pre-constructed numerically represented feebas lake.

    Returns: Tuple
        - ``feebas_map``: A 2D array containing: 0 (water), 1 (fishable rock), 2 (solid rocks
        - ``start_positions``: Dict with 1D array containing start pos for vertical or horizontal start positions.)
    """

    map_file_path = SRC_DIR / f"resources/{tile_map}.json"
    # Ensure the resources directory exists
    if not map_file_path.exists():
        raise FileNotFoundError(f"{tile_map} does not exist")

    with open(map_file_path, "r") as f:
        feebas_map = json.load(f)

    np_map = np.array(feebas_map)

    top_start_points = np_map[0][1:]
    left_start_points = np_map[:, 0][1:]
    feebas_map = np_map[1:, 1:].copy().tolist()

    # Start positions may look like: [4, 4, 4, 3, 3, 3, 3]
    shore_positions = {"top": top_start_points, "left": left_start_points}

    return feebas_map, shore_positions
