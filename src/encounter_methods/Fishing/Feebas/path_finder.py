"""
path_finder.py
=====================
Generates a Hamiltonian path through the Feebas lake given any eligible
starting shore tile (type 3).

Tile encoding
-------------
    - **0  WALKABLE AND FISHABLE**          → must be visited exactly once \n
    - **1  NOT WALKABLE AND FISHABLE**      → must be faced (adjacent to any visited tile) \n
    - **2  NOT WALKABLE AND NOT FISHABLE**  → solid wall, cannot enter \n
    - **3  ELIGIBLE ROUTE STARTING POINT**  → shore entry tile \n
    - **4  BLOCKED SHORE TILE**             → no entry allowed \n

Algorithm: Randomized Warnsdorff + Connectivity Guard
-----------------------------------------------------
1. **Warnsdorff's Heuristic**

    At each step, rank candidate moves by how many unvisited neighbors the destination tile has — "prefer the most constrained next
    step". This is the classic Knight's Tour heuristic and avoids dead-ends on open grids.

2. **Connectivity Guard**

    Before committing to a move, verify that the remaining unvisited tiles will still form a single connected component. This prevents
    the path from inadvertently isolating a cluster of tiles that can never be reached again. The check uses a local BFS from the
    candidate tile's unvisited neighbors (fast for nearby splits) with a global BFS fallback for long-range splits.

3. **Randomized Tie-Breaking**

    When two candidates share the same Warnsdorff degree, a seeded RNG breaks the tie. Re-running with different seeds explores different
    path branches without expensive backtracking.

Parity Constraint
-----------------
    The 523 walkable tiles colored as 262 "black" (r+c even) and 261 "white" tiles on a checkerboard. A Hamiltonian path on a bipartite
    grid graph must alternate colors, so it must start AND end on the majority color (black). Shore tiles that enter the lake on a white
    tile are therefore structurally unsolvable — the algorithm detects this and skips them immediately.

    Of the 42 type-3 shore tiles, exactly 21 have valid (black) entry points; the other 21 are parity-impossible. Of the 21 valid ones,
    20 are confirmed to solve within 500 random seeds. Shore (0,17) is parity-valid but may require more seeds due to the tight corridor
    in the top-right corner of the lake — the algorithm will try up to max_seeds before reporting it as unsolved.
"""

import json
import random
import sys
from collections import deque
from pathlib import Path

from src.definitions import SRC_DIR

# from src.encounter_methods.Fishing.Feebas.feebas import walkable_tiles, lake_entries, parity_valid, _attempt
from src.encounter_methods.Fishing.Feebas.feebas_utils import read_feebas_tile_map
from src.UI.CLI.Fishing.feebas_menus import select_start_shore_pos

# ---------------------------------------------------------------------------
# Tile constants
# ---------------------------------------------------------------------------
WALKABLE = 0  # must visit
FACE_ONLY = 1  # must face (be adjacent to), cannot stand on
WALL = 2  # impassable
SHORE_OPEN = 3  # valid entry point on shore
SHORE_BLOCK = 4  # blocked shore tile

DIRS = [(-1, 0, "w"), (1, 0, "s"), (0, -1, "a"), (0, 1, "d")]


def find_path(grid, shore: tuple[int, int], max_seeds: int = 500, verbose: bool = True) -> dict | None:
    """
    Find a Hamiltonian path starting from the given shore tile.

    Args:
        grid        : 2D tile map.
        shore       : (row, col) coordinates of a type-3 shore tile.
        max_seeds   : Maximum number of random seeds to try.
        verbose     : Whether to print search progress.

    Returns:
        A dictionary containing

        -``shore``: Starting shore coordinates.

        -``entry``: First lake tile coordinates.

        -``entry_key``: WASD key used to reach the entry tile.

        -``positions``: Coordinates of all tiles along the path.

        -``path``: WASD movement keys.

        -``steps``: Total number of steps taken.

        or None if no solution is found.
    """

    all_tiles = walkable_tiles(grid)
    entries = lake_entries(grid, *shore, all_tiles)

    if not entries:
        if verbose:
            print(f"  Shore {shore}: no walkable lake neighbor.")
        return None

    for entry_r, entry_c, entry_key in entries:
        # Fast parity check before spending any cycles
        if not parity_valid((entry_r, entry_c), all_tiles):
            if verbose:
                print(f"  Shore {shore} → entry ({entry_r},{entry_c}): " f"wrong parity (structurally unsolvable).")
            continue

        if verbose:
            print(f"  Shore {shore} → entry ({entry_r},{entry_c}) " f"via '{entry_key}' [parity OK] searching…", end=" ", flush=True)

        for seed in range(max_seeds):
            result = _attempt(grid, all_tiles, (entry_r, entry_c), seed)
            if result is not None:
                lake_path, lake_keys = result
                if verbose:
                    print(f"found at seed {seed}.")
                return {
                    "shore": shore,
                    "entry": (entry_r, entry_c),
                    "entry_key": entry_key,
                    "positions": [shore] + lake_path,
                    "path": [entry_key] + lake_keys,
                    "steps": 1 + len(lake_keys),
                }

        if verbose:
            print(f"not found in {max_seeds} seeds.")

    return None


