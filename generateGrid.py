import random

def generate_random_grid(n_rows, n_cols):
    symbols = ['⭐', '🟩', '🔷', '🔶', '🃏']
    grid = [[random.choice(symbols) for _ in range(n_cols)] for _ in range(n_rows)]
    return grid

n_rows, n_cols = 6, 6  # Specify the size of the grid
grid = generate_random_grid(n_rows, n_cols)

for row in grid:
    print(row)
