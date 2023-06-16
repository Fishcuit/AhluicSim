import numpy as np
import random
reel = 0
total_scatter_pay = 0
total_cluster_pay = 0
total_pay = 0
reel1_triggered = 0
reel2_triggered = 0
bet = 50 #coins
increment_factor = 0
turnover = 0
free_spin_feature = 0
# Define the reel files and their weights
reel_files = ['BaseReels1.txt', 'BaseReels2.txt']
reel_weights = [1, 2]


# Symbols in the reel
symbolss = ['🃏', '😷', '🐅', '🐢', '🦎', '🔶', '📘', '🔷', '🟩', '⭐']
weights_r1 = [10, 100, 150, 250, 450, 200, 400, 425, 450, 750]
weights_r2_r3 = [55, 50, 100, 200, 275, 500, 400, 420, 475, 0]

symbols_map = {
    'HH': '🟩',
    'GG': '🔷',
    'FF': '📘',
    'EE': '🔶',
    'DD': '🦎',
    'CC': '🐢',
    'BB': '🐅',
    'AA': '😷',
    'WD': '🃏',
    'BT': '⭐',
    'MS': '🙈',

}

# Score for each cluster size
scoring = {
    '🟩': {4: 10, 5: 20, 6: 30, 7: 50, range(8, 9): 60,  range(10, 12): 80, range(12, 15): 90, range(15, 20): 100, range(20, 25): 150, range(25, 30): 200, range(30,): 300},
    '🔷': {4: 10, 5: 20, 6: 30, 7: 50, range(8, 9): 60,  range(10, 12): 80, range(12, 15): 90, range(15, 20): 100, range(20, 25): 150, range(25, 30): 200, range(30,): 300},
    '📘': {4: 10, 5: 20, 6: 30, 7: 50, range(8, 9): 60,  range(10, 12): 80, range(12, 15): 90, range(15, 20): 100, range(20, 25): 150, range(25, 30): 200, range(30,): 300},
    '🔶': {4: 20, 5: 30, 6: 40, 7: 80, range(8, 9): 100, range(10, 12): 150, range(12, 15): 200, range(15, 20): 200, range(20, 25): 300, range(25, 30): 400, range(30,): 500},
    '🦎': {4: 30, 5: 40, 6: 50, 7: 100, range(8, 9): 150,  range(10, 12): 200, range(12, 15): 250, range(15, 20): 300, range(20, 25): 400, range(25, 30): 500, range(30,): 600},
    '🐢': {4: 40, 5: 50, 6: 60, 7: 120, range(8, 9): 200,  range(10, 12): 250, range(12, 15): 300, range(15, 20): 350, range(20, 25): 500, range(25, 30): 600, range(30,): 700},
    '🐅': {4: 50, 5: 60, 6: 80, 7: 150, range(8, 9): 300,  range(10, 12): 350, range(12, 15): 400, range(15, 20): 450, range(20, 25): 600, range(25, 30): 700, range(30,): 800},
    '😷': {4: 60, 5: 80, 6: 100, 7: 200, range(8, 9): 400,  range(10, 12): 500, range(12, 15): 550, range(15, 20): 600, range(20, 25): 700, range(25, 30): 800, range(30,): 1000},
    '🃏': {4: 60, 5: 80, 6: 100, 7: 200, range(8, 9): 400,  range(10, 12): 500, range(12, 15): 550, range(15, 20): 600, range(20, 25): 700, range(25, 30): 800, range(30,): 1000},
    '⭐': {5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}

}

def load_reel_from_file(filename):
    global reel
    reels = [
        [],  # Reel 1
        [],  # Reel 2
        [],  # Reel 3
    ]
    
    with open(filename, 'r') as file:
        for line in file:
            # Split the line into symbols
            symbols = line.strip().split()

            # Convert symbols to their emoji representations and add to reels
            for i in range(3):
                reels[i].append(symbols_map[symbols[i]])
 
    for reel_idx, reel in enumerate(reels):
        for i in range(len(reel)):
            if reel[i] == '🙈':
                # Select a new symbol based on the weights
                weights = weights_r1 if reel_idx == 0 else weights_r2_r3
                new_symbol = random.choices(symbolss, weights, k=1)[0]
                reel[i] = new_symbol
      
    return reels





def play_round(grid_size):
    global free_spin_feature, turnover, bet
    # Generate a random grid of the current size.
    reel = np.random.choice(reels[0], size=(grid_size, grid_size))
    if grid_size == 2:
        turnover += bet
    # If the grid is 4x4 or larger, replace the inner grid with symbols from the second reel.
    if grid_size >= 4:
        reel[1:-1, 1:-
             1] = np.random.choice(reels[0], size=(grid_size-2, grid_size-2))

    # If the grid is 6x6 or larger, replace the innermost 2x2 grid with symbols from the first reel.
    if grid_size >= 6:
        inner_size = grid_size - 4  # The size of the innermost grid.
        # The starting index of the innermost grid.
        start = (grid_size - inner_size) // 2
        reel[start:start+inner_size, start:start +
             inner_size] = np.random.choice(reels[0], size=(inner_size, inner_size))


    # Calculate all winning clusters in the reel.
    clusters = get_clusters(reel)

    # Calculate the total win for these clusters 
    win = calculate_win(clusters, reel)
    print(f"Grid size: {grid_size}x{grid_size}")
    print(reel)
    print(f"Win: $", win)
    print("----------------------------------------------------")

    # Check if the BIG FOUR SYMBOL is in a corner. Its the star symbol.
    corners = [reel[0, 0], reel[0, -1], reel[-1, 0], reel[-1, -1]]
    if check_jackpot(reel):
        print("Jackpot! Bonus game triggered!")
        free_spin_feature += 1
        # freeSpin()
        return grid_size + 4
    elif '⭐' in corners and grid_size < 6:
        # If the BIG FOUR SYMBOL is in a corner, increase the grid size for the next round.
        return grid_size + 2
    else:
        # If the BIG FOUR SYMBOL is not in a corner, reset the grid size to 2x2 for the next round.
        return 2