# ---------------------------------------------------------------------------
# Grid helpers
# ---------------------------------------------------------------------------


def load_grid(path: str | Path) -> list[list[int]]:
    with open(path) as f:
        return [list(row) for row in json.load(f)]


def walkable_tiles(grid) -> frozenset:
    return frozenset((r, c) for r, row in enumerate(grid) for c, v in enumerate(row) if v == WALKABLE)


def face_only_tiles(grid) -> frozenset:
    return frozenset((r, c) for r, row in enumerate(grid) for c, v in enumerate(row) if v == FACE_ONLY)


def shore_starts(grid) -> list[tuple[int, int]]:
    return [(r, c) for r, row in enumerate(grid) for c, v in enumerate(row) if v == SHORE_OPEN]


def lake_entries(grid, shore_r, shore_c, all_tiles) -> list[tuple[int, int, str]]:
    """

    :param grid:
    :param shore_r:
    :param shore_c:
    :param all_tiles:
    :return: A list of valid entry points
    """
    rows, cols = len(grid), len(grid[0])
    return [
        (shore_r + row_dir, shore_c + col_dir, key)
        for row_dir, col_dir, key in DIRS
        if ((0 <= shore_r + row_dir < rows) and (0 <= shore_c + col_dir < cols) and ((shore_r + row_dir, shore_c + col_dir) in all_tiles))
    ]


def check_connected(all_tiles) -> bool:
    """Return True if all walkable tiles form a single connected component."""
    if not all_tiles:
        return True
    seed = next(iter(all_tiles))
    seen = {seed}
    q = deque([seed])
    while q:
        r, c = q.popleft()
        for dr, dc, _ in DIRS:
            t = (r + dr, c + dc)
            if t in all_tiles and t not in seen:
                seen.add(t)
                q.append(t)
    return seen == all_tiles


def parity_valid(entry: tuple[int, int], all_tiles: frozenset) -> bool:
    """
    Check the bipartite parity condition.
    Colour each tile (r+c) % 2. A Hamiltonian path on a bipartite grid must
    start on the majority colour. Returns True if `entry` is majority-coloured.
    """
    black = sum(1 for r, c in all_tiles if (r + c) % 2 == 0)
    white = len(all_tiles) - black
    entry_colour = (entry[0] + entry[1]) % 2  # 0 = black, 1 = white
    majority = 0 if black >= white else 1
    return entry_colour == majority


# ---------------------------------------------------------------------------
# Core algorithm
# ---------------------------------------------------------------------------


def _wdeg(grid, rows, cols, r, c, visited):
    """Warnsdorff degree: number of unvisited walkable neighbors."""
    return sum(
        1
        for new_row, new_col in ((r + dr, c + dc) for dr, dc, _ in DIRS)
        if (0 <= new_row < rows and 0 <= new_col < cols and grid[new_row][new_col] == WALKABLE and (new_row, new_col) not in visited)
    )


