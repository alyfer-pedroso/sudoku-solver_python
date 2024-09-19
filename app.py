import tkinter as tk
from tkinter import messagebox
import random

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Dinâmico")
        self.root.configure(background="#d4d4d4")
        self.solutioned = False
        
        self.size = 9  # initial sudoku size
        self.entries = []  # list of entries fields
        self.sudoku = []  # sudoku board
        self.invalid = False

        self.default_color = "white"
        self.selected_color = "#405dff"  # selected cell color
        self.update_delay = 0 # delay in ms

        # top control frame
        control_frame = tk.Frame(root, background="#d4d4d4")
        control_frame.pack(pady=10)

        self.size_label = tk.Label(control_frame, background="#d4d4d4", text="Tamanho da grade:")
        self.size_label.grid(row=0, column=0, padx=5)

        self.size_var = tk.StringVar(value=str(self.size))
        self.size_entry = tk.Entry(control_frame, textvariable=self.size_var, width=5)
        self.size_entry.grid(row=0, column=1, padx=5)

        self.delay_label = tk.Label(control_frame, background="#d4d4d4", text="Delay de resolução (ms):")
        self.delay_label.grid(row=1, column=0, padx=5)

        self.delay_var = tk.StringVar(value=str(self.update_delay))
        self.delay_entry = tk.Entry(control_frame, textvariable=self.delay_var, width=5)
        self.delay_entry.grid(row=1, column=1, padx=5)

        self.create_grid_button = tk.Button(control_frame, text="Gerar Sudoku", command=self.create_sudoku)
        self.create_grid_button.grid(row=0, column=2, padx=5)

        self.validate_button = tk.Button(control_frame, text="Validar Sudoku", command=self.validate_sudoku)
        self.validate_button.grid(row=0, column=3, padx=5)

        self.solve_button = tk.Button(control_frame, text="Solucionar Sudoku", command=self.solve_sudoku)
        self.solve_button.grid(row=0, column=4, padx=5)

        # sudoku grid frame
        self.grid_frame = tk.Frame(root)
        self.grid_frame.pack(pady=10)

        # create initial grid
        self.create_sudoku()

    def create_sudoku(self):
        try:
            self.size = int(self.size_var.get())
        except ValueError:
            messagebox.showerror("Cuidado!", "O tamanho da grade deve ser um número inteiro.")
            return 
        
        # clear last grid
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.entries = []
        self.sudoku = self.generate_sudoku(self.size)

        if self.invalid:
            return

        for i in range(self.size):
            row_entries = []
            for j in range(self.size):
                value = self.sudoku[i][j]
                
                entry = tk.Entry(self.grid_frame, width=4, justify="center", font=("Arial", 14), relief="solid", bd=1, background="white")
                entry.grid(row=i, column=j, padx=0, pady=0, ipady=8)
                
                # cell event selecion
                entry.bind("<FocusIn>", lambda e, row=i, col=j: self.on_entry_focus(row, col))
                entry.bind("<FocusOut>", lambda e: self.restore_colors())

                if value != 0:
                    entry.insert(0, str(value))
                    entry.config(state="disabled", disabledbackground="white", disabledforeground="black", cursor="arrow")
                
                row_entries.append(entry)
            self.entries.append(row_entries)

    def generate_sudoku(self, size):
        self.solutioned = False
        self.invalid = False

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

        squares = size * size
        empties = squares * 3 // 4
        for p in random.sample(range(squares), empties):
            board[p // size][p % size] = 0

        return board

    def highlight_related_cells(self, row, col):
        if self.solutioned:
            return
        
        """ Destaca a linha, coluna e subgrade da célula selecionada, incluindo as desativadas. """
        base = int(self.size ** 0.5)
        
        # highlight row and column
        for i in range(self.size):
            self.highlight_entry(self.entries[row][i])  # row
            self.highlight_entry(self.entries[i][col])  # col
        
        # highlight subgrid
        start_row, start_col = base * (row // base), base * (col // base)
        for i in range(start_row, start_row + base):
            for j in range(start_col, start_col + base):
                self.highlight_entry(self.entries[i][j])

    def highlight_entry(self, entry):
        if self.solutioned:
            return
        
        """ Destaca uma célula, seja ela desativada ou normal. """
        if entry["state"] == "normal":
            entry.config(background=self.selected_color)
        elif entry["state"] == "disabled":
            entry.config(disabledbackground=self.selected_color)

    def restore_colors(self):
        if self.solutioned:
            return
        
        """ Restaura as cores das células para o estado original. """
        for row_entries in self.entries:
            for entry in row_entries:
                if entry["state"] == "normal":
                    entry.config(background=self.default_color)
                elif entry["state"] == "disabled":
                    entry.config(disabledbackground=self.default_color)

    def on_entry_focus(self, row, col):
        if self.solutioned:
            return
        
        """ Callback quando uma célula é selecionada. """
        self.restore_colors()
        self.highlight_related_cells(row, col)

    def validate_sudoku(self):
        if self.invalid:
            messagebox.showerror("Error", "Sudoku inválido.")
            return
        board = self.get_board_from_entries()
        if self.is_valid_sudoku(board):
            messagebox.showinfo("Validação", "Sudoku é válido.")
        else:
            messagebox.showerror("Validação", "Sudoku inválido.")

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

    def get_board_from_entries(self):
        board = []
        for row_entries in self.entries:
            row = []
            for entry in row_entries:
                try:
                    value = int(entry.get())
                except ValueError:
                    value = 0
                row.append(value)
            board.append(row)
        return board

    def solve_sudoku(self):
        if self.solutioned:
            return
        
        if self.invalid:
            messagebox.showerror("Error", "Sudoku inválido.")
            return
        
        board = self.get_board_from_entries()
        if self.solve(board):
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
                if self.solve(board):
                    return True
                board[row][col] = 0
        return False

    def find_empty(self, board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def is_safe(self, board, row, col, num):
        size = len(board)
        base = int(size ** 0.5)

        for i in range(size):
            if board[row][i] == num or board[i][col] == num:
                return False

        start_row, start_col = base * (row // base), base * (col // base)
        for i in range(start_row, start_row + base):
            for j in range(start_col, start_col + base):
                if board[i][j] == num:
                    return False

        return True

    def update_entries_with_delay(self, board, row=0, col=0):
        # refresh cells with delay
        if row >= self.size:
            return
        entry = self.entries[row][col]
        if entry["state"] == "normal":
            entry.delete(0, tk.END)
            entry.insert(0, str(board[row][col]))
            entry.config(state="readonly", readonlybackground="#9ccc75")
        else:
            entry.config(disabledbackground="#f0f0f0")

        # next item
        if col < self.size - 1:
            self.root.after(self.update_delay, self.update_entries_with_delay, board, row, col + 1)
        elif row < self.size - 1:
            self.root.after(self.update_delay, self.update_entries_with_delay, board, row + 1, 0)

    def update_entries(self, board):
        # refresh cells with delay
        self.update_delay = int(self.delay_var.get())
        self.update_entries_with_delay(board)

if __name__ == "__main__":
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()
