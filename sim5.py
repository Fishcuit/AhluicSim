def create_grid(columns):
    grid = [list(column) for column in zip(*columns)]
    return grid


def get_sub_grids(grid):
    grid_2x2 = [row[2:4] for row in grid[2:4]]
    grid_4x4 = [row[1:5] for row in grid[1:5]]
    return grid_2x2, grid_4x4


def dfs(i, j, visited, grid, wild='🃏'):
    stack = [(i, j)]
    size = 0
    while stack:
        x, y = stack.pop()
        size += 1
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and (nx, ny) not in visited and (grid[nx][ny] == grid[x][y] or grid[nx][ny] == wild):
                visited.add((nx, ny))
                stack.append((nx, ny))
    return size


def count_clusters(grid):
    visited = set()
    clusters = 0
    cluster_sizes = []  # Store sizes of each cluster found

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i, j) not in visited:
                visited.add((i, j))
                cluster_size = dfs(i, j, visited, grid)
                if cluster_size >= 4:  # Count as a cluster if size is 4 or more
                    clusters += 1
                    cluster_sizes.append(cluster_size)
    return clusters, cluster_sizes


columns = [
    ['⭐', '🟩', '🔷', '⭐', '🔷', '🔶'],
    ['⭐', '⭐', '🃏', '⭐', '🔷', '🔶'],
    ['🔷', '🟩', '🟩', '🟩', '🔷', '🔶'],
    ['⭐', '🟩', '🔷', '🟩', '🔶', '🃏'],
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