# Function to get clusters
def check_jackpot(reel):
    # Assuming reel is a 2D list
    if all([item == '⭐' for sublist in reel for item in sublist]):
        return True
    return False

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
                # (i.e., has 5 or more cells), add it to our list of clusters.
                cluster = get_cluster(reel, visited, i, j)
                if len(cluster) >= 4:
                    clusters.append(cluster)
    return clusters

# Function to calculate cluster based on a specific cell


def get_cluster(reel, visited, i, j):
    symbol = reel[i, j]  # The symbol in the current cell.

    # A list to store the cells that are in the same cluster as the current cell.
    # We start with just the current cell itself.
    cluster = [(i, j)]

    # A stack for our depth-first search. We start with the current cell.
    stack = [(i, j)]

    # Mark the current cell as visited.
    visited[i, j] = True

    # While there are still cells to visit:
    while stack:
        x, y = stack.pop()  # Pop a cell from the stack.

        # For each of the cell's four neighbors:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy

            # If the neighbor is within the grid, has the same symbol as the current cell, and hasn't been visited yet:
            if (0 <= nx < reel.shape[0] and 0 <= ny < reel.shape[1] and
                    reel[nx, ny] == symbol and not visited[nx, ny]):

                # Add the neighbor to the stack and mark it as visited.
                stack.append((nx, ny))
                visited[nx, ny] = True

                # Add the neighbor to the current cluster.
                cluster.append((nx, ny))

    return cluster

# Function to calculate win based on clusters
def scatter_pay(reel):
    global bet, increment_factor
    star_symbol = '⭐'
    star_count = sum(cell == star_symbol for row in reel for cell in row)

    # Define pay table
    pay_table = {
        5: {'value': 2, 'increment': 0.00},
        6: {'value': 4, 'increment': 0.00},
        7: {'value': 6, 'increment': 0.00},
        8: {'value': 10, 'increment': 0.005},  # 0.5%
        9: {'value': 20, 'increment': 0.003},  # 0.3%
        10: {'value': 50, 'increment': 0.002},  # 0.2%
        11: {'value': 100, 'increment': 0.0002},  # 0.02%
        12: {'value': 1000, 'increment': 0.0001},  # 0.01%
 
    }
    base_value = pay_table.get(star_count, {'value': 0, 'increment': 0})['value']
    increment = pay_table.get(star_count, {'value': 0, 'increment': 0})['increment']
    if star_count > 4:
        increment_factor = 0
    return (base_value * bet) + (base_value * bet * increment * increment_factor)


def calculate_win(clusters, reel):
    global total_cluster_pay, total_scatter_pay, total_pay, bet
    win = 0
    for cluster in clusters:
        symbol = reel[cluster[0][0], cluster[0][1]]
        cluster_size = len(cluster)
        symbol_scoring = scoring.get(symbol, {})
        for cluster_range, score in symbol_scoring.items():
            if isinstance(cluster_range, range):
                if cluster_size in cluster_range:
                    total_cluster_pay+=score
                    win += score
                    break
            else:
                if cluster_size == cluster_range:
                    total_cluster_pay+=score 
                    win += score
                    break
    scatterPay = scatter_pay(reel)
    total_scatter_pay+=scatterPay
    win += scatterPay
    total_pay+=win
    return win




num_rounds = 1000
grid_size = 2  # Start with a 2x2 grid
for i in range(num_rounds):
    increment_factor += 1
    # Select a reel file
    selected_file = random.choices(reel_files, reel_weights, k=1)[0]
    if selected_file == 'BaseReels1.txt':
        reel1_triggered += 1
        reel = 0
    else :
        reel2_triggered += 1
        reel = 1

    # Load a new reel for the round
    reels = load_reel_from_file(selected_file)
    
    # Play one round of the game and get the new grid size
    grid_size = play_round(grid_size)




print(f"Total cluster pay: $", total_cluster_pay)
print(f"Total scatter pay: $", total_scatter_pay)
print(f"Total pay: $", total_pay)
print(f"Turnover: $", turnover)
print(f"RTP: ", (total_pay/turnover)*100)
print(f"Reel 1 triggered: ", reel1_triggered)
print(f"Reel 2 triggered: ", reel2_triggered)
print(f"Free spin feature triggered: {free_spin_feature} times")