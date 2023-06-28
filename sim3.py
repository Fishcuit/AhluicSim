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

    # First, find all clusters including '🃏'
    for i in range(rows):
        for j in range(cols):
            if (i, j) not in visited:
                current_cluster = []
                dfs(grid, i, j, visited, current_cluster, grid[i][j])
                clusters[cluster_id] = current_cluster
                for cell in current_cluster:
                    cell_to_cluster[cell] = cluster_id
                cluster_id += 1

    # Then, merge clusters that are connected by a '🃏'
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '🃏':
                connected_clusters = set()
                for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                    nx, ny = i + dx, j + dy
                    if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) in cell_to_cluster:
                        connected_clusters.add(cell_to_cluster[(nx, ny)])
                if len(connected_clusters) > 1:
                    # Merge clusters
                    clusters_to_merge = [clusters[cluster_id]
                                         for cluster_id in connected_clusters]
                    merged_cluster = [
                        cell for cluster in clusters_to_merge for cell in cluster]
                    # Update cell_to_cluster
                    for cell in merged_cluster:
                        cell_to_cluster[cell] = min(connected_clusters)
                    # Update clusters
                    for cluster_id in connected_clusters:
                        if cluster_id != min(connected_clusters):
                            del clusters[cluster_id]
                    clusters[min(connected_clusters)] = merged_cluster
        for cluster_id, cluster in clusters.items():
            print(f"Cluster {cluster_id}: {cluster}")

    return clusters, cell_to_cluster


def check_grid_sizes(grid, clusters):
    sizes = [2, 4, 6]
    # Adjust the indices to cover the correct area
    grid_positions = [(2, 4), (1, 5), (0, 6)]
    counts = []
    for size, (min_row_col, max_row_col) in zip(sizes, grid_positions):
        count = 0
        for cluster in clusters.values():
            if all(min_row_col <= x < max_row_col and min_row_col <= y < max_row_col for x, y in cluster):
                count += 1
        counts.append(count)
    return counts


grid = [
    ['🃏', '🟩', '🔷', '⭐', '🟩', '🔶'],
    ['⭐', '🔶', '🔷', '⭐', '🟩', '🔶'],
    ['⭐', '🔶', '🔶', '⭐', '🟩', '🔶'],
    ['⭐', '🟩', '🔷', '⭐', '🟩', '🔶'],
    ['⭐', '🟩', '🔷', '⭐', '🔷', '🔶'],
    ['⭐', '🟩', '🔷', '⭐', '🟩', '🔶']
]

clusters, cell_to_cluster = count_clusters(grid)
print(f"Total number of clusters: {len(clusters)}")

counts = check_grid_sizes(grid, clusters)
print("Number of clusters in 2x2 grid: ", counts[0])
print("Number of clusters in 4x4 grid: ", counts[1])
print("Number of clusters in 6x6 grid: ", counts[2])
