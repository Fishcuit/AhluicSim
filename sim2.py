import numpy as np
import random

# Just random columns I made for testing. Replace with your own.
columns = [
    ['⭐', '🟩', '🔷', '⭐', '🔷', '🔶'],
    ['⭐', '🟩', '⭐', '⭐', '🔷', '🔶'],
    ['⭐', '🔷', '⭐', '🟩', '🔷', '🔶'],
    ['⭐', '🟩', '🔷', '🟩', '🔷', '🔶'],
    ['⭐', '🟩', '🔷', '🟩', '🔷', '🔶'],
    ['⭐', '🟩', '🔷', '🟩', '🔷', '🔶']
]

bonus_symbol = '🃏'  # Bonus symbol for testing. Replace with your own.


def play_round():
    # Ok so I think this might be the best way to do it. It will take your list into a 2d array as the columns.
    reel = np.array(columns)  # Puts the lists into an array as columns

    # Calculate all winning clusters in the reel.
    # Check the center 2x2 grid
    center = reel[2:4, 2:4]  # Evaluate the center 2x2 grid
    print(center)
    clusters_center = get_clusters(center)
    clusters = get_clusters(center)
    print("Number of clusters in Center: ", len(clusters_center))

    # Check the secondary 4x4 grid
    secondary = reel[1:5, 1:5]  # Evaluate the secondary 4x4 grid
    print(secondary)
    clusters = get_clusters(secondary)
    clusters_secondary = get_clusters(secondary)
    print("Number of clusters in Secondary: ", len(clusters_secondary))

    # Check the whole 6x6 grid
    print(reel)
    clusters_whole = get_clusters(reel)
    clusters = get_clusters(reel)  # Evaluate the whole 6x6 grid
    print("Number of clusters in Whole: ", len(clusters_whole))

    # Prints data, prob wont need this for your sim
    print("----------------------------------------------------")

    # Check if the BIG FOUR SYMBOL is in a corner. Its the star symbol.
    # corners = [reel[0, 0], reel[0, -1], reel[-1, 0], reel[-1, -1]]

    # if '⭐' in corners and grid_size < 6:
    #     # If the BIG FOUR SYMBOL is in a corner, increase the grid size for the next round.
    #     return grid_size + 2
    # else:
    #     # If the BIG FOUR SYMBOL is not in a corner, reset the grid size to 2x2 for the next round.
    #     return 2


def get_clusters(reel):
    # Create a 2D boolean array of the same shape as the reel,
    # with all elements initially set to False. This will track
    # which cells we've already visited.
    visited = np.zeros(reel.shape, dtype=bool)

    clusters = []  # Initialize the list of clusters to empty.

    # For each cell in the reel:
    for i in range(reel.shape[0]):
        for j in range(reel.shape[1]):
            # If we haven't visited this cell yet:
            if not visited[i, j]:
                # Calculate the cluster starting from this cell, and if it's a winning cluster
                # (i.e., has 4 or more cells), add it to our list of clusters.
                cluster = get_cluster(reel, visited, i, j)
                if len(cluster) >= 4:
                    clusters.append(cluster)
    return clusters


def get_cluster(reel, visited, i, j):
    symbol = reel[i, j]  # The symbol in the current cell.
    cluster = [(i, j)]  # Start with just the current cell itself.
    stack = [(i, j)]  # Start with the current cell.

    # Mark the initial cell as visited, unless it's the bonus symbol.
    if symbol != bonus_symbol:
        visited[i, j] = True

    while stack:  # While there are still cells to visit:
        x, y = stack.pop()  # Pop a cell from the stack.

        # For each of the cell's four neighbors:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy

            # If the neighbor is within the grid, has the same symbol as the current cell, or is a bonus symbol,
            # and hasn't been visited yet (unless it's the bonus symbol):
            if (0 <= nx < reel.shape[0] and 0 <= ny < reel.shape[1] and
                (reel[nx, ny] == symbol or reel[nx, ny] == bonus_symbol) and 
                (not visited[nx, ny] or reel[nx, ny] == bonus_symbol)):

                # Add the neighbor to the stack.
                stack.append((nx, ny))

                # Mark it as visited (unless it's the bonus symbol), and add it to the cluster.
                if reel[nx, ny] != bonus_symbol:
                    visited[nx, ny] = True
                cluster.append((nx, ny))

    return cluster


# Function to calculate win based on clusters


play_round()
