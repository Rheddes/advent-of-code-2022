
def get_signal_from_file(file_path):
    with open(file_path, 'r') as file:
        return [char for char in file.read()]


def get_index_after_first_n_unique(signal, n):
    for i in range(len(signal)-n):
        if len(set(signal[i:i + n])) == n:
            return i + n


def part1(file_path):
    signal = get_signal_from_file(file_path)
    return get_index_after_first_n_unique(signal, 4)


def part2(file_path):
    signal = get_signal_from_file(file_path)
    return get_index_after_first_n_unique(signal, 14)


if __name__ == '__main__':
    print(part1('./data/signal.txt'))
    print(part2('./data/signal.txt'))
