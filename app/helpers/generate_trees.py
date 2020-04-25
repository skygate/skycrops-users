import math
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
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

    def get_trees_coords(self) -> List[Point]:
        """
        Iterates through every alley to get tree coordinates
        """
        trees_coords = []
        alleys_startpoints, alleys_endpoints = self._get_alleys_endpoints()
        for idx, startpoint in enumerate(alleys_startpoints):
            endpoint = alleys_endpoints[idx]
            angle = math.atan(self._get_slope(startpoint, endpoint))
            trees = self._generate_points(
                startpoint, endpoint, angle, self.distance_between_trees
            )
            trees_coords.extend(trees)
        return trees_coords

    def _get_alleys_endpoints(self) -> Tuple[List[Point], List[Point]]:
        """
        Gets starting points and endpoints of every alley
        """
        first_side, second_side = self._get_shorter_rectangle_sides()
        first_start_point = first_side[0]
        first_end_point = first_side[1]
        second_start_point = second_side[0]
        second_end_point = second_side[1]

        first_side_angle = math.atan(
            self._get_slope(first_start_point, first_end_point)
        )
        second_side_angle = math.atan(
            self._get_slope(second_start_point, second_end_point)
        )

        alleys_startpoints = self._generate_points(
            first_start_point,
            first_end_point,
            first_side_angle,
            self.distance_between_rows,
        )
        alleys_endpoints = self._generate_points(
            second_start_point,
            second_end_point,
            second_side_angle,
            self.distance_between_rows,
        )

        return alleys_startpoints, alleys_endpoints

    def _get_shorter_rectangle_sides(
        self
    ) -> Tuple[Tuple[Point, Point], Tuple[Point, Point]]:
        """
        Find shorter rectangle sides in order to chose direction of orchard alleys (according to the assumption that alleys are parallel to longer side"
        """
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

    def _generate_points(
        self,
        start_point: Point,
        end_point: Point,
        angle: float,
        distance_between_points: float,
    ) -> List[Point]:
        """
        Generates points with the given distance on a straight line described by the given angle
        :param start_point: First point, next one is generated with distance to the previous one
        :param end_point: If point has to be generated behind this, the function stops
        :param angle: An angle of the straight line, on which points are generated
        :param distance_between_points: Distance between the previous one and next one points
        :return:
        """
        points = [start_point]
        actual_point = start_point
        while distance.euclidean(actual_point, end_point) >= distance_between_points:
            actual_point = (
                actual_point[0] + distance_between_points * np.cos(angle),
                actual_point[1] + distance_between_points * np.sin(angle),
            )
            points.append(actual_point)
        return points

    def plot_coordinates(self) -> None:
        """
        Plots coordinates
        """
        coords = self.get_trees_coords()
        x, y = zip(*coords)
        plt.scatter(x, y, color="red")
        plt.show()
