import tkinter as tk
import numpy as np

def validate_solution(sudoku_frame: tk.Frame) -> bool:
    """Verifies whether the sudoku game solution was correct."""

    rows = sudoku_frame.winfo_children()

    line = 0, column = 0
    size = len(rows)
    total_cells = pow(len(rows), 2)

    for i in range(0, total_cells + 1):
        
        # Column testing

        # Line testing

        # Subgrid testing

        pass