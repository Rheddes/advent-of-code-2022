from common.coordinates import gimme_something


def read_coordinates(file_path):
    with open(file_path, 'r') as file:
        return [
            [tuple(int(pos) for pos in coord.strip().split(',')) for coord in line.strip().split('->')]
            for line in file.readlines()
        ]


def part1(file_path):
    rock_formations = read_coordinates(file_path)
    # Build 2d cavern
    # add send_source (500, 0) top!
    # simulate all the things
    # Return number of stationary sand packets
    print(gimme_something())
    return rock_formations


if __name__ == '__main__':
    print(part1('./data/testcavern.txt'))
