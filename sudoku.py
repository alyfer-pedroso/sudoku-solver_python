import tkinter as tk
import random, os
from tkinter import messagebox

def create_sudoku(self):
    # Gets sudoku grid size
    try:
        self.size = int(self.size_var.get())
    except ValueError:
        messagebox.showerror("Cuidado!", "O tamanho da grade deve ser um número inteiro.")
        return 
    
    # Clears any previous sudoku game
    for widget in self.grid_frame.winfo_children():
        widget.destroy()

    
    self.entries = [] # Array with sudoku's row and within them the cells
    self.solutioned_sudoku = []
    self.sudoku = generate_sudoku(self, self.size) # Generates the grid

    # Check for invalid sudoku size and whether console mode is on
    if self.invalid or self.console:
        return

    for i in range(self.size):
        row_entries = []
        for j in range(self.size):
            value = self.sudoku[i][j]
            
            # Creating grid's cell
            entry = tk.Entry(self.grid_frame, width=4, justify="center", font=("Arial", 14), relief="solid", bd=1, background="white")
            entry.grid(row=i, column=j, padx=0, pady=0, ipady=8)
            
            # Cell event selection
            entry.bind("<FocusIn>", lambda e, row=i, col=j: self.on_entry_focus(row, col))
            entry.bind("<FocusOut>", lambda e: self.restore_colors())
            entry.bind("<KeyRelease>", lambda e, entry=entry: self.validate_entry(entry))

            if value != 0:
                entry.insert(0, str(value))
                entry.config(state="disabled", disabledbackground="white", disabledforeground="black", cursor="arrow")
            # Adds the cell to the row
            row_entries.append(entry)
        # Adds the row to the grid
        self.entries.append(row_entries)
    
def generate_sudoku(self, size):
    self.solutioned = False
    self.invalid = False

    # Tests whether the grid size is a perfect square
    base = int(size ** 0.5)
    if base ** 2 != size:
        messagebox.showerror("Error", "O tamanho da grade deve ser um quadrado perfeito.")
        self.invalid = True
        return [[0] * size for _ in range(size)]

    def pattern(r, c):
        return (base * (r % base) + r // base + c) % size

    def shuffle(s):
        return random.sample(s, len(s))

    rows = [g * base + r for g in shuffle(range(base)) for r in shuffle(range(base))]
    cols = [g * base + c for g in shuffle(range(base)) for c in shuffle(range(base))]
    nums = shuffle(range(1, size + 1))

    board = [[nums[pattern(r, c)] for c in cols] for r in rows]
    self.solutioned_sudoku = [[nums[pattern(r, c)] for c in cols] for r in rows]

    if self.console:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
            
        print("[")
        for i in range(size):
            space = i != size - 1 and "," or ""
            print("  " + str(board[i]) + space)
        print("]")

    squares = size * size
    empties = squares * 3 // 4

    for p in random.sample(range(squares), empties):
        board[p // size][p % size] = 0

    return board

def validate_sudoku(self):
    if self.invalid:
        messagebox.showerror("Error", "Sudoku inválido.")
        return
    board = self.get_board_from_entries()
    if is_valid_sudoku(self, board):
        messagebox.showinfo("Validação", "Sudoku é válido.")
    else:
        messagebox.showerror("Validação", "Sudoku inválido.")

def solve_sudoku(self):
    if self.solutioned:
        return
    
    if self.invalid:
        messagebox.showerror("Error", "Sudoku inválido.")
        return
    
    board = self.memorized_solution and self.solutioned_sudoku or self.get_board_from_entries()
    if solve(self, board):
        self.update_entries(board)
        self.solutioned = True
    else:
        messagebox.showerror("Error", "Sudoku não pode ser solucionado.")

def solve(self, board):
    size = len(board)
    empty = self.find_empty(board)
    if not empty:
        return True
    row, col = empty

    for num in range(1, size + 1):
        if self.is_safe(board, row, col, num):
            board[row][col] = num
            if solve(self, board):
                return True
            board[row][col] = 0
    return False

def is_valid_sudoku(self, board):
    size = len(board)
    base = int(size ** 0.5)

    def is_valid_unit(unit):
        unit = [i for i in unit if i != 0]
        return len(unit) == len(set(unit))

    for i in range(size):
        if not is_valid_unit([board[i][j] for j in range(size)]) or not is_valid_unit([board[j][i] for j in range(size)]):
            return False

    for i in range(0, size, base):
        for j in range(0, size, base):
            if not is_valid_unit([board[r][c] for r in range(i, i + base) for c in range(j, j + base)]):
                return False

    return True