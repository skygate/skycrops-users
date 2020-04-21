from typing import NewType, Tuple


Point = NewType("Point", Tuple[float, float])

HOST = "0.0.0.0"

COORDS_KEY = "coords"
ROWS_KEY = "rows"
TREES_KEY = "trees"

DEFAULT_ROWS_DISTANCE = 4
DEFAULT_TREES_DISTANCE = 1
