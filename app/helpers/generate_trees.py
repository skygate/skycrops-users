from typing import List, Tuple

import matplotlib.pyplot as plt
import utm
from scipy.spatial import distance

from config import Point


class TreesGenerator:
    """
    Class that generates trees coordinates on orchard
    """

    def __init__(
        self,
        corner_coords: List[Point],
        distance_between_rows: float,
        distance_between_trees: float,
    ) -> None:
        self.corner_coords = self._coords_to_utm(corner_coords)
        self.distance_between_rows = distance_between_rows
        self.distance_between_trees = distance_between_trees

    def _coords_to_utm(self, coords: List[Point]) -> List[Point]:
        """
        Converts coordinates to UTM format
        """
        return [
            (utm.from_latlon(lat, lon)[0], utm.from_latlon(lat, lon)[1])
            for lat, lon in coords
        ]

    def get_shorter_rectangle_sides(self) -> Tuple[Tuple[Point, Point]]:
        first_shorter_side = (
            self.corner_coords[0],
            self._find_closest_point(self.corner_coords[0], self.corner_coords),
        )
        other_points = [
            point for point in self.corner_coords if point not in first_shorter_side
        ]
        closer_point = self._find_closest_point(self.corner_coords[0], other_points)
        further_point = [point for point in other_points if point != closer_point][0]
        second_shorter_side = closer_point, further_point
        return first_shorter_side, second_shorter_side

    def _find_closest_point(self, start_point: Point, points: List[Point]) -> Point:
        """
        Finds the nearest point to the given one
        """
        min_dist = 99999
        coordinates = [point for point in points if point != start_point]
        for point in coordinates:
            dist = distance.euclidean(start_point, point)
            if dist < min_dist:
                min_dist = dist
                closest_point = point
        return closest_point

    def _get_slope(self, start_point: Point, end_point: Point) -> float:
        """
        Gets the slope A of the line passing through two points written by the formula y = Ax + B
        """
        return (end_point[1] - start_point[1]) / (end_point[0] - start_point[0])

    def plot_coordinates(self) -> None:
        """
        Plots coordinates
        """
        x, y = zip(*self.corner_coords)
        plt.scatter(x, y, color="red")
        plt.show()
