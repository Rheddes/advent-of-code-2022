def read_input(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]


def get_register_values(operations):
    register_values = [1]
    for op in operations:
        register_values.append(register_values[-1])
        if op.startswith('addx'):
            [_, delta] = op.split(' ')
            register_values.append(register_values[-1] + int(delta))
    return register_values


def part1(file_path):
    register_values = get_register_values(read_input(file_path))
    return sum([(i+1) * register_values[i] for i in range(19, 220, 40)])


def part2(file_path):
    register_values = get_register_values(read_input(file_path))
    cur_line = ''
    for idx, sprite_pos in enumerate(register_values):
        crt_index = idx % 40
        if crt_index == 0:
            print(cur_line)
            cur_line = ''
        cur_line += '#' if abs(crt_index - sprite_pos) <= 1 else '.'
    return 'done'


if __name__ == '__main__':
    print(part1('./data/cycles.txt'))
    print(part2('./data/cycles.txt'))
