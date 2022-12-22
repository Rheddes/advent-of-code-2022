class Number:
    def __init__(self, value):
        self.value = value

    def decrypted(self, key):
        return self.value * key

    def __repr__(self):
        return f'{self.value}'


def read(file_path):
    with open(file_path, 'r') as file:
        return [Number(int(line.strip())) for line in file.readlines()]


def perform_move(move, coords, key=1):
    old_i = coords.index(move)
    move_v = move.decrypted(key)
    temp = coords[old_i+1:] + coords[0:old_i]
    new_i = move_v % len(temp)
    return temp[0:new_i] + [move] + temp[new_i:]


def part1(file_path):
    moves = read(file_path)
    coordinates = moves[:]
    for move in moves:
        coordinates = perform_move(move, coordinates)
    start = [i for i, coord in enumerate(coordinates) if coord.value == 0][0]
    return sum(coordinates[(start + offset) % len(coordinates)].value for offset in (1000, 2000, 3000))


def part2(file_path):
    moves = read(file_path)
    key = 811589153
    mixes = 10
    coordinates = moves[:]
    for _ in range(mixes):
        for move in moves:
            coordinates = perform_move(move, coordinates, key)
    start = [i for i, coord in enumerate(coordinates) if coord.value == 0][0]
    return sum(coordinates[(start + offset) % len(coordinates)].decrypted(key) for offset in (1000, 2000, 3000))


if __name__ == '__main__':
    print(part1('./data/encryption.txt'))
    print(part2('./data/encryption.txt'))
