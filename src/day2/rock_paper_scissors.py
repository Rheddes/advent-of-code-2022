map_opponent = {
    'A': 0,
    'B': 1,
    'C': 2,
}
map_me = {
    'X': 0,
    'Y': 1,
    'Z': 2,
}
map_outcome = {
    'X': 0,
    'Y': 3,
    'Z': 6,
}


def round_winner(a, b):
    if (a + 1) % 3 == b:
        return 6
    elif a == b:
        return 3
    else:
        return 0


def map_winning_strategy(opponent, outcome):
    if outcome == 6:
        return (opponent + 1) % 3
    elif outcome == 3:
        return opponent
    else:
        return (opponent - 1) % 3


def simulate_part1(file_path):
    with open(file_path, 'r') as file:
        return sum([round_winner(map_opponent[opponent], map_me[me]) + map_me[me] + 1 for [opponent, me] in (line.split() for line in file.readlines())])


def simulate_part2(file_path):
    with open(file_path, 'r') as file:
        return sum([map_outcome[outcome] + map_winning_strategy(map_opponent[opponent], map_outcome[outcome]) + 1 for [opponent, outcome] in (line.split() for line in file.readlines())])


if __name__ == '__main__':
    print(simulate_part1('./data/strategy.txt'))
    print(simulate_part2('./data/strategy.txt'))
