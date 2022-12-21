import functools
import math
import re
import sys
from collections import namedtuple

from core.vector import Vector


class Costs(namedtuple('costs', 'ore clay obsidian')):
    def __ge__(self, other):
        return all(self_resource >= other_resource for self_resource, other_resource in zip(self, other))


def read_blueprints(file_path):
    pattern = r'Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.'
    with open(file_path, 'r') as file:
        return {
            int(blueprint): {
                'ore_robot': Costs(int(ore_robot_ore), 0, 0),
                'clay_robot': Costs(int(clay_robot_ore), 0, 0),
                'obsidian_robot': Costs(int(obsidian_robot_ore), int(obsidian_robot_clay), 0),
                'geode_robot': Costs(int(geode_ore), 0, int(geode_obsidian)),
            } for
            blueprint, ore_robot_ore, clay_robot_ore, obsidian_robot_ore, obsidian_robot_clay, geode_ore, geode_obsidian
            in
            [re.match(pattern, line.strip()).groups() for line in file.readlines()]
        }


class Simulator:
    def __init__(self, blueprint):
        self.blueprint = blueprint
        self.current_max = 0
        self.cache = {}

    def robot_vector(self, next_robot):
        robot_indices = {'ore_robot': 1, 'clay_robot': 2, 'obsidian_robot': 3, 'geode_robot': 4}
        base = [0] * 9
        base[robot_indices[next_robot]] = 1
        base[5:8] = [-cost for cost in self.blueprint[next_robot]]
        return Vector(base)

    def get_resource_amount_and_rate(self, factory_state: Vector, robot):
        for i, _ in enumerate(['ore', 'clay', 'obsidian']):
            yield self.blueprint[robot][i], factory_state[i + 5], factory_state[i + 1]

    def calculate_delta_vector(self, factory_state: Vector, next_robot: str) -> Vector:
        if next_robot is None:
            return Vector([0] * 9)
        robot = self.blueprint[next_robot]
        steps = max(1, math.ceil(max(
            (robot_resource_cost - current_resource_amount) / rate if rate else robot_resource_cost * 10000
            for robot_resource_cost, current_resource_amount, rate in self.get_resource_amount_and_rate(factory_state, next_robot)
        )) + 1)
        steps_left, ore_rate, clay_rate, obsidian_rate, geode_rate = factory_state[:5]
        if steps_left < steps:
            return Vector([-steps_left, 0, 0, 0, 0, steps_left * ore_rate, steps_left * clay_rate, steps_left * obsidian_rate, steps_left * geode_rate])
        return Vector([-steps, 0, 0, 0, 0, steps*ore_rate, steps*clay_rate, steps*obsidian_rate, steps*geode_rate]) + self.robot_vector(next_robot)

    def determine_feasible_robots(self, factory_state: Vector):
        steps_left, ore_bots, clay_bots, obsidian_bots, geode_bots, ores, clays, obsidian, _ = factory_state
        max_ore, max_clay, max_obsidian = [max(costs) for costs in zip(*self.blueprint.values())]
        feasible_robots = []
        if ore_bots > 0 and obsidian_bots > 0:
            feasible_robots.append('geode_robot')
        if obsidian_bots < max_obsidian and clay_bots > 0 and ore_bots > 0 and obsidian <= (
                steps_left - 1) * max_obsidian:
            feasible_robots.append('obsidian_robot')
        if ore_bots < max_ore and ores <= (steps_left - 1) * max_ore:
            feasible_robots.append('ore_robot')
        if clay_bots < max_clay and ore_bots > 0 and clays <= (steps_left - 1) * max_clay:
            feasible_robots.append('clay_robot')
        return feasible_robots

    # [ 0 ,    1    ,    2     ,   3     ,    4    ,  5 ,  6  ,  7 ,  8 ]
    # [min, ore_bots, clay_bots, obs_bots, geo_bots, ore, clay, obs, geo]
    def recursive_search(self, factory_state: Vector, robots):
        if robots[-1] and factory_state.__str__() + robots[-1] in self.cache:
            return self.cache[factory_state.__str__() + robots[-1]]
        updated_state = factory_state + self.calculate_delta_vector(factory_state, robots[-1])
        if updated_state[-1] + updated_state[0] * (updated_state[4] + updated_state[0]) < self.current_max:
            return 0
        if updated_state[0] == 0:
            # print(updated_state)
            return updated_state[-1]
        geodes = max(self.recursive_search(updated_state, robots + [robot]) for robot in self.determine_feasible_robots(updated_state))
        if updated_state[0] < 5:
            self.cache[factory_state.__str__() + robots[-1]] = geodes
        self.current_max = max(self.current_max, geodes)
        return  geodes


# Assume every robot costs at least 2 ores
def part1(file_path):
    quality = 0
    for id, blueprint in read_blueprints(file_path).items():
        start_state = Vector([24, 1, 0, 0, 0, 0, 0, 0, 0])
        geodes = Simulator(blueprint).recursive_search(start_state, [None])
        quality += id * geodes
    return quality


def part2(file_path):
    geodes = 1
    for id, blueprint in read_blueprints(file_path).items():
        if id > 3:
            break
        start_state = Vector([32, 1, 0, 0, 0, 0, 0, 0, 0])
        geodes *= Simulator(blueprint).recursive_search(start_state, [None])
    return geodes


if __name__ == '__main__':
    sys.setrecursionlimit(100)
    print(part1('./data/blueprints.txt'))
    print(part2('./data/blueprints.txt'))
