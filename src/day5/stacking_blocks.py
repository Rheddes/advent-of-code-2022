from string import ascii_uppercase


def stack_index(idx):
    return (idx - 1) // 4


def parse_stacks(stack_description):
    stacks = {}
    for line in stack_description:
        for idx, char in enumerate(line):
            if char in ascii_uppercase:
                stacks[stack_index(idx)] = stacks.get(stack_index(idx), []) + [char]
    return {k: stack[::-1] for k, stack in stacks.items()}


def parse_moves(move_lines):
    moves = []
    for line in move_lines:
        splitted = line.split(' ')
        moves += [{'take': int(splitted[1]), 'from': int(splitted[3])-1, 'to': int(splitted[5])-1}]
    return moves


def read_input(file_path):
    with open(file_path, 'r') as file:
        file_contents = file.read()
    stacks = parse_stacks([line for line in file_contents.split('\n') if '[' in line])
    moves = parse_moves([line for line in file_contents.split('\n') if 'move' in line])
    return stacks, moves


def part1(file_path):
    (stacks, moves) = read_input(file_path)
    for move in moves:
        take = stacks[move['from']][:-move['take']-1:-1]
        stacks[move['from']] = stacks[move['from']][:-move['take']]
        stacks[move['to']] = stacks[move['to']] + take
    result = ''
    for key in range(max(stacks.keys())+1):
        result += stacks[key][-1]
    return result


def part2(file_path):
    (stacks, moves) = read_input(file_path)
    for move in moves:
        take = stacks[move['from']][-move['take']:]
        stacks[move['from']] = stacks[move['from']][:-move['take']]
        stacks[move['to']] = stacks[move['to']] + take
    result = ''
    for key in range(max(stacks.keys())+1):
        result += stacks[key][-1]
    return result


if __name__ == '__main__':
    print(part1('./data/stonks.txt'))
    print(part2('./data/stonks.txt'))
