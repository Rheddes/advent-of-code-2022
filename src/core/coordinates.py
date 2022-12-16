from collections import namedtuple
Point = namedtuple('Point', 'x y')


def point_from_string(coord: str):
    [x, y] = coord.strip().split(',')
    return Point(int(x), int(y))


def diff(a: Point, b: Point):
    return tuple(a_ax - b_ax for a_ax, b_ax in zip(a, b))


def add(a: Point, b: Point):
    return tuple(a_ax + b_ax for a_ax, b_ax in zip(a, b))


def manhattan(a: Point, b: Point):
    return sum([abs(d) for d in diff(a, b)])


def move_straight(start: Point, end: Point, include_end=False):
    (x_diff, y_diff) = diff(end, start)
    end_inclusion_delta = 1 if include_end else 0
    if x_diff == 0:
        if y_diff > 0:
            for y in range(y_diff + end_inclusion_delta):
                yield Point(start.x, start.y + y)
        if y_diff < 0:
            for y in range(0, y_diff - end_inclusion_delta, -1):
                yield Point(start.x, start.y + y)
    if y_diff == 0:
        if x_diff > 0:
            for x in range(x_diff + end_inclusion_delta):
                yield Point(start.x + x, start.y)
        if x_diff < 0:
            for x in range(0, x_diff - end_inclusion_delta, -1):
                yield Point(start.x + x, start.y)
