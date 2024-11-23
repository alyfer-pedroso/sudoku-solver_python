import tkinter as tk
import sudoku

# This class defines the GUI
class SudokuGUI:
    # Constructor
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Dinâmico")
        self.root.configure(background="#d4d4d4")
        self.solutioned = False

        # Sets the app to the console mode
        self.console = False
        
        self.size = 9  # initial sudoku size
        self.entries = []  # list of entries fields
        self.sudoku = []  # sudoku board
        self.solutioned_sudoku = []
        self.invalid = False
        self.memorized_solution = True

        self.default_color = "white"
        self.selected_color = "#405dff"  # selected cell color

        # Setting up the GUI
        # top control frame
        control_frame = tk.Frame(root, background="#d4d4d4")
        control_frame.pack(pady=10)

        self.size_label = tk.Label(control_frame, background="#d4d4d4", text="Tamanho da grade:")
        self.size_label.grid(row=0, column=0, padx=5)

        self.size_var = tk.StringVar(value=str(self.size))
        self.size_entry = tk.Entry(control_frame, textvariable=self.size_var, width=5)
        self.size_entry.grid(row=0, column=1, padx=5)

        self.create_grid_button = tk.Button(control_frame, text="Gerar Sudoku", command=lambda: sudoku.create_sudoku(self))
        self.create_grid_button.grid(row=0, column=2, padx=5)

        if not self.console:
            self.memorized_solution_label = tk.Label(control_frame, background="#d4d4d4", text="Solução memorizada:")
            self.memorized_solution_label.grid(row=1, column=0, padx=5)

            self.memorized_solution_button = tk.Button(control_frame, width=10, text=self.memorized_solution and "Ativado" or "Desativado", background=self.memorized_solution and "green" or "red", foreground="white", state=self.solutioned and "disabled" or "normal", command=self.toggle_memorized_solution)
            self.memorized_solution_button.grid(row=1, column=1, padx=5)

            self.validate_button = tk.Button(control_frame, text="Validar Sudoku", command=lambda: sudoku.validate_sudoku(self))
            self.validate_button.grid(row=0, column=3, padx=5)

            self.solve_button = tk.Button(control_frame, text="Solucionar Sudoku", command=lambda: sudoku.solve_sudoku(self))
            self.solve_button.grid(row=0, column=4, padx=5)

        # sudoku grid frame
        self.grid_frame = tk.Frame(root)
        self.grid_frame.pack(pady=10)

        # create initial grid
        if not self.console: sudoku.create_sudoku(self)

    def highlight_related_cells(self, row, col):
        if self.solutioned:
            return
        
        # highlights the row, column and sub-grid of the selected cell, including disabled cells
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

    # Highlights 
    def highlight_entry(self, entry):
        if self.solutioned:
            return

        # highlights a cell, whether it is deactivated or normal
        if entry["state"] == "normal":
            entry.config(background=self.selected_color)
        elif entry["state"] == "disabled":
            entry.config(disabledbackground=self.selected_color)

    def restore_colors(self):
        if self.solutioned:
            return
        
        # restores cell colors to their original state
        for row_entries in self.entries:
            for entry in row_entries:
                if entry["state"] == "normal":
                    entry.config(background=self.default_color)
                elif entry["state"] == "disabled":
                    entry.config(disabledbackground=self.default_color)

    def on_entry_focus(self, row, col):
        if self.solutioned:
            return
        
        # callback when a cell is selected
        self.restore_colors()
        self.highlight_related_cells(row, col)

    def validate_entry(self, entry):
        value = entry.get()
        try:
            int(value)
        except ValueError:
            entry.delete(0, tk.END)

    def get_board_from_entries(self):
        board = []
        for row_entries in self.entries:
            row = []
            for entry in row_entries:
                try:
                    value = int(entry.get())
                except ValueError:
                    value = 0
                    entry.delete(0, tk.END)
                row.append(value)
            board.append(row)
        return board
    
    def toggle_memorized_solution(self):
        if self.solutioned:
            return
        self.memorized_solution = not self.memorized_solution
        self.memorized_solution_button.config(text=self.memorized_solution and "Ativado" or "Desativado", background=self.memorized_solution and "green" or "red", foreground="white", state=self.solutioned and "disabled" or "normal")

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

    def update_entries(self, board):
        size = len(board)
        for row in range(size):
            for col in range(size):
                entry = self.entries[row][col]
                if entry["state"] == "normal":
                    entry.delete(0, tk.END)
                    entry.insert(0, str(board[row][col]))
                    entry.config(state="readonly", readonlybackground="#9ccc75")
                else:
                    entry.config(disabledbackground="#f0f0f0")