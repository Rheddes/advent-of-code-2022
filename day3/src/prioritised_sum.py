from string import ascii_lowercase, ascii_uppercase
from operator import iand
from functools import reduce

def build_character_priority_map():
    lower_case = {char: index + 1 for index, char in enumerate(ascii_lowercase)}
    upper_case = {char: index + 27 for index, char in enumerate(ascii_uppercase)}
    return {' ': 0} | lower_case | upper_case


def build_character_bitwise_map():
    lower_case = {char: 1 << index for index, char in enumerate(ascii_lowercase)}
    upper_case = {char: 1 << (index + 26) for index, char in enumerate(ascii_uppercase)}
    return lower_case | upper_case


char_priority_map = build_character_priority_map()
char_map = build_character_bitwise_map()
inverse_map = {v: k for k, v in char_map.items()}


def split_string_in_equal_parts(string_to_split):
    half = len(string_to_split) // 2
    return string_to_split[0:half], string_to_split[half:]


def convert_string_to_bits(string_to_convert):
    return sum([char_map[c] for c in set(string_to_convert)])

def bin(s):
    return str(s) if s <= 1 else bin(s >> 1) + str(s & 1)


def part1(file_path):
    with open(file_path, 'r') as file:
        compartments = [split_string_in_equal_parts(items) for items in (line.strip() for line in file.readlines())]
        bit_vectors = [convert_string_to_bits(a) & convert_string_to_bits(b) for (a, b) in compartments]
        characters = [inverse_map.get(bit_vector, ' ') for bit_vector in bit_vectors]
        return sum([char_priority_map[char] for char in characters])




def part2(file_path, group_size=3):
    with open(file_path, 'r') as file:
        rucksacks = [convert_string_to_bits(rucksack) for rucksack in (line.strip() for line in file.readlines())]
        grouped_rucksacks = [rucksacks[i:i + group_size] for i in range(0, len(rucksacks), group_size)]
        badges = [inverse_map.get(reduce(iand, group), ' ') for group in grouped_rucksacks]
        return sum([char_priority_map[char] for char in badges])

if __name__ == '__main__':
    # print(part1('../data/rucksack.txt'))
    print(part2('../data/rucksack.txt'))
