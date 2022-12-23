import re
from enum import Enum
from typing import List

from core.coordinates import Point, unit_x


class Rot:
    def __init__(self, matrix):
        self.mat = matrix

    def __repr__(self):
        return f'{self.mat}'

    def __mul__(self, other):
        result = [[], []]
        for i, row in enumerate(self.mat):
            for column in list(zip(*other)):
                result[i].append(sum([l * r for l, r in zip(row, column)]))
        return Rot(result)

    def is_horizontal(self):
        return abs(self.mat[0][0]) == 1

    def get_rot_pass(self):
        if self.is_horizontal():
            return 0 if self.mat[0][0] == 1 else 2
        return 1 if self.mat[0][1] == -1 else 3


class Cell(Enum):
    VOID = 1
    EMPTY = 2
    WALL = 3


rotations = {
    'L': [[0, 1], [-1, 0]],
    'R': [[0, -1], [1, 0]],
}


class SparseMap:
    def __init__(self):
        self.board = {}
        self.player = None
        self.rotation = Rot([[1, 0], [0, 1]])
        self.rows = {}
        self.columns = {}

    def add_cell(self, location: Point, contents: Cell):
        if self.player is None:
            self.player = location
        self.board[location] = contents
        if location.y not in self.rows:
            self.rows[location.y] = (location.x, 0)
        if location.x not in self.columns:
            self.columns[location.x] = (location.y, 0)
        offset, length = self.rows[location.y]
        self.rows[location.y] = (offset, max(length, location.x-offset+1))
        offset, length = self.columns[location.x]
        self.columns[location.x] = (offset, max(length, location.y-offset+1))

    def get(self, location: Point):
        return self.board.get(location, Cell.VOID)

    def move(self, steps):
        points_ahead = [self.player + unit_x * self.rotation.mat * i for i in range(steps + 1)]
        if self.rotation.is_horizontal():
            (offset, length) = self.rows[self.player.y]
            wrapped_points = [Point((x - offset) % length + offset, y) for x, y in points_ahead]
        else:
            (offset, length) = self.columns[self.player.x]
            wrapped_points = [Point(x, (y - offset) % length + offset) for x, y in points_ahead]
        cells = [self.get(loc) for loc in wrapped_points]
        index_of_location = cells.index(Cell.WALL)-1 if Cell.WALL in cells else steps
        self.player = wrapped_points[index_of_location]

    def move_cube(self, steps):
        points_ahead = [self.player + unit_x * self.rotation.mat * i for i in range(steps + 1)]
        wrapped_points = [self.wrap_point(point) for point in points_ahead]
        cells = [self.get(loc) for loc in wrapped_points]
        index_of_location = cells.index(Cell.WALL)-1 if Cell.WALL in cells else steps
        self.player = wrapped_points[index_of_location]
        self.wrap_rotate(points_ahead[index_of_location])
        return wrapped_points

    def rotate(self, r_key):
        self.rotation = self.rotation * rotations[r_key]

    def wrap_point(self, p: Point) -> Point:
        if self.rotation.get_rot_pass() == 0 and 50 <= p.y < 100 and p.x >= 100: # 3 to 1
            return Point(p.y+50, 49-(p.x-100))  # ROT LEFT
        if self.rotation.get_rot_pass() == 1 and 50 <= p.y < 100 and p.x >= 100: # 1 to 3
            return Point(99-(p.y-50), p.x-50) # ROT RIGHT
        if self.rotation.get_rot_pass() == 0 and 100 <= p.y < 150 and p.x >= 100: # 4 to 1
            return Point(149-(p.x-100), 49-(p.y-100)) # ROT ROT
        if self.rotation.get_rot_pass() == 0 and p.x > 149 and p.y < 50: # 1 to 4
            return Point(99-(p.x-150), 149-p.y) # ROT ROT
        if self.rotation.get_rot_pass() == 0 and p.x > 49 and p.y > 149: # 6 to 4
            return Point(p.y-100, 149-(p.x-50)) # ROT LEFT
        if self.rotation.get_rot_pass() == 1 and 49 < p.x < 100 and p.y > 149: # 4 to 6
            return Point(49-(p.y-150), p.x+100) # ROT RIGHT
        if self.rotation.get_rot_pass() == 1 and 0 <= p.x < 50 and p.y > 199: # 6 to 1
            return Point(p.x+100, p.y-200) # NO ROT
        if self.rotation.get_rot_pass() == 3 and 99 < p.x < 150 and p.y < 0: # 1 to 6
            return Point(p.x-100, 200+p.y) # NO ROT
        if self.rotation.get_rot_pass() == 2 and p.x < 0 and 149 < p.y < 200: # 6 to 2
            return Point(p.y-100, -1-p.x) # ROT LEFT
        if self.rotation.get_rot_pass() == 3 and 49 < p.x < 100 and p.y < 0: # 2 to 6
            return Point(-1-p.y, p.x+100) # ROT RIGHT
        if self.rotation.get_rot_pass() == 2 and p.x < 0 and 99 < p.y < 150: # 5 to 2
            return Point(49-p.x, 149-p.y) # ROT ROT
        if self.rotation.get_rot_pass() == 2 and p.x < 50 and 0 <= p.y < 50: # 2 to 5
            return Point(49-p.x, 149-p.y) # ROT ROT
        if self.rotation.get_rot_pass() == 3 and 0 <= p.x < 50 and p.y < 100: # 5 to 3
            return Point(149-p.y, 50+p.x) # ROT RIGHT
        if self.rotation.get_rot_pass() == 2 and p.x < 50 and 49 < p.y < 100: # 3 to 5
            return Point(p.y-50, 149-p.x) # ROT LEFT
        return p

    def wrap_rotate(self, p: Point):
        if self.rotation.get_rot_pass() == 0 and 50 <= p.y < 100 and p.x >= 100: # 3 to 1
            self.rotate('L')
        if self.rotation.get_rot_pass() == 1 and 50 <= p.y < 100 and p.x >= 100: # 1 to 3
            self.rotate('R')
        if self.rotation.get_rot_pass() == 0 and 100 <= p.y < 150 and p.x >= 100: # 4 to 1
            self.rotate('R')
            self.rotate('R')
        if self.rotation.get_rot_pass() == 0 and p.x > 149 and p.y < 50: # 1 to 4
            self.rotate('R')
            self.rotate('R')
        if self.rotation.get_rot_pass() == 0 and p.x > 49 and p.y > 149: # 6 to 4
            self.rotate('L')
        if self.rotation.get_rot_pass() == 1 and 49 < p.x < 100 and p.y > 149: # 4 to 6
            self.rotate('R')
        if self.rotation.get_rot_pass() == 2 and p.x < 0 and 149 < p.y < 200: # 6 to 2
            self.rotate('L')
        if self.rotation.get_rot_pass() == 3 and 49 < p.x < 100 and p.y < 0: # 2 to 6
            self.rotate('R')
        if self.rotation.get_rot_pass() == 2 and p.x < 0 and 99 < p.y < 150: # 5 to 2
            self.rotate('R')
            self.rotate('R')
        if self.rotation.get_rot_pass() == 2 and p.x < 50 and 0 <= p.y < 50: # 2 to 5
            self.rotate('R')
            self.rotate('R')
        if self.rotation.get_rot_pass() == 3 and 0 <= p.x < 50 and p.y < 100: # 5 to 3
            self.rotate('R')
        if self.rotation.get_rot_pass() == 2 and p.x < 50 and 49 < p.y < 100: # 3 to 5
            self.rotate('L')


def read(file_path):
    with open(file_path, 'r') as file:
        grid, moves = file.read().split('\n\n')
        grid_map = SparseMap()
        for y, row in enumerate(grid.splitlines()):
            for x, cell in enumerate(row):
                if cell != ' ':
                    grid_map.add_cell(Point(x, y), Cell.EMPTY if cell == '.' else Cell.WALL)
        parsed_moves = [int(move) if move.isnumeric() else move for move in moves.replace('R', ' R ').replace('L', ' L ').split(' ')]
        return grid_map, parsed_moves


def part1(file_path):
    grid, moves = read(file_path)
    for move in moves:
        if type(move) == int:
            grid.move(move)
        else:
            grid.rotate(move)
    return (grid.player.y + 1) * 1000 + (grid.player.x + 1) * 4 + grid.rotation.get_rot_pass()


def part2(file_path):
    grid, moves = read(file_path)
    for move in moves:
        if type(move) == int:
            grid.move_cube(move)
        else:
            grid.rotate(move)
    return (grid.player.y + 1) * 1000 + (grid.player.x + 1) * 4 + grid.rotation.get_rot_pass()


if __name__ == '__main__':
    print(part1('./data/path.txt'))
    print(part2('./data/path.txt'))