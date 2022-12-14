from functools import reduce


def grouped_sum(accumulator, food_item):
    (current_elf, foods) = accumulator
    if food_item is None:
        return current_elf + 1, foods + [0]
    foods[current_elf] += food_item
    return current_elf, foods


def get_elves_with_most_food(file_path, n=1):
    with open(file_path, 'r') as file:
        parsed = [int(food_item) if food_item else None for food_item in (line.strip() for line in file.readlines())]
        (_, carrying_foods) = reduce(grouped_sum, parsed, (0, [0]))
        return sum(sorted(carrying_foods)[-n:])


if __name__ == '__main__':
    print('part 1: ', get_elves_with_most_food('./../data/calories.txt', 1))
    print('part 2: ', get_elves_with_most_food('./../data/calories.txt', 3))