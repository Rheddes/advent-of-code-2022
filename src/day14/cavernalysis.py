from enum import Enum
from typing import List
from core.coordinates import Point, point_from_string, move_straight


class Cell(Enum):
    EMPTY = 1
    ROCK = 2
    SAND = 3


class SparseRockMap:
    def __init__(self):
        self.rock_map = {}
        self.abyss_depth = 0
        self.is_floor = False

    def add_rock(self, location: Point):
        self.rock_map[location] = Cell.ROCK
        self.abyss_depth = max(self.abyss_depth, location.y)

    def set_sand(self, location: Point):
        self.rock_map[location] = Cell.SAND

    def get(self, location: Point):
        if self.is_floor and location.y >= self.abyss_depth + 2:
            return Cell.ROCK
        return self.rock_map.get(location, Cell.EMPTY)

    def move_sand(self, current_location: Point):
        x, y = current_location
        if not self.is_floor and y > self.abyss_depth:
            return 'reached_abyss'
        if self.get(Point(x, y + 1)) == Cell.EMPTY:
            return Point(x, y + 1)
        if self.get(Point(x - 1, y + 1)) == Cell.EMPTY:
            return Point(x - 1, y + 1)
        if self.get(Point(x + 1, y + 1)) == Cell.EMPTY:
            return Point(x + 1, y + 1)
        return False


def read_coordinates(file_path):
    with open(file_path, 'r') as file:
        return [[point_from_string(coord) for coord in line.strip().split('->')] for line in file.readlines()]


def construct_map(rock_formations: List[List[Point]]) -> SparseRockMap:
    rock_map = SparseRockMap()
    for formation in rock_formations:
        for start, end in zip(formation, formation[1:]):
            for point in move_straight(start, end, True):
                rock_map.add_rock(point)
    return rock_map


def simulate_sand_unit(rock_map: SparseRockMap, sand_location: Point):
    new_sand_location = rock_map.move_sand(sand_location)
    if new_sand_location == 'reached_abyss':
        return True
    if new_sand_location:
        return simulate_sand_unit(rock_map, new_sand_location)
    if rock_map.get(sand_location) == Cell.SAND:
        return True
    rock_map.set_sand(sand_location)
    return False


def simulate_sand(rock_map: SparseRockMap, sand_source: Point):
    total_sand = 0
    while True:
        stationary = simulate_sand_unit(rock_map, sand_source)
        if stationary:
            return total_sand
        total_sand += 1


def part1(file_path):
    rock_formations = read_coordinates(file_path)
    rock_map = construct_map(rock_formations)
    sand_source = Point(500, 0)
    fallen_sand = simulate_sand(rock_map, sand_source)
    return fallen_sand


def part2(file_path):
    rock_formations = read_coordinates(file_path)
    rock_map = construct_map(rock_formations)
    rock_map.is_floor = True
    sand_source = Point(500, 0)
    fallen_sand = simulate_sand(rock_map, sand_source)
    return fallen_sand


if __name__ == '__main__':
    print(part1('./data/cavern.txt'))
    print(part2('./data/cavern.txt'))
