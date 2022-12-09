def read_canopy_from_file(file_path):
    with open(file_path, 'r') as file:
        return [[int(char) for char in line.strip()] for line in file.readlines()]


def highest_trees(current_trees, current_highest_trees):
    return tuple(max(x, y) for x, y in zip(current_trees, current_highest_trees))


class CanopyCounter:
    def __init__(self, canopy):
        self.canopy = canopy
        self.visibility_grid = [[False for _ in row] for row in canopy]
        self.visible = 0

    def set_visible(self, x, y):
        if self.visibility_grid[x][y]:
            return
        self.visible += 1
        self.visibility_grid[x][y] = True

    def count(self):
        for row_idx in range(len(self.canopy)):
            self.count_visible_in_row(row_idx)
        for column_idx in range(len(self.canopy[0])):
            self.count_visible_in_column(column_idx)

    def count_visible_in_row(self, row_idx, idx=0, highest_seen=(-1, -1)):
        if idx == len(self.canopy[0]):
            return
        trees = (self.canopy[row_idx][idx], self.canopy[row_idx][-idx-1])
        if trees[0] > highest_seen[0]:
            self.set_visible(row_idx, idx)
        if trees[1] > highest_seen[1]:
            self.set_visible(row_idx, -idx-1)
        return self.count_visible_in_row(row_idx, idx + 1, highest_trees(trees, highest_seen))

    def count_visible_in_column(self, column_idx, idx=0, highest_seen=(-1, -1)):
        if idx == len(self.canopy):
            return
        trees = (self.canopy[idx][column_idx], self.canopy[-idx-1][column_idx])
        if trees[0] > highest_seen[0]:
            self.set_visible(idx, column_idx)
        if trees[1] > highest_seen[1]:
            self.set_visible(-idx-1, column_idx)
        return self.count_visible_in_column(column_idx, idx + 1, highest_trees(trees, highest_seen))


def part1(file_path):
    canopy = read_canopy_from_file(file_path)
    canopy_counter = CanopyCounter(canopy)
    canopy_counter.count()
    return canopy_counter.visible


def calculate_scenic_score(grid, x, y):
    current_tree = grid[x][y]
    score = 1
    score_dir = 0
    for i in range(x-1, 0-1, -1):
        score_dir += 1
        if grid[i][y] >= current_tree:
            break
    score *= score_dir
    score_dir = 0
    for j in range(x+1, len(grid)):
        score_dir += 1
        if grid[j][y] >= current_tree:
            break
    score *= score_dir
    score_dir = 0
    for k in range(y-1, -1, -1):
        score_dir += 1
        if grid[x][k] >= current_tree:
            break
    score *= score_dir
    score_dir = 0
    for l in range(y + 1, len(grid[0])):
        score_dir += 1
        if grid[x][l] >= current_tree:
            break
    score *= score_dir
    return score


def part2(file_path):
    canopy = read_canopy_from_file(file_path)
    scores = [[0 for cell in row] for row in canopy]
    for i in range(len(canopy)):
        for j in range(len(canopy[0])):
            scores[i][j] = calculate_scenic_score(canopy, i, j)
    return max([max([score for score in row]) for row in scores])


if __name__ == '__main__':
    # print(part1('../data/test_grid.txt') == 21)
    print(part1('../data/grid.txt') == 1849)
    # print(part2('../data/grid.txt'))