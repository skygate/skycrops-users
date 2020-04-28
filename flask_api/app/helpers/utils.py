import csv
import io
from typing import List

from config import Point


def read_coordinates(file: io.StringIO) -> List[Point]:
    """
    Reads coordinates from CSV file and converts them to list
    """
    reader = csv.reader(file)
    next(reader)
    return [(float(lat), float(lon)) for lat, lon in reader]
