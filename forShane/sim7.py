def create_grid(columns):
    grid = [list(column) for column in zip(*columns)]
    return grid


def get_sub_grids(grid):
    grid_2x2 = [row[2:4] for row in grid[2:4]]
    grid_4x4 = [row[1:5] for row in grid[1:5]]
    return grid_2x2, grid_4x4


def dfs(i, j, grid, wild='WD', non_cluster_symbols=('JT', 'BT')):
    symbol = grid[i][j]
    if symbol in non_cluster_symbols or symbol == wild:
        return set()

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
                if grid[nx][ny] not in non_cluster_symbols and (grid[nx][ny] == symbol or grid[nx][ny] == wild):
                    stack.append((nx, ny))

    return cluster_cells if len(cluster_cells) >= 4 else set()


# I am separating the wild card function from the dfs function, this dfs function will count clusters of wild symbols only if they have no adjacent symbols;
def dfs_wild(i, j, grid, non_cluster_symbols=['JT', 'BT'], wild='WD'):
    symbol = grid[i][j]
    if symbol != wild:
        return set()

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
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and (nx, ny) not in visited:
                if grid[nx][ny] == wild:
                    stack.append((nx, ny))
        cluster_cells = set(cell for cell in cluster_cells if all(
            0 > nx or nx >= len(grid) or 0 > ny or ny >= len(
                grid[0]) or grid[nx][ny] == wild or grid[nx][ny] in non_cluster_symbols
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for nx, ny in [(cell[0] + dx, cell[1] + dy)]
        ))

    return cluster_cells if len(cluster_cells) >= 4 else set()


def count_clusters(grid):
    all_cluster_cells = set()
    clusters = []
    cluster_sizes = []
    cluster_symbols = []
    # First phase
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i, j) not in all_cluster_cells:
                cluster_cells = dfs(i, j, grid)
                if cluster_cells:
                    all_cluster_cells.update(cluster_cells)
                    clusters.append(cluster_cells)
                    cluster_sizes.append(len(cluster_cells))
                    cluster_symbols.append(grid[i][j])
    # Second phase
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i, j) not in all_cluster_cells:
                cluster_cells = dfs_wild(i, j, grid)
                if cluster_cells:
                    all_cluster_cells.update(cluster_cells)
                    clusters.append(cluster_cells)
                    cluster_sizes.append(len(cluster_cells))
                    cluster_symbols.append(grid[i][j])

    return len(clusters), list(zip(cluster_sizes, cluster_symbols))


# columns = [
#     ['HH', 'HH', 'HH', 'HH', 'HH', 'HH'],
#     ['HH', 'WD', 'WD', 'WD', 'BB', 'HH'],
#     ['HH', 'WD', 'WD', 'WD', 'BB', 'HH'],
#     ['HH', 'WD', 'WD', 'WD', 'WD', 'HH'],
#     ['HH', 'HH', 'AA', 'BB', 'CC', 'HH'],
#     ['HH', 'HH', 'HH', 'HH', 'HH', 'HH']
# ]
# columns = [
#     ['HH', 'HH', 'HH', 'HH', 'HH', 'HH'],
#     ['HH', 'WD', 'WD', 'WD', 'WD', 'HH'],
#     ['HH', 'WD', 'WD', 'WD', 'WD', 'HH'],
#     ['HH', 'WD', 'WD', 'WD', 'WD', 'HH'],
#     ['HH', 'WD', 'WD', 'WD', 'WD', 'HH'],
#     ['HH', 'HH', 'HH', 'HH', 'HH', 'HH']
# ]
# columns = [
#     ['CC', 'GG', 'AA', 'WD', 'WD', 'AA'],
#     ['GG', 'AA', 'BB', 'HH', 'JT', 'CC'],
#     ['BB', 'DD', 'BT', 'BT', 'JT', 'CC'],
#     ['JT', 'JT', 'BT', 'BT', 'HH', 'AA'],
#     ['BT', 'BT', 'DD', 'EE', 'AA', 'DD'],
#     ['AA', 'EE', 'GG', 'WD', 'JT', 'DD']
# ]
# 'WD' cluster of size 4
columns = [
    ['WD', 'WD', 'AA', 'BT', 'BT', 'BT'],
    ['WD', 'WD', 'BT', 'BT', 'BT', 'BT'],
    ['BT', 'BT', 'AA', 'WD', 'BT', 'BT'],
    ['BT', 'BT', 'WD', 'WD', 'BT', 'BT'],
    ['BT', 'BT', 'BT', 'BT', 'BT', 'BT'],
    ['BT', 'BT', 'BT', 'BT', 'BT', 'BT'],
]

grid = create_grid(columns)
grid_2x2, grid_4x4 = get_sub_grids(grid)

clusters_2x2, sizes_and_symbols_2x2 = count_clusters(grid_2x2)
clusters_4x4, sizes_and_symbols_4x4 = count_clusters(grid_4x4)
clusters_6x6, sizes_and_symbols_6x6 = count_clusters(grid)

print(
    f"2x2 grid has {clusters_2x2} clusters with sizes and symbols {sizes_and_symbols_2x2}")
print(
    f"4x4 grid has {clusters_4x4} clusters with sizes and symbols {sizes_and_symbols_4x4}")
print(
    f"6x6 grid has {clusters_6x6} clusters with sizes and symbols {sizes_and_symbols_6x6}")
