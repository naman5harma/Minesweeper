import tkinter as tk
import random

class MinesweeperGUI:
    def __init__(self, master, rows=16, cols=30, mines=99):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.buttons = []
        self.mine_positions = set()
        self.flags = set()
        self.first_click = True  # Flag to track first click

        self.create_grid()

    def create_grid(self):
        for row in range(self.rows):
            button_row = []
            for col in range(self.cols):
                button = tk.Button(self.master, width=2, height=1)
                button.bind('<Button-1>', lambda event, r=row, c=col: self.click(event, r, c))
                button.bind('<Button-3>', lambda event, r=row, c=col: self.toggle_flag(event, r, c))
                button.grid(row=row, column=col)
                button_row.append(button)
            self.buttons.append(button_row)

    def handle_first_click(self, row, col):
        possible_positions = [(r, c) for r in range(self.rows) for c in range(self.cols) if abs(r - row) > 1 or abs(c - col) > 1]
        self.mine_positions = set(random.sample(possible_positions, self.mines))

        # Calculate adjacent mine counts for revealed squares
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) not in self.mine_positions:
                    adjacent_mines = sum(1 for dr in [-1, 0, 1] for dc in [-1, 0, 1]
                                         if (r+dr, c+dc) in self.mine_positions)
                    self.mine_positions.add((r, c)) if adjacent_mines == 0 else None

        # Reveal the area around the clicked square and its neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                    if (new_row, new_col) not in self.mine_positions:
                        count = sum(1 for dr2 in [-1, 0, 1] for dc2 in [-1, 0, 1]
                                     if (new_row+dr2, new_col+dc2) in self.mine_positions)
                        if count > 0:
                            self.buttons[new_row][new_col].config(text=str(count))
                        else:
                            self.buttons[new_row][new_col].config(text=" ")
                            self.uncover_neighbors(new_row, new_col)

    def create_mines(self, row, col):
        possible_positions = [(r, c) for r in range(self.rows) for c in range(self.cols) if (r, c) != (row, col)]
        self.mine_positions = set(random.sample(possible_positions, self.mines))

        # Calculate adjacent mine counts
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) not in self.mine_positions:
                    adjacent_mines = sum(1 for dr in [-1, 0, 1] for dc in [-1, 0, 1]
                                         if (r+dr, c+dc) in self.mine_positions)
                    self.mine_positions.add((r, c)) if adjacent_mines == 0 else None

    def uncover(self, row, col):
        if self.first_click:
            self.handle_first_click(row, col)
            self.first_click = False
        if (row, col) in self.mine_positions:
            self.buttons[row][col].config(text="M")
            self.game_over()
        else:
            count = sum(1 for dr in [-1, 0, 1] for dc in [-1, 0, 1]
                        if (row+dr, col+dc) in self.mine_positions)
            if count > 0:
                self.buttons[row][col].config(text=str(count))
            else:
                self.buttons[row][col].config(text=" ")
                self.uncover_neighbors(row, col)

    def uncover_neighbors(self, row, col):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        revealed = set()
        revealed.add((row, col))

        while len(revealed) > 0:
            current = revealed.pop()
            current_row, current_col = current[0], current[1]

            count = sum(1 for dr in [-1, 0, 1] for dc in [-1, 0, 1]
                        if (current_row+dr, current_col+dc) in self.mine_positions)

            if count == 0:
                for d in directions:
                    new_row, new_col = current_row + d[0], current_col + d[1]
                    if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                        if (new_row, new_col) not in revealed and (new_row, new_col) not in self.mine_positions:
                            self.buttons[new_row][new_col].config(text=" ")
                            revealed.add((new_row, new_col))

            if count > 0:
                self.buttons[current_row][current_col].config(text=str(count))

    def click(self, event, row, col):
        if (row, col) not in self.flags:
            self.uncover(row, col)

    def toggle_flag(self, event, row, col):
        button = self.buttons[row][col]
        if button['state'] != 'disabled':
            if (row, col) not in self.flags:
                self.flags.add((row, col))
                button.config(text="F", fg="red")  # Flag displayed as "F" and colored red
            else:
                self.flags.remove((row, col))
                button.config(text="")
            # Re-enable right-click event binding
            button.bind('<Button-3>', lambda event, r=row, c=col: self.toggle_flag(event, r, c))

    def game_over(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) in self.mine_positions:
                    self.buttons[row][col].config(text="M")
                self.buttons[row][col].config(state='disabled')


def main():
    root = tk.Tk()
    root.title("Minesweeper")
    minesweeper_game = MinesweeperGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
