import tkinter as tk
from tkinter import messagebox
import time
import random  


goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

def is_goal(board):
    return board == goal_state

def get_moves(board):
    moves = []
    try:
        zero_index = board.index(0)
    except ValueError:
        return []

    if zero_index >= 3:
        new_board = board.copy()
        new_board[zero_index], new_board[zero_index - 3] = new_board[zero_index - 3], new_board[zero_index]
        moves.append(new_board)
    if zero_index % 3 != 2:
        new_board = board.copy()
        new_board[zero_index], new_board[zero_index + 1] = new_board[zero_index + 1], new_board[zero_index]
        moves.append(new_board)
    if zero_index < 6:
        new_board = board.copy()
        new_board[zero_index], new_board[zero_index + 3] = new_board[zero_index + 3], new_board[zero_index]
        moves.append(new_board)
    # LEFT
    if zero_index % 3 != 0:
        new_board = board.copy()
        new_board[zero_index], new_board[zero_index - 1] = new_board[zero_index - 1], new_board[zero_index]
        moves.append(new_board)

    return moves

def generate_random_solvable_board(steps=20):
    """
    بتبدأ من الحل، وتتحرك حركات عشوائية عشان تلخبط اللوحة
    """
    current = goal_state.copy()
    for _ in range(steps):
        possible_moves = get_moves(current)
        current = random.choice(possible_moves)
    return current

def solve_imperative_with_path(start, goal):

    if start == goal:
        return [start]

    queue = [ (start, [start]) ] 
    visited = set()
    visited.add(tuple(start)) 

    print("Thinking...") 

    while len(queue) > 0:
        if len(queue) > 50000:
            return None 

        current_data = queue.pop(0)
        current_board = current_data[0]
        current_path  = current_data[1]

        if current_board == goal:
            print(f"Solved in {len(current_path)-1} moves")
            return current_path

        possible_moves = get_moves(current_board)

        for move in possible_moves:
            
            move_tuple = tuple(move)
            if move_tuple not in visited:
                new_path = current_path + [move] 
                queue.append((move, new_path))
                visited.add(move_tuple)

    return None

class EightPuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle (Guaranteed Solvable)")
        
        self.current_state = goal_state.copy()
        self.buttons = []
        
        self.create_widgets()
        self.update_display(self.current_state)

    def create_widgets(self):
        # Grid
        frame_grid = tk.Frame(self.root, bg='#333')
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

        shuffle_btn = tk.Button(frame_controls, text="Randomize (Shuffle)", 
                              bg='#FF9800', fg='white', font=('Arial', 12),
                              command=self.shuffle_board)
        shuffle_btn.pack(side=tk.LEFT, padx=5)

        solve_btn = tk.Button(frame_controls, text="Solve!", 
                              bg='#2196F3', fg='white', font=('Arial', 12),
                              command=self.start_solving_animation)
        solve_btn.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(self.root, text="Click Randomize to start.", font=('Arial', 10), fg="blue")
        self.status_label.pack(pady=5)

    def update_display(self, board):
        for i in range(9):
            r = i // 3
            c = i % 3
            val = board[i]
            if val == 0:
                self.buttons[r][c].config(text="", bg="#ddd")
            else:
                self.buttons[r][c].config(text=str(val), bg="white")
        self.root.update()

    def shuffle_board(self):
        self.status_label.config(text="Shuffling...", fg="orange")
        self.root.update()
        self.current_state = generate_random_solvable_board(steps=15) 
        self.update_display(self.current_state)
        self.status_label.config(text="Board Shuffled. Ready to Solve.", fg="blue")

    def start_solving_animation(self):
        self.status_label.config(text="Calculating...", fg="orange")
        self.root.update()

        path = solve_imperative_with_path(self.current_state, goal_state)

        if path:
            self.status_label.config(text=f"Solving... ({len(path)-1} moves)", fg="green")
            for step_board in path:
                self.current_state = step_board
                self.update_display(step_board)
                time.sleep(0.3) 
            
            messagebox.showinfo("Done", "Puzzle Solved!")
            self.status_label.config(text="Solved!", fg="green")
        else:
            self.status_label.config(text="Too difficult or timed out.", fg="red")
            messagebox.showerror("Error", "Could not find solution in reasonable time.")

if __name__ == "__main__":
    root = tk.Tk()
    gui = EightPuzzleGUI(root)
    root.resizable(False, False)
    root.mainloop()