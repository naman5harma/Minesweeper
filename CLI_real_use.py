import numpy as np
from random import sample
import itertools
from tqdm import tqdm

# Initialize parameters
rows, cols, mines = 16, 30, 1

# Initialize the board with no mines
board = np.zeros((rows, cols), dtype=int)

# Function to print the board
def print_board(board):
    for row in board:
        print(' '.join(str(cell) for cell in row))

# Function to place mines randomly on the board
def place_mines(board, mines):
    rows, cols = board.shape
    mine_positions = sample(list(itertools.product(range(rows), range(cols))), mines)
    for pos in mine_positions:
        board[pos] = -1  # Let's use -1 to represent a mine
    return board

# Function to calculate the number of adjacent mines for each cell
def calculate_adjacent_mines(board):
    rows, cols = board.shape
    for row in range(rows):
        for col in range(cols):
            if board[row, col] == -1:
                continue
            # Count mines in adjacent cells
            mines_count = sum([board[r, c] == -1 for r in range(max(0, row-1), min(rows, row+2))
                              for c in range(max(0, col-1), min(cols, col+2))])
            board[row, col] = mines_count
    return board

# Place mines and calculate adjacent mines
board = place_mines(board, mines)
board = calculate_adjacent_mines(board)

# Print the board with mines and numbers
print_board(board)
def print_player_board(player_board):
    for row in player_board:
        print(' '.join('?' if cell == -2 else 'F' if cell == -3 else ' ' if cell == 0 else str(cell) for cell in row))

# Initialize player's board with unrevealed cells marked as -2
player_board = np.full((rows, cols), -2, dtype=int)

# Function to reveal a cell on the player's board
# If the player selects a cell with no adjacent mines, reveal all adjacent cells recursively

def reveal_cell(board, player_board, row, col):
    if player_board[row, col] >= 0:
        return # Cell already revealed
    if board[row, col] == -1:
        player_board[row, col] = -1 # Reveal mine
        return
    player_board[row, col] = board[row, col] # Reveal cell
    if board[row, col] == 0:
        for r in range(max(0, row-1), min(rows, row+2)):
            for c in range(max(0, col-1), min(cols, col+2)):
                if (r, c) != (row, col):
                    reveal_cell(board, player_board, r, c)

# Function to place a flag on the player's board

def place_flag(player_board, row, col):
    if player_board[row, col] == -2: # If cell is unrevealed
        player_board[row, col] = -3 # Place flag
    elif player_board[row, col] == -3: # If cell is flagged
        player_board[row, col] = -2 # Remove flag

# Function to check for win condition

def check_win(board, player_board):
    return np.all((board >= 0) == (player_board >= 0))

# Function to start the game

def start_game(board):
    while True:
        print_player_board(player_board)
        action = input('Choose an action (reveal, flag, quit): ')
        if action == 'quit':
            break
        row = int(input('Enter row number (0-15): '))
        col = int(input('Enter column number (0-29): '))
        if action == 'reveal':
            reveal_cell(board, player_board, row, col)
            if player_board[row, col] == -1: # If a mine is revealed
                print('Boom! Game over.')
                break
        elif action == 'flag':
            place_flag(player_board, row, col)
        if check_win(board, player_board):
            print('Congratulations! You have won the game!')
            break

# Start the game
start_game(board)
