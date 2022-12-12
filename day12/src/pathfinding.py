import copy
import sys

movement_options = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def read_grid_as_dict(file_path):
    with open(file_path, 'r') as file:
        return {(x, y): char for y, line in enumerate(file.readlines()) for x, char in enumerate(line.strip())}


def edge(a, b, reverse):
    if reverse:
        return b, a
    return a, b


def construct_graph(file_path, reverse=False):
    grid = read_grid_as_dict(file_path)
    start = None
    end = None
    edges = set()
    for coord, char in grid.items():
        start = coord if char == 'S' else start
        end = coord if char == 'E' else end
        char_ord = ord('a') if char == 'S' else ord('z') if char == 'E' else ord(char)
        edges |= {edge(coord, move(coord, diff), reverse) for diff in movement_options if (ord(grid.get(move(coord, diff), '~')) - char_ord) < 2}
    return grid, edges, start, end


def move(coord, diff):
    return tuple(pos + step for pos, step in zip(coord, diff))


def dijkstra_algorithm(nodes, edges, start_node):
    unvisited_nodes = copy.deepcopy(nodes)
    shortest_paths = {node: sys.maxsize if node != start_node else 0 for node in unvisited_nodes}
    previous_nodes = {}
    while unvisited_nodes:
        shortest_paths_for_unvisited = {n: shortest_paths[n] for n in unvisited_nodes}
        current_min_node = min(shortest_paths_for_unvisited, key=shortest_paths_for_unvisited.get)
        for neighbor in [move(current_min_node, diff) for diff in movement_options]:
            if (current_min_node, neighbor) in edges and shortest_paths[current_min_node] + 1 < shortest_paths[neighbor]:
                shortest_paths[neighbor] = shortest_paths[current_min_node] + 1
                previous_nodes[neighbor] = current_min_node
        unvisited_nodes.remove(current_min_node)

    return previous_nodes, shortest_paths


def part1(file_path):
    (grid, edges, start, end) = construct_graph(file_path)
    _, paths = dijkstra_algorithm(set(grid.keys()), edges, start)
    return paths[end]


def part2(file_path):
    (grid, edges, end, start) = construct_graph(file_path, True)
    _, shortest_paths = dijkstra_algorithm(set(grid.keys()), edges, start)
    for coord, length in {k: v for k, v in sorted(shortest_paths.items(), key=lambda item: item[1])}.items():
        if grid[coord] == 'a':
            return length


if __name__ == '__main__':
    print(part1('../data/grid.txt'))
    print(part2('../data/grid.txt'))
