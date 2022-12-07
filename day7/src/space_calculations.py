
def parse_command(command, cwd):
    if command == '$ cd /':
        cwd = ['/']
    elif command == '$ cd ..':
        cwd = cwd[:-1]
    elif command.startswith('$ cd '):
        cwd += [command.split(' ')[2]]
    return cwd


# tighten up code
def get_entry(recursive_dict, key_list):
    result = recursive_dict[key_list[0]]
    for key in key_list[1:]:
        result = result[key]
    return result


def parse_result(ls_result, cwd, tree):
    if ls_result.startswith('dir'):
        get_entry(tree, cwd)[ls_result.split(' ')[1]] = {}
    else:
        get_entry(tree, cwd)[ls_result.split(' ')[1]] = int(ls_result.split(' ')[0])
    return tree


def parse_file(file_path):
    cwd = ['/']
    tree = {'/': {}}
    with open(file_path, 'r') as file:
        for line in file.readlines():
            line = line.strip()
            if line.startswith('$'):
                cwd = parse_command(line, cwd)
            else:
                tree = parse_result(line, cwd, tree)

    dir_sizes = []
    calculate_dict_sizes(tree, dir_sizes)
    return dir_sizes


def calculate_dict_sizes(current_item, dir_sizes):
    if type(current_item) == int:
        return current_item
    dir_size = sum([calculate_dict_sizes(item, dir_sizes) for item in current_item.values()])
    dir_sizes += [dir_size]
    return dir_size


def part1(file_path):
    return sum([dir_size for dir_size in parse_file(file_path) if dir_size <= 100000])


def part2(file_path):
    dir_sizes = parse_file(file_path)
    space_needed = max(dir_sizes) + 30000000 - 70000000
    for dir_size in sorted(dir_sizes):
        if dir_size > space_needed:
            return dir_size


# 50822529
# 967369
if __name__ == '__main__':
    print(part1('../data/cmd.txt'))
    print(part2('../data/cmd.txt'))
