import random


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
    wild_cluster = True  # Initially assume it's a wild cluster

    if symbol == wild:  # Check if there are any same symbol neighbors
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = i + dx, j + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] != wild:
                symbol = grid[nx][ny]
                wild_cluster = False  # If any neighbor is not a wild symbol, it's not a wild cluster
                break

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
                if grid[nx][ny] == symbol or (wild_cluster and grid[nx][ny] == wild) or (grid[nx][ny] == wild and not wild_cluster):
                    stack.append((nx, ny))

    return cluster_cells if len(cluster_cells) >= 4 else set()  # Return cells if it's a cluster



def count_clusters(grid):
    all_cluster_cells = set()  # Keep track of all cells that are part of any cluster
    clusters = []
    cluster_sizes = []
    cluster_grid = [list(row) for row in grid]  # Copy the grid
    cluster_index = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            # Only start a new DFS if the cell is not part of any cluster
            if (i, j) not in all_cluster_cells:
                cluster_cells = dfs(i, j, grid)
                if cluster_cells:  # If it's a cluster
                    # Add the cells to the set of all cluster cells
                    all_cluster_cells.update(cluster_cells)
                    clusters.append(cluster_cells)
                    cluster_sizes.append(len(cluster_cells))
                    for x, y in cluster_cells:  # Replace the symbols in the cluster by the cluster index
                        cluster_grid[x][y] = "{:02}".format(cluster_index)
                    cluster_index += 1  # Move to the next cluster index
    return len(clusters), cluster_sizes, cluster_grid


with open("output.txt", "w") as file:
    for _ in range(100):  # Run the simulation 100 times
        grid = generate_random_grid(n_rows, n_cols)
        grid_2x2, grid_4x4 = get_sub_grids(grid)
        clusters_2x2, sizes_2x2, cluster_grid_2x2 = count_clusters(grid_2x2)
        clusters_4x4, sizes_4x4, cluster_grid_4x4 = count_clusters(grid_4x4)
        clusters_6x6, sizes_6x6, cluster_grid_6x6 = count_clusters(grid)
        file.write(f"**********************************************************Simulation #{_ + 1}*****************************************************************\n")
        file.write("2x2 grid:\n")
        for row in grid_2x2:
            file.write(" ".join(row) + "\n")
        file.write(f"2x2 grid has {clusters_2x2} clusters with sizes {sizes_2x2}\n")

        for row in cluster_grid_2x2:
            file.write(' '.join(row)+ "\n")
        file.write("\n")

        file.write("4x4 grid:\n")
        for row in grid_4x4:
            file.write(" ".join(row) + "\n")
        file.write(f"4x4 grid has {clusters_4x4} clusters with sizes {sizes_4x4}\n")
        for row in cluster_grid_4x4:
            file.write(' '.join(row)+ "\n")
        file.write("\n")

        file.write("6x6 grid:\n")
        for row in grid:
            file.write(" ".join(row) + "\n")
        file.write(f"6x6 grid has {clusters_6x6} clusters with sizes {sizes_6x6}\n")
        for row in cluster_grid_6x6:
            file.write(' '.join(row)+ "\n")
        file.write("\n")




