import math
import operator

operations = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}


class MonkeyMath:
    def __init__(self, is_part_one):
        self.is_part_one = is_part_one
        self.monkeys = {}

    def set(self, monkey, operation):
        if operation.isnumeric():
            self.monkeys[monkey] = int(operation) if monkey != 'humn' or self.is_part_one else 1j
        else:
            a, op, b = operation.split(' ')
            self.monkeys[monkey] = lambda: operations[op](self.get(a), self.get(b))

    def get(self, monkey):
        val = self.monkeys[monkey]
        if callable(val):
            val = val()
            self.monkeys[monkey] = val
        return val


def read(file_path, is_part_one):
    monkey_a, monkey_b = None, None
    with open(file_path, 'r') as file:
        monkeys = MonkeyMath(is_part_one)
        for line in file.readlines():
            monkey, operation = line.strip().split(': ')
            monkeys.set(monkey, operation)
            if monkey == 'root':
                monkey_a, _, monkey_b = operation.split(' ')
        return monkeys, monkey_a, monkey_b


def part1(file_path):
    equations, _, _ = read(file_path, is_part_one=True)
    return math.floor(equations.get('root'))


def part2(file_path):
    equations, monkey_a, monkey_b = read(file_path, is_part_one=False)
    compare = equations.get(monkey_b) - equations.get(monkey_a)
    return -1 * math.floor(compare.real / compare.imag)


if __name__ == '__main__':
    print(part1('./data/monkeys.txt'))
    print(part2('./data/monkeys.txt'))
