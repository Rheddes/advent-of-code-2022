import re
from collections import namedtuple
from itertools import combinations

Valve = namedtuple('Valve', ('name', 'rate', 'destinations'))


def read(file_path):
    pattern = r'Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? (.*)'
    with open(file_path, 'r') as file:
        return {
            valve: Valve(valve, int(flow), tuple(tunnels.split(', '))) for valve, flow, tunnels in
            [re.match(pattern, line.strip()).groups() for line in file.readlines()]
        }


def path_id(a, b):
    return tuple(sorted([a, b]))


def bfs_shortest_path(all_valves, valve: Valve):
    shortest_paths = {}
    visited = {valve.name}
    queue = [(valve, 1)]
    while queue:
        current, distance = queue.pop(0)
        for neighbour in current.destinations:
            if neighbour not in visited:
                visited |= {neighbour}
                shortest_paths[path_id(valve.name, neighbour)] = distance
                queue.append((all_valves[neighbour], distance + 1))
    return shortest_paths


def construct_shortest_paths(valves, all_valves):
    shortest_paths = {}
    for valve in valves:
        shortest_paths |= {path: length for path, length in bfs_shortest_path(all_valves, valve).items() if length < shortest_paths.get(path, 100000)}
    return shortest_paths


class FlowFinder:
    def __init__(self, shortest_paths, max_steps):
        self.shortest_paths = shortest_paths
        self.paths = []
        self.max_steps = max_steps

    def explore(self, node: Valve, unvisited, path, steps=0, rate=0, flow=0):
        if len(unvisited) == 0:
            flow += (self.max_steps - steps) * rate
            self.paths.append((path, flow))
            return flow
        for v in unvisited:
            new_steps = self.shortest_paths.get(path_id(node.name, v.name), -1) + 1
            if not new_steps or steps + new_steps > self.max_steps:
                new_flow = (self.max_steps - steps) * rate
                self.paths.append((path, flow + new_flow))
                continue
            new_flow = rate * new_steps
            self.explore(v, unvisited - {v}, path + [v.name], steps=steps + new_steps, rate=rate + v.rate, flow=flow + new_flow)

    def best(self):
        max_flow = (None, 0)
        for valve, flow in self.paths:
            if flow > max_flow[1]:
                max_flow = (valve, flow)
        return max_flow


def part1(file_path):
    valves = read(file_path)
    start_valve = [valve for valve in valves.values() if valve.name == 'AA'][0]
    valves_of_interest = {v for v in valves.values() if v.rate != 0}
    shortest_paths = construct_shortest_paths(valves_of_interest, valves)
    flow_finder = FlowFinder(shortest_paths, 30)
    flow_finder.explore(start_valve, valves_of_interest, [])
    return flow_finder.best()


def part2(file_path):
    valves = read(file_path)
    start_valve = [valve for valve in valves.values() if valve.name == 'AA'][0]
    valves_of_interest = {v for v in valves.values() if v.rate != 0}
    shortest_paths = construct_shortest_paths(valves_of_interest, valves)

    max_flow = (None, None, 0)
    for i in range(len(valves)):
        for valve_partition in combinations(valves_of_interest, i):
            my_valves = set(valve_partition)
            elephant_valves = valves_of_interest - my_valves

            flow_finder = FlowFinder(shortest_paths, 26)
            flow_finder.explore(start_valve, my_valves, [])
            my_best = flow_finder.best()

            flow_finder = FlowFinder(shortest_paths, 26)
            flow_finder.explore(start_valve, elephant_valves, [])
            elephant_best = flow_finder.best()

            if my_best[1] + elephant_best[1] > max_flow[2]:
                max_flow = (my_best, elephant_best, my_best[1] + elephant_best[1])
    return max_flow


if __name__ == '__main__':
    print(part1('./data/valves.txt'))
    print(part2('./data/valves.txt'))

