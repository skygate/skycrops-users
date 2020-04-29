import os
from typing import NewType, Tuple

Point = NewType("Point", Tuple[float, float])

HOST = "0.0.0.0"

USERNAME_KEY = "name"
PASSWORD_KEY = "password"
COORDS_KEY = "coords"
ROWS_KEY = "rows"
TREES_KEY = "trees"

DEFAULT_ROWS_DISTANCE = 4
DEFAULT_TREES_DISTANCE = 1

_BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(_BASE_DIR, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
