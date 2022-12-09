def read_file(file_path):
    with (open(file_path, 'r')) as file:
        return [line.strip().split() for line in file.readlines()]


def take_step_in(direction, cur_pos):
    (vertical, horizontal) = cur_pos
    if direction == 'U':
        return vertical + 1, horizontal
    if direction == 'D':
        return vertical - 1, horizontal
    if direction == 'R':
        return vertical, horizontal + 1
    if direction == 'L':
        return vertical, horizontal - 1


def normalize(v):
    if abs(v) > 1:
        return v / abs(v)
    return v


def follow(head, tail):
    diff = tuple(h - t for h, t in zip(head, tail))
    if 2 in diff or -2 in diff:
        return tuple(pos + normalize(step) for pos, step in zip(tail, diff))
    return tail


def move_rope(rope, direction):
    new_rope = [take_step_in(direction, rope[0])]
    for i in range(1, len(rope)):
        new_rope += [follow(new_rope[i - 1], rope[i])]
    return new_rope


def take_step(direction, old_pos_head, old_pos_tail):
    new_pos_head = take_step_in(direction, old_pos_head)
    return new_pos_head, follow(new_pos_head, old_pos_tail)


def part1(file_path):
    visited = set()
    rope = [(0, 0)] * 2
    for (direction, steps) in read_file(file_path):
        for step in range(int(steps)):
            rope = move_rope(rope, direction)
            visited.add(rope[-1])
    return len(visited)


def part2(file_path, rope_length: int):
    visited = set()
    rope = [(0, 0)] * rope_length
    for (direction, steps) in read_file(file_path):
        for step in range(int(steps)):
            rope = move_rope(rope, direction)
            visited.add(rope[-1])
    return len(visited)


if __name__ == '__main__':
    print(part1('../data/moves.txt'))
    print(part2('../data/moves.txt', 10))
