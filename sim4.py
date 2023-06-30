def create_grid(columns):
    grid = [list(column) for column in zip(*columns)]
    return grid


def get_sub_grids(grid):
    grid_2x2 = [row[2:4] for row in grid[2:4]]
    grid_4x4 = [row[1:5] for row in grid[1:5]]
    return grid_2x2, grid_4x4


def dfs(i, j, grid, wild='🃏'):
    stack = [(i, j)]
    visited = set()
    symbol = grid[i][j]
    cluster_cells = set()  # To store the cells belonging to the current cluster
    while stack:
        x, y = stack.pop()
        if (x, y) in visited:  # Skip visited cells
            continue
        visited.add((x, y))
        cluster_cells.add((x, y))
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                if grid[nx][ny] == symbol or grid[nx][ny] == wild or symbol == wild:
                    stack.append((nx, ny))
    return cluster_cells if len(cluster_cells) >= 4 else set()  # Return cells if it's a cluster

def count_clusters(grid):
    all_cluster_cells = set()  # Keep track of all cells that are part of any cluster
    clusters = []
    cluster_sizes = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i, j) not in all_cluster_cells:  # Only start a new DFS if the cell is not part of any cluster
                cluster_cells = dfs(i, j, grid)
                if cluster_cells:  # If it's a cluster
                    all_cluster_cells.update(cluster_cells)  # Add the cells to the set of all cluster cells
                    clusters.append(cluster_cells)
                    cluster_sizes.append(len(cluster_cells))
    return len(clusters), cluster_sizes





columns = [
    ['⭐', '🟩', '🔷', '⭐', '🔷', '🔶'],
    ['⭐', '⭐', '🃏', '⭐', '🔷', '🔶'],
    ['🔷', '🟩', '🟩', '🟩', '🔷', '🔶'],
    ['⭐', '🟩', '🃏', '🟩', '🃏', '🃏'],
    ['⭐', '🟩', '🔷', '🟩', '🔷', '🔶'],
    ['⭐', '🟩', '🔷', '🟩', '🔷', '🔶']
]

grid = create_grid(columns)
grid_2x2, grid_4x4 = get_sub_grids(grid)

clusters_2x2, sizes_2x2 = count_clusters(grid_2x2)
clusters_4x4, sizes_4x4 = count_clusters(grid_4x4)
clusters_6x6, sizes_6x6 = count_clusters(grid)

print(f"2x2 grid has {clusters_2x2} clusters with sizes {sizes_2x2}")
print(f"4x4 grid has {clusters_4x4} clusters with sizes {sizes_4x4}")
print(f"6x6 grid has {clusters_6x6} clusters with sizes {sizes_6x6}")

