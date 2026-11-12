import pytest

# from src.definitions import SRC_DIR
from src.encounter_methods.Fishing.Feebas.feebas_utils import (
    read_feebas_tile_map,
    read_tiles,
    take_step,
)


def test_feebas_shortest_path_from_tile_map():
    """
    This test goes under the naive assumption that the lake has no obstacles...which it does.
    So this current solution will not work in practice for all positions.
    """

    tiles = read_tiles()
    _, shore_positions = read_feebas_tile_map()

    start_row = row = -1
    start_col = col = len(shore_positions["top"])

    # col = len(shore_positions["top"])

    current_pos = 199
    print()
    print("Start Row:", row)
    print("Start Col:", col)

    for i, tile in enumerate(tiles):

        if i == current_pos + 1:
            break

        if not take_step(tile):
            continue

        # print(tile)

        match tile:
            case "w":
                row -= 1
            case "a":
                col -= 1
            case "s":
                row += 1
            case "d":
                col += 1

        print((row, col))

    take_steps = (row - start_row - 1, col - start_col)

    print("Take Steps:", take_steps)

    assert True
