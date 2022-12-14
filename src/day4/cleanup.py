from functools import reduce
from operator import iand, ior


def read_file(file_path):
    with (open(file_path, 'r')) as file:
        return [line.strip() for line in file.readlines()]


def sectors_as_bits(assignment_string):
    bounds = [int(x) for x in assignment_string.split('-')]
    return reduce(ior, [1 << sector for sector in range(bounds[0], bounds[1] + 1)])


def read_assignments_as_bits(file_path):
    return [(sectors_as_bits(elf_a), sectors_as_bits(elf_b)) for elf_a, elf_b in (line.split(',') for line in read_file(file_path))]


def part1(file_path):
    return sum([1 if (a & b == a) or (a & b == b) else 0 for a, b in read_assignments_as_bits(file_path)])


def part2(file_path):
    return sum([1 if a & b else 0 for a, b in read_assignments_as_bits(file_path)])


if __name__ == '__main__':
    # print(part1('./data/assignments.txt'))
    print(part2('./data/assignments.txt'))