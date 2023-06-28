from collections import defaultdict

def dfs(grid, i, j, visited, current_cluster, symbol):
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    stack = [(i, j)]
    while stack:
        x, y = stack.pop()
        if (x, y) not in visited and (grid[x][y] == symbol or grid[x][y] == '🃏'):
            visited.add((x, y))
            current_cluster.append((x, y))
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols:
                    stack.append((nx, ny))

def count_clusters(grid):
    visited = set()
    clusters = defaultdict(list)
    cell_to_cluster = {}
    rows, cols = len(grid), len(grid[0])
    cluster_id = 0
    for i in range(rows):
        for j in range(cols):
            if (i, j) not in visited and grid[i][j] != '🃏':
                current_cluster = []
                dfs(grid, i, j, visited, current_cluster, grid[i][j])
                if len(current_cluster) >= 4:  # only consider cluster if its size >= 4
                    clusters[cluster_id] = current_cluster
                    for cell in current_cluster:
                        cell_to_cluster[cell] = cluster_id
                    cluster_id += 1
    return clusters, cell_to_cluster

def check_grid_sizes(grid, clusters):
    sizes = [2, 4, 6]
    counts = []
    for size in sizes:
        count = 0
        min_row, max_row = 3 - size // 2, 3 + size // 2
        min_col, max_col = 3 - size // 2, 3 + size // 2
        for cluster in clusters.values():
            if all(min_row <= x < max_row and min_col <= y < max_col for x, y in cluster):
                count += 1
        counts.append(count)
    return counts


grid = [
    ['🃏', '🟩', '🔷', '⭐', '🟩', '🔶'],
    ['⭐', '🔶', '🔷', '⭐', '🟩', '🔶'],
    ['⭐', '🔶', '🔶', '⭐', '🟩', '🔶'],
    ['⭐', '🟩', '🔷', '🃏', '🟩', '🔶'],
    ['⭐', '🟩', '🔷', '⭐', '🔷', '🔶'],
    ['⭐', '🟩', '🔷', '⭐', '🟩', '🔶']
]

clusters, cell_to_cluster = count_clusters(grid)
print(f"Total number of clusters: {len(clusters)}")

counts = check_grid_sizes(grid, clusters)
print("Number of clusters in 2x2 grid: ", counts[0])
print("Number of clusters in 4x4 grid: ", counts[1])
print("Number of clusters in 6x6 grid: ", counts[2])

