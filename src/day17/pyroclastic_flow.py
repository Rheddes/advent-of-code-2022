from collections import deque
from enum import Enum
from typing import List, Optional

from core.coordinates import Point, unit_x, unit_y

shapes = {
    'hline': [Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0)],
    'vline': [Point(0, 0), Point(0, 1), Point(0, 2), Point(0, 3)],
    'square': [Point(0, 0), Point(0, 1), Point(1, 0), Point(1, 1)],
    'right_l': [Point(0, 0), Point(1, 0), Point(2, 0), Point(2, 1), Point(2, 2)],
    'cross': [Point(0, 1), Point(1, 0), Point(1, 1), Point(1, 2), Point(2, 1)],
}
ordered_rocks = [shapes['hline'], shapes['cross'], shapes['right_l'], shapes['vline'], shapes['square']]


class Cell(Enum):
    EMPTY = 1
    ROCK = 2
    BOUNDS = 3


def get_moves(file_path):
    with open(file_path, 'r') as file:
        return [move for move in file.readline()]


def column_sum(heights):
    return [sum(col) for col in zip(*heights)]


class SparseRockMap:
    def __init__(self, debug=False, track_historic_heights=False):
        self.column_heights = [0] * 7
        self.rock_map = {}
        self.current_rock: Optional[(Point, List[Point])] = None
        self.rock_i = 0
        self.debug = debug
        self.add_rock()
        self.track_historic_heights = track_historic_heights
        self.historic_heights = [[0]*7]

    def simulate(self, n_rocks, move_pattern):
        i = 0
        while self.rock_i < n_rocks + 1:
            move = move_pattern[i % len(move_pattern)]
            i += 1
            self.move(move)
        return max(self.column_heights)

    def add_rock(self):
        shape = ordered_rocks[self.rock_i % len(ordered_rocks)]
        self.rock_i += 1
        if self.rock_i % 100_000 == 0:
            print(self.rock_i)
        self.current_rock = (Point(2, max(self.column_heights) + 4), shape)
        if self.debug:
            self.print_rock_map()

    def print_rock_map(self):
        for y in range(max(self.column_heights) + 4, 0, -1):
            row = ''.join(['#' if self.get(Point(x, y)) == Cell.ROCK else '.' for x in range(0, 7)])
            print(f'|{row}|')
        print('+-------+')

    def stop_and_add_new_rock(self, rock_origin, rock_shape):
        for rock_loc in [rock_origin + offset for offset in rock_shape]:
            self.rock_map[rock_loc] = Cell.ROCK
            self.column_heights[rock_loc.x] = max(self.column_heights[rock_loc.x], rock_loc.y)
        if self.track_historic_heights:
            self.historic_heights.append([x for x in self.column_heights])
        self.add_rock()

    def get(self, loc: Point):
        if loc.x < 0 or loc.x > 6 or loc.y <= 0:
            return Cell.BOUNDS
        return self.rock_map.get(loc, Cell.EMPTY)

    def collides(self, rock: List[Point]) -> bool:
        for rock_lock in rock:
            if self.get(rock_lock) != Cell.EMPTY:
                return True
        return False

    def move(self, move):
        assert self.current_rock
        (x, y), shape = self.current_rock
        if move == '<' and not self.collides([Point(x, y) + offset - unit_x for offset in shape]):
            x -= 1
        elif move == '>' and not self.collides([Point(x, y) + offset + unit_x for offset in shape]):
            x += 1
        if not self.collides([Point(x, y) + offset - unit_y for offset in shape]):
            y -= 1
            self.current_rock = (Point(x, y), shape)
        else:
            self.stop_and_add_new_rock(Point(x, y), shape)


def find_offset_and_period(height_diffs):
    for t1 in range(1, len(height_diffs)):
        for period_size in range(2, len(height_diffs) // 2):
            t2 = t1 + period_size
            t3 = t2 + period_size
            if len(height_diffs[t1:t2]) != len(height_diffs[t2:t3]):
                break
            if all(h1 == h2 for h1, h2 in zip(height_diffs[t1:t2], height_diffs[t2:t3])):
                return t1, period_size
    assert False


def part1(file_path):
    rocks = SparseRockMap()
    return rocks.simulate(2022, get_moves(file_path))


def part2(file_path, n_rocks=1000000000000):
    rocks = SparseRockMap(track_historic_heights=True)
    rocks.simulate(20000, get_moves(file_path))
    heights_top20 = rocks.historic_heights
    height_diff = [[a-b for b, a in zip(before, after)] for before, after in zip(heights_top20, heights_top20[1:])]
    start, period_size = find_offset_and_period(height_diff)
    print(start, period_size)
    periods = (n_rocks - start) // period_size
    end = (n_rocks-start) % period_size
    period_dh = column_sum(height_diff[start+1:start+period_size+1]) # Index magic
    total_repeating = [dh * periods for dh in period_dh]
    end = column_sum(height_diff[start+1:start+end])
    return max(column_sum([heights_top20[start]] + [total_repeating] + [end]))


if __name__ == '__main__':
    print(part1('./data/jets.txt'))
    print(part2('./data/jets.txt'))
