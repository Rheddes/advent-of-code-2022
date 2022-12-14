from ast import literal_eval
from functools import cmp_to_key


def read(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def compare_ints(left, right):
    if left == right:
        return None
    return left < right


def compare(left, right):
    if type(left) == int and type(right) == int:
        return compare_ints(left, right)
    if type(left) == int:
        left = [left]
    if type(right) == int:
        right = [right]
    if not left and not right:
        return None
    if not left:
        return True
    if not right:
        return False
    head_l, tail_l = left[0], left[1:]
    head_r, tail_r = right[0], right[1:]
    comp_head = compare(head_l, head_r)
    return comp_head if comp_head is not None else compare(tail_l, tail_r)


def cmp(left, right):
    compared = compare(left, right)
    if compared is None:
        return 0
    return -1 if compared else 1


def part1(file_path):
    right_order = []
    left, right = None, None
    for idx, line in enumerate(read(file_path).split('\n')):
        if idx % 3 == 0:
            left = literal_eval(line)
        elif idx % 3 == 1:
            right = literal_eval(line)
        elif idx % 3 == 2:
            if compare(left, right):
                right_order += [1 + idx // 3]
            left, right = None, None
    return sum(right_order)


def part2(file_path):
    lists = [[[2]], [[6]]] + [literal_eval(line) for line in read(file_path).split('\n') if line]
    sorted_packets = sorted(lists, key=cmp_to_key(cmp))
    return (sorted_packets.index(lists[0])+1) * (sorted_packets.index(lists[1])+1)


if __name__ == '__main__':
    print(part1('./data/lists.txt'))
    print(part2('./data/lists.txt'))