def _splits_graph(pos, visited, all_tiles, depth=20):
    """
    Return True if adding `pos` to `visited` disconnects the remaining tiles.

    Uses a local BFS (radius = depth) from the candidate's unvisited neighbors
    for speed. Falls back to a global BFS only when the local check is
    inconclusive (i.e. some neighbors weren't reachable within `depth` steps).
    """
    remaining = all_tiles - visited
    if len(remaining) <= 1:
        return False

    # Unvisited walkable neighbors of `pos`
    neighbors = [(pos[0] + row_dir, pos[1] + col_dir) for row_dir, col_dir, _ in DIRS if (pos[0] + row_dir, pos[1] + col_dir) in remaining]
    if len(neighbors) <= 1:
        return False  # 0 or 1 neighbor → can't split

    # Local BFS: can all neighbors reach each other without going through pos?
    start, targets = neighbors[0], set(neighbors[1:])
    found = set()
    queue = deque([(start, 0)])
    seen = {start, pos}
    while queue and targets - found:
        curr, d = queue.popleft()
        if d >= depth:
            continue
        for row_dir, col_dir, _ in DIRS:
            tile = (curr[0] + row_dir, curr[1] + col_dir)
            if tile in all_tiles and tile not in seen and tile not in visited:
                seen.add(tile)
                queue.append((tile, d + 1))
                if tile in targets:
                    found.add(tile)

    if found >= targets:
        return False  # all neighbors reachable locally → no split

    # Inconclusive: global BFS fallback
    seed_tile = next(iter(remaining))
    seen2 = {seed_tile}
    q = deque([seed_tile])
    while q:
        r, c = q.popleft()
        for row_dir, col_dir, _ in DIRS:
            tile = (r + row_dir, c + col_dir)
            if tile in remaining and tile not in seen2:
                seen2.add(tile)
                q.append(tile)
    return len(seen2) < len(remaining)


def _attempt(grid, all_tiles, entry, seed):
    """
    One greedy Warnsdorff + connectivity attempt from `entry` with given seed.
    Returns:
         (path, wasd_keys) on success, or None if the walk stalls.
    """
    rows = len(grid)
    cols = len(grid[0])
    total = len(all_tiles)
    rng = random.Random(seed)

    visited = {entry}
    pos = entry
    path = [entry]
    keys = []

    for _ in range(total - 1):
        r, c = pos
        candidates = []
        for row_dir, col_dir, key in DIRS:
            new_row, new_col = r + row_dir, c + col_dir
            if 0 <= new_row < rows and 0 <= new_col < cols and grid[new_row][new_col] == WALKABLE and (new_row, new_col) not in visited:
                new_vis = visited | {(new_row, new_col)}
                deg = _wdeg(grid, rows, cols, new_row, new_col, new_vis)
                candidates.append((deg, rng.random(), new_row, new_col, key))

        if not candidates:
            return None  # stuck

        candidates.sort()

        # Pick the first candidate that doesn't disconnect remaining tiles
        chosen = None
        for deg, _, new_row, new_col, key in candidates:
            if not _splits_graph((new_row, new_col), visited | {(new_row, new_col)}, all_tiles):
                chosen = (new_row, new_col, key)
                break

        # If connectivity guard blocked everything, take the Warnsdorff-best anyway
        if chosen is None:
            chosen = (candidates[0][2], candidates[0][3], candidates[0][4])

        new_row, new_col, key = chosen
        visited.add((new_row, new_col))
        pos = (new_row, new_col)
        path.append(pos)
        keys.append(key)

    if len(path) == total:
        return path, keys
    return None


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def validate(grid, result: dict) -> dict:
    """Full correctness check on a solution dict."""
    all_tiles = walkable_tiles(grid)
    type1 = face_only_tiles(grid)
    positions = result["positions"]
    pos_set = set(positions)
    issues = []

    # Every consecutive step is adjacent (distance 1)
    adj_ok = all(
        abs(positions[i][0] - positions[i + 1][0]) + abs(positions[i][1] - positions[i + 1][1]) == 1 for i in range(len(positions) - 1)
    )
    if not adj_ok:
        issues.append("Non-adjacent step found.")

    # No tile visited twice
    no_revisit = len(positions) == len(set(positions))
    if not no_revisit:
        dup = [p for p in set(positions) if positions.count(p) > 1]
        issues.append(f"Revisited tiles: {dup[:5]}")

    # All walkable lake tiles covered (excluding the shore itself)
    lake_visited = pos_set - {result["shore"]}
    all_covered = lake_visited == all_tiles
    if not all_covered:
        missing = all_tiles - lake_visited
        issues.append(f"Missing {len(missing)} tile(s): {sorted(missing)[:5]}")

    # Every type-1 tile is adjacent to at least one visited tile
    uncovered_1 = {t for t in type1 if not any((t[0] + dr, t[1] + dc) in pos_set for dr, dc, _ in DIRS)}
    type1_ok = not uncovered_1
    if not type1_ok:
        issues.append(f"Non-faced type-1 tiles: {uncovered_1}")

    return {
        "ok": adj_ok and no_revisit and all_covered and type1_ok,
        "adjacent": adj_ok,
        "no_revisit": no_revisit,
        "all_covered": all_covered,
        "type1_faced": type1_ok,
        "issues": issues,
    }


