import re
from enum import Enum

from core.coordinates import Point, manhattan, add


def map_quadrants(q_p, q_n):
    if (q_p == 'q1' and q_n == 'q2') or (q_p == 'q2' and q_n == 'q1'):
        return Point(-1, 0)
    if (q_p == 'q1' and q_n == 'q4') or (q_p == 'q4' and q_n == 'q1'):
        return Point(0, -1)
    if (q_p == 'q2' and q_n == 'q3') or (q_p == 'q3' and q_n == 'q2'):
        return Point(0, 1)
    if (q_p == 'q4' and q_n == 'q3') or (q_p == 'q3' and q_n == 'q4'):
        return Point(1, 0)
    print('ERROR ILLEGAL INTERSECTION')


def read(file_path):
    pattern = r"Sensor at x=(?P<sensor_x>-?\d+), y=(?P<sensor_y>-?\d+): closest beacon is at x=(?P<beacon_x>-?\d+), y=(?P<beacon_y>-?\d+)"
    with open(file_path, 'r') as file:
        return \
            [(
                Point(int(matches.group('sensor_x')), int(matches.group('sensor_y'))),
                Point(int(matches.group('beacon_x')), int(matches.group('beacon_y')))
            ) for line in file.readlines() if (matches := re.match(pattern, line.strip()))]


def construct_diagonals(sensors_and_beacons):
    diagonals_pos, diagonals_neg = [], []
    for sensor, beacon in sensors_and_beacons:
        radius = manhattan(sensor, beacon)
        corner_bottom, corner_top = Point(sensor.x, sensor.y - radius), Point(sensor.x, sensor.y + radius)
        corner_left, corner_right = Point(sensor.x - radius, sensor.y), Point(sensor.x + radius, sensor.y)
        diagonals_pos += [(sensor, corner_bottom.y - corner_bottom.x, corner_bottom.x, corner_right.x), (sensor, corner_top.y - corner_top.x, corner_left.x, corner_top.x)]
        diagonals_neg += [(sensor, corner_bottom.y + corner_bottom.x, corner_left.x, corner_bottom.x), (sensor, corner_top.y + corner_top.x, corner_top.x, corner_right.x)]
    return diagonals_pos, diagonals_neg


def get_quadrant(sensor: Point, intersect: Point):
    if intersect.x < sensor.x and intersect.y < sensor.y:
        return 'q1'
    if intersect.x < sensor.x and intersect.y > sensor.y:
        return 'q2'
    if intersect.x > sensor.x and intersect.y > sensor.y:
        return 'q3'
    if intersect.x > sensor.x and intersect.y < sensor.y:
        return 'q4'
    return 'corner'


def get_inner_point(diagonal_pos, diagonal_neg, intersect: Point):
    sensor_p, sensor_n = diagonal_pos[0], diagonal_neg[0]
    diff = map_quadrants(get_quadrant(sensor_p, intersect), get_quadrant(sensor_n, intersect))
    return Point(*add(intersect, diff))




def find_x_range(sensors_and_beacons):
    min_x, max_x = 0, 0
    for sensor, beacon in sensors_and_beacons:
        min_x = min(min_x, sensor.x, beacon.x)
        max_x = max(max_x, sensor.x, beacon.x)
    return range(min_x, max_x+1)


def part1(file_path, row):
    sensors_and_beacons = read(file_path)
    sensors, beacons = list(zip(*sensors_and_beacons))

    no_beacon = set()
    for sensor, beacon in sensors_and_beacons:
        radius = manhattan(sensor, beacon)
        closest_to_row = Point(sensor.x, row)
        slice_length = radius - manhattan(sensor, closest_to_row)
        if slice_length < 0:
            continue
        no_beacon |= {Point(x, row) for x in range(closest_to_row.x-slice_length, closest_to_row.x+slice_length+1) if Point(x, row) not in beacons}
    return len(no_beacon)


def part2(file_path):
    diagonals_pos, diagonals_neg = construct_diagonals(read(file_path))
    intersections = {}
    for diagonal_pos in diagonals_pos:
        for diagonal_neg in diagonals_neg:
            if diagonal_pos[0] == diagonal_neg[0]:
                continue
            x_intersect = (diagonal_neg[1]-diagonal_pos[1])//2
            if max(diagonal_neg[2], diagonal_pos[2]) < x_intersect < min(diagonal_neg[3], diagonal_pos[3]):
                intersect = Point(x_intersect, diagonal_pos[1] + x_intersect)
                inner = get_inner_point(diagonal_pos, diagonal_neg, intersect)
                intersections[inner] = intersections.get(inner, 0) + 1
                if intersections[inner] == 4:
                    return inner.x * 4000000 + inner.y
    return 'NO POINT FOUND'




if __name__ == '__main__':
    # print(part1('./data/test.txt', 10))
    # print(part1('./data/beacons.txt', 2000000))
    print(part2('./data/beacons.txt'))
