import tkinter as tk
from tkinter import messagebox
import time
import random
import sys

sys.setrecursionlimit(20000) 

GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]

def get_moves(board):
    try:
        zero_index = board.index(0)
    except ValueError:
        return []

    directions = [
        (zero_index - 3, zero_index >= 3),       # Up
        (zero_index + 1, zero_index % 3 != 2),    # Righ
        (zero_index + 3, zero_index < 6),         # Down
        (zero_index - 1, zero_index % 3 != 0)     # Left
    ]

    moves = []
    for target_idx, condition in directions:
        if condition:
            new_board = list(board) 
            new_board[zero_index], new_board[target_idx] = new_board[target_idx], new_board[zero_index]
            moves.append(new_board)
            
    return moves

def generate_random_solvable_board(steps=10):
    current = GOAL_STATE.copy()
    for _ in range(steps):
        possible = get_moves(current)
        current = random.choice(possible)
    return current


def solve_recursive(queue, visited_set): 
    if not queue:
        return None

    current_item = queue[0]
    rest_of_queue = queue[1:]

    current_board, path = current_item

    if current_board == GOAL_STATE:
        return path
    
    possible_moves = get_moves(current_board)

    new_entries = []
    updated_visited_set = visited_set.copy()
    
    for move in possible_moves:
        move_tuple = tuple(move)
        if move_tuple not in visited_set:
            updated_visited_set.add(move_tuple)
            new_path = path + [move]    
            new_entries.append((move, new_path))
    
    return solve_recursive(rest_of_queue + new_entries, updated_visited_set)


def start_functional_solver(start_board):
    initial_queue = [(start_board, [start_board])]
    initial_visited = {tuple(start_board)}
    
    return solve_recursive(initial_queue, initial_visited)


class EightPuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle (Functional/Recursive Solver)")
        
        self.current_state = GOAL_STATE.copy()
        self.buttons = []
        
        self.create_widgets()
        self.update_display(self.current_state)

    def create_widgets(self):
        frame_grid = tk.Frame(self.root, bg='#222')
        frame_grid.pack(pady=20)

        row_buttons = []
        for i in range(9):
            btn = tk.Button(frame_grid, text="", font=('Arial', 24, 'bold'), 
                            width=4, height=2, bg='white', relief=tk.RIDGE)
            r = i // 3
            c = i % 3
            btn.grid(row=r, column=c, padx=2, pady=2)
            row_buttons.append(btn)
            if (i + 1) % 3 == 0:
                self.buttons.append(row_buttons)
                row_buttons = []

        frame_controls = tk.Frame(self.root)
        frame_controls.pack(pady=10)

        shuffle_btn = tk.Button(frame_controls, text="Shuffle (12 Steps)", 
                              bg='#FF9800', fg='white', font=('Arial', 11),
                              command=self.shuffle_board)
        shuffle_btn.pack(side=tk.LEFT, padx=5)

        solve_btn = tk.Button(frame_controls, text="Solve Recursively", 
                              bg='#9C27B0', fg='white', font=('Arial', 11),
                              command=self.start_solving_animation)
        solve_btn.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(self.root, text="Functional Mode. Ready.", font=('Arial', 10), fg="purple")
        self.status_label.pack(pady=5)

    def update_display(self, board):
        for i in range(9):
            r = i // 3
            c = i % 3
            val = board[i]
            if val == 0:
                self.buttons[r][c].config(text="", bg="#555")
            else:
                self.buttons[r][c].config(text=str(val), bg="white")
        self.root.update()

    def shuffle_board(self):
        self.status_label.config(text="Shuffling...", fg="orange")
        self.root.update()
        self.current_state = generate_random_solvable_board(steps=12) 
        self.update_display(self.current_state)
        self.status_label.config(text="Board Shuffled.", fg="purple")

    def start_solving_animation(self):
        self.status_label.config(text="Thinking (Recursively)...", fg="orange")
        self.root.update()

        try:
            path = start_functional_solver(self.current_state)

            if path:
                self.status_label.config(text=f"Solved! ({len(path)-1} moves)", fg="green")
                
                for step_board in path:
                    self.current_state = step_board
                    self.update_display(step_board)
                    time.sleep(0.3)
                messagebox.showinfo("Success", "Puzzle Solved using Functional Paradigm!")
            else:
                self.status_label.config(text="No solution found.", fg="red")
                messagebox.showerror("Failed", "No solution found.")
                
        except RecursionError:
            self.status_label.config(text="Stack Overflow!", fg="red")
            messagebox.showerror("Error", "Recursion Limit Exceeded!\nThis is a limitation of pure recursion for deep searches in Python.")

if __name__ == "__main__":
    root = tk.Tk()
    gui = EightPuzzleGUI(root)
    root.resizable(False, False)
    root.mainloop()