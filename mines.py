import tkinter as tk
import random
from collections import deque

def generate_grid(size, num_mines):
    grid = [['G' for _ in range(size)] for _ in range(size)]  # 'G' for gem (safe)
    mine_positions = random.sample([(r, c) for r in range(size) for c in range(size)], num_mines)
    for r, c in mine_positions:
        grid[r][c] = 'M'  # 'M' for mine
    return grid

def bfs_solve(grid):
    size = len(grid)
    queue = deque([(0, 0, [])])
    visited = set()
    while queue:
        r, c, path = queue.popleft()
        if (r, c) in visited:
            continue
        visited.add((r, c))
        path = path + [(r, c)]
        if grid[r][c] == 'M':
            return path  # Stop if a mine is hit
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size and (nr, nc) not in visited:
                queue.append((nr, nc, path))
    return path

def dfs_solve(grid):
    size = len(grid)
    stack = [(0, 0, [])]
    visited = set()
    while stack:
        r, c, path = stack.pop()
        if (r, c) in visited:
            continue
        visited.add((r, c))
        path = path + [(r, c)]
        if grid[r][c] == 'M':
            return path  # Stop if a mine is hit
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size and (nr, nc) not in visited:
                stack.append((nr, nc, path))
    return path

def reveal_tile(r, c, grid, labels, popup):
    if grid[r][c] == 'M':
        labels[r][c].config(bg='red', text='💣')  # Mine
        game_over_popup(popup)
    else:
        labels[r][c].config(bg='green', text='💎')  # Gem

def game_over_popup(popup):
    game_over = tk.Toplevel(popup)
    game_over.title("Game Over")
    tk.Label(game_over, text="You hit a mine! Game Over!", font=("Arial", 14)).pack(padx=20, pady=20)
    tk.Button(game_over, text="Close", command=popup.destroy).pack()

def show_game_popup(grid, path):
    size = len(grid)
    popup = tk.Toplevel()
    popup.title("Stake Mines - AI Solver")
    labels = []
    
    for r in range(size):
        row_labels = []
        for c in range(size):
            color = "white"
            if (r, c) in path:
                color = "blue"
            label = tk.Label(popup, bg=color, width=4, height=2, borderwidth=1, relief="solid")
            label.grid(row=r, column=c)
            label.bind("<Button-1>", lambda e, row=r, col=c: reveal_tile(row, col, grid, labels, popup))
            row_labels.append(label)
        labels.append(row_labels)
    popup.mainloop()

def play_game(solve_with_bfs=True):
    size = 5
    num_mines = int(input("Enter number of mines: "))  # User selects number of mines
    grid = generate_grid(size, num_mines)
    path = bfs_solve(grid) if solve_with_bfs else dfs_solve(grid)
    show_game_popup(grid, path)

if __name__ == "__main__":
    play_game(solve_with_bfs=True)  # Change to False for DFS
