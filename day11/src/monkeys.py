import operator
from collections import deque
from functools import reduce
from typing import Callable

def parse_worry_operation(operation: str, after_inspection_mod=3):
    modifier = operation.split(' ')[-1]
    if '*' in operation and modifier == 'old':
        return lambda x: x * x // after_inspection_mod
    elif '*' in operation:
        return lambda x: x * int(modifier) // after_inspection_mod
    elif '+' in operation and modifier == 'old':
        return lambda x: (x + x) // after_inspection_mod
    return lambda x: (x + int(modifier)) // after_inspection_mod


class Monkey:
    def __init__(self, starting_items: list, operation: Callable, modulo: int, to_a, to_b):
        self.items = deque(starting_items)
        self.worry_op = operation
        self.modulo = modulo
        self.to_a = to_a
        self.to_b = to_b
        self.inspected_items = 0

    def throw(self):
        self.inspected_items += 1
        current_item = self.worry_op(self.items.popleft())
        return current_item, (self.to_a if current_item % self.modulo == 0 else self.to_b)

    def receive(self, item):
        self.items.append(item)


def parse_monkeys(file_path, worries_decrease):
    monkeys = []
    lcm = 1
    with open(file_path, 'r') as file:
        for line in file.read().split('\n'):
            line = line.strip()
            if line.startswith('Starting items:'):
                items = [int(item) for item in line.split(':')[1].strip().split(', ')]
            if line.startswith('Operation:'):
                operation = parse_worry_operation(line.split(':')[1].strip(), 3 if worries_decrease else 1)
            if line.startswith('Test:'):
                modulo = int(line.split(' ')[-1])
                lcm *= modulo
            if line.startswith('If true:'):
                to_a = int(line.split(' ')[-1])
            if line.startswith('If false:'):
                to_b = int(line.split(' ')[-1])
            if line == '':
                monkeys += [Monkey(items, operation, modulo, to_a, to_b)]
    return monkeys, lcm


def shenanigans(file_path, turns: int, worries_decrease: bool):
    monkeys, lcm = parse_monkeys(file_path, worries_decrease)
    for i in range(turns):
        for monkey in monkeys:
            while monkey.items:
                item, to_monkey = monkey.throw()
                monkeys[to_monkey].receive(item % lcm)
    return reduce(operator.mul, sorted([monkey.inspected_items for monkey in monkeys])[-2:])


if __name__ == '__main__':
    print(shenanigans('../data/monkeys.txt', 20, True))
    print(shenanigans('../data/monkeys.txt', 10000, False))
