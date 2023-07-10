import random
from collections import defaultdict

def generate_random_grid(n_rows, n_cols):
    symbols = ['BB', 'AA', 'HH', 'GG', 'WD', 'CC', 'JT', 'EE', 'DD']
    grid = [[random.choice(symbols) for _ in range(n_cols)]
            for _ in range(n_rows)]
    return grid


n_rows, n_cols = 6, 6  # Specify the size of the grid


def get_sub_grids(grid):
    grid_2x2 = [row[2:4] for row in grid[2:4]]
    grid_4x4 = [row[1:5] for row in grid[1:5]]
    return grid_2x2, grid_4x4


def dfs(i, j, grid, wild='WD'):
    symbol = grid[i][j]
    if symbol == wild:
        return set(), ''

    stack = [(i, j)]
    visited = set()
    cluster_cells = set()
    while stack:
        x, y = stack.pop()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        cluster_cells.add((x, y))
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                if grid[nx][ny] == symbol or grid[nx][ny] == wild:
                    stack.append((nx, ny))

    return cluster_cells if len(cluster_cells) >= 4 else set(), symbol


def dfs_wild(i, j, grid, wild='WD'):
    symbol = grid[i][j]
    if symbol != wild:
        return set(), ''

    stack = [(i, j)]
    visited = set()
    cluster_cells = set()
    while stack:
        x, y = stack.pop()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        cluster_cells.add((x, y))
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == wild:
                stack.append((nx, ny))

    return cluster_cells if len(cluster_cells) >= 4 else set(), symbol


def count_clusters(grid):
    all_cluster_cells = set()
    clusters = []
    cluster_sizes = []
    symbol_clusters = defaultdict(lambda: defaultdict(int))
    cluster_grid = [list(row) for row in grid]  # Copy the grid
    cluster_index = 0
    # First phase
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i, j) not in all_cluster_cells:
                cluster_cells, symbol = dfs(i, j, grid)
                if cluster_cells:
                    all_cluster_cells.update(cluster_cells)
                    clusters.append(cluster_cells)
                    cluster_size = len(cluster_cells)
                    cluster_sizes.append(cluster_size)
                    symbol_clusters[symbol][cluster_size] += 1
                    for x, y in cluster_cells:  # Replace the symbols in the cluster by the cluster index
                        cluster_grid[x][y] = "{:02}".format(cluster_index)
                    cluster_index += 1  # Move to the next cluster index
    # Second phase
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i, j) not in all_cluster_cells:
                cluster_cells, symbol = dfs_wild(i, j, grid)
                if cluster_cells:
                    all_cluster_cells.update(cluster_cells)
                    clusters.append(cluster_cells)
                    cluster_size = len(cluster_cells)
                    cluster_sizes.append(cluster_size)
                    symbol_clusters[symbol][cluster_size] += 1
                    for x, y in cluster_cells:  # Replace the symbols in the cluster by the cluster index
                        cluster_grid[x][y] = "{:02}".format(cluster_index)
                    cluster_index += 1  # Move to the next cluster index

    return len(clusters), cluster_sizes, dict(symbol_clusters)


overall_stats = {"2x2": defaultdict(lambda: defaultdict(int)),
                 "4x4": defaultdict(lambda: defaultdict(int)),
                 "6x6": defaultdict(lambda: defaultdict(int))}

for _ in range(1000000):  
    grid = generate_random_grid(n_rows, n_cols)
    grid_2x2, grid_4x4 = get_sub_grids(grid)
    clusters_2x2, sizes_2x2, symbol_clusters_2x2 = count_clusters(grid_2x2)
    clusters_4x4, sizes_4x4, symbol_clusters_4x4 = count_clusters(grid_4x4)
    clusters_6x6, sizes_6x6, symbol_clusters_6x6 = count_clusters(grid)

    for symbol, size_dict in symbol_clusters_2x2.items():
        for size, count in size_dict.items():
            overall_stats["2x2"][symbol][size] += count

    for symbol, size_dict in symbol_clusters_4x4.items():
        for size, count in size_dict.items():
            overall_stats["4x4"][symbol][size] += count

    for symbol, size_dict in symbol_clusters_6x6.items():
        for size, count in size_dict.items():
            overall_stats["6x6"][symbol][size] += count

# Write overall stats to file
with open('simulation_output.txt', 'w') as f:
    for grid_size, symbol_stats in overall_stats.items():
        f.write(f"\n\n****** {grid_size} ******\n")
        for symbol, size_dict in symbol_stats.items():
            f.write(f"\n--- {symbol} ---\n")
            for size, count in size_dict.items():
                f.write(f"Size {size}: {count} times\n")
