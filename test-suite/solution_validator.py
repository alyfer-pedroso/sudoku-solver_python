import tkinter as tk
from colorama import Fore, Style

def validate_solution(sudoku_frame: tk.Frame) -> bool:
    """
    Verifies whether the Sudoku game solution is correct.

    This function checks if each row, column, and 3x3 subgrid (box) in the provided
    Sudoku frame contains unique values from 1 to 9, ensuring the validity of the solution.

    Args:
        sudoku_frame (tk.Frame): A tkinter Frame object that contains the Sudoku grid.

    Returns:
        bool: True if the solution is valid, False otherwise. Prints error messages for
        invalid rows, columns, or boxes.
    """
    
    def is_valid_unit(unit):
        """
        Check if a unit (row, column, or box) is valid.

        A unit is considered valid if it contains no duplicates and all values are 
        integers between 1 and 9.

        Args:
            unit (list): A list of tkinter Entry widgets representing a row, column, or box.

        Returns:
            bool: True if the unit is valid, False otherwise.
        """
        unit = [int(x.get()) for x in unit if x.get() != '']  # Remove empty values
        return len(unit) == len(set(unit))  # Check for duplicates

    # Get all entries from the frame
    rows = sudoku_frame.entries

    # Verify the lines
    for row_index, row in enumerate(rows):
        if not is_valid_unit(row):
            print(f"{Fore.RED}Linha {row_index + 1} inválida!{Style.RESET_ALL}")
            return False

    # Verify the columns
    for col_index in range(9):
        col = [rows[row_index][col_index] for row_index in range(9)]
        if not is_valid_unit(col):
            print(f"{Fore.RED}Coluna {col_index + 1} inválida!{Style.RESET_ALL}")
            return False

    # Verify the subgrids 3x3
    base = 3
    for box_row in range(base):
        for box_col in range(base):
            box = [rows[r][c]
                   for r in range(box_row * base, (box_row + 1) * base)
                   for c in range(box_col * base, (box_col + 1) * base)]
            if not is_valid_unit(box):
                print(f"{Fore.RED}Submatriz ({box_row + 1}, {box_col + 1}) inválida!{Style.RESET_ALL}")
                return False

    return True
