import sys

directions = [
    (0, 0, 1),
    (0, 0, -1),
    (0, 1, 0),
    (0, -1, 0),
    (1, 0, 0),
    (-1, 0, 0),
]

def add(a, b):
    return tuple(a_ax + b_ax for a_ax, b_ax in zip(a, b))


def read(file_path):
    with open(file_path, 'r') as file:
        return {(int(x), int(y), int(z)) for x, y, z in (line.strip().split(',') for line in file.readlines())}


def hashmap(cube_list):
    candidates = {}
    for cube in cube_list:
        candidates[sum(cube)] = candidates.get(sum(cube), []) + [cube]
    return candidates


def adjacent(a, b):
    a_x, a_y, a_z = a
    b_x, b_y, b_z = b
    if a_x == b_x and a_y == b_y and abs(a_z - b_z) == 1:
        return True
    if a_x == b_x and a_z == b_z and abs(a_y - b_y) == 1:
        return True
    if a_z == b_z and a_y == b_y and abs(a_x - b_x) == 1:
        return True
    return False


def count_adjacent(cubes):
    adjacent_sides = 0
    potential_candidates = hashmap(cubes)
    for hash_key in sorted(potential_candidates.keys()):
        for cube_a in potential_candidates[hash_key]:
            for cube_b in potential_candidates.get(hash_key + 1, []):
                if adjacent(cube_a, cube_b):
                    adjacent_sides += 2
    return adjacent_sides


def bfs(cubes, aircubes, visited, bounds):
    if not aircubes:
        return 0
    current = aircubes.pop()
    visited |= {current}
    neighbours = [(x,y,z) for (x,y,z) in [add(current, unit) for unit in directions] if bounds[0] <= x < bounds[1] and bounds[0] <= y < bounds[1] and bounds[0] <= z <= bounds[1]]
    cube_sides = sum([1 if neighbour in cubes else 0 for neighbour in neighbours])
    return cube_sides + bfs(cubes, aircubes + [neighbour for neighbour in neighbours if neighbour not in cubes and neighbour not in visited and neighbour not in aircubes], visited, bounds)


def part1(file_path):
    cubes = read(file_path)
    exposed_sides = len(cubes) * 6 - count_adjacent(cubes)
    return exposed_sides


def part2(file_path):
    cubes = read(file_path)
    bounds = (min(min(ax) - 3 for ax in zip(*cubes)), max(max(ax) + 3 for ax in zip(*cubes)))
    print(bounds)
    exposed_sides = bfs(cubes, [(0, 0, 0)], set(), bounds)
    return exposed_sides


if __name__ == '__main__':
    print(part1('./data/cubes.txt'))
    sys.setrecursionlimit(100000)
    print(part2('./data/cubes.txt'))