# ---------------------------------------------------------------------------
# ASCII visualization
# ---------------------------------------------------------------------------


def visualize(grid, positions=None):
    sym = {WALKABLE: "·", FACE_ONLY: "F", WALL: "█", SHORE_OPEN: "╡", SHORE_BLOCK: "▓"}
    rows, cols = len(grid), len(grid[0])
    disp = [[sym.get(grid[r][c], "?") for c in range(cols)] for r in range(rows)]
    if positions:
        for step, (r, c) in enumerate(positions):
            disp[r][c] = str(step % 10)
    print("┌" + "─" * cols + "┐")
    for row in disp:
        print("│" + "".join(row) + "│")
    print("└" + "─" * cols + "┘")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def find_feebas_path(max_seeds=500):
    """
    Entry point for generating a dynamic feebas hunt path based on starting position.
    """

    grid, start_positions = read_feebas_tile_map()

    # grid = load_grid(grid_file)
    all_tiles = walkable_tiles(grid)
    type1 = face_only_tiles(grid)
    starts = shore_starts(grid)

    rows, cols = len(grid), len(grid[0])
    black = sum(1 for r, c in all_tiles if (r + c) % 2 == 0)
    white = len(all_tiles) - black

    print(f"Grid          : {rows} × {cols}")
    print(f"Walkable tiles: {len(all_tiles)}  (black={black}, white={white})")
    print(f"Majority color: {'black (r+c even)' if black >= white else 'white (r+c odd)'}")
    print(f"Type-1 tiles  : {sorted(type1)}")
    print(f"Shore starts  : {len(starts)}")
    print(f"Connected     : {check_connected(all_tiles)}")
    print()

    start_pos_coord = select_start_shore_pos(start_positions)
    # Determine which starts to attempt
    if start_pos_coord is None:
        targets = starts  # try all, stop at first solution
        stop_first = True
    elif start_pos_coord == "all":
        targets = starts
        stop_first = False
    else:
        if start_pos_coord not in set(starts):
            print(f"Error: {start_pos_coord} is not a type-3 shore tile.")
            sys.exit(1)
        targets = [start_pos_coord]
        stop_first = True

    # Find solutions
    solutions = []
    for shore in targets:
        print(f"Shore {shore}:")
        result = find_path(grid, shore, max_seeds=max_seeds, verbose=True)
        if result is None:
            continue

        # Validate path
        report = validate(grid, result)
        if report["ok"]:
            print(f"  Validation  : ✓  steps={result['steps']}  " f"type1_faced={report['type1_faced']}")
        else:
            print(f"  Validation  : ✗  issues={report['issues']}")

        # Save result
        out_file = SRC_DIR / f"resources/feebas_path_{shore[0]}_{shore[1]}.json"
        with open(out_file, "w") as f:
            json.dump(
                {
                    "shore": list(result["shore"]),
                    "entry": list(result["entry"]),
                    "entry_key": result["entry_key"],
                    "steps": result["steps"],
                    "path": result["path"],
                    "positions": [list(p) for p in result["positions"]],
                },
                f,
                indent=2,
            )
        print(f"  Saved       : {out_file}")
        # print(f"  WASD preview: {''.join(result['path'][:80])}…")
        visualize(grid, result["positions"])
        print()

        solutions.append(result)
        if stop_first:
            break

    print(f"Done. {len(solutions)} solution(s) found.")
    if not solutions:
        sys.exit(1)
