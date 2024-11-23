import unittest
import tkinter as tk
import json
import os
from solution_validator import validate_solution
from colorama import init, Fore, Style

class TestSudokuValidator(unittest.TestCase):
    """
    Unit test class for validating Sudoku solutions using the validate_solution function.

    This class sets up a testing environment for the Sudoku GUI, loads test cases from a JSON file,
    and verifies that each Sudoku solution is correct using assert statements.
    """

    def setUp(self):
        """Set up a basic Sudoku GUI frame for testing."""
        init(convert=True)
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root)
        self.frame.entries = self.create_test_entries() 
        self.load_sudoku_solutions()

    def create_test_entries(self):
        """
        Create a 9x9 grid of tkinter Entry widgets for testing.

        Returns:
            list: A 2D list of tkinter Entry widgets.
        """
        entries = []
        for _ in range(9):
            row_entries = []
            for _ in range(9):
                entry = tk.Entry(self.frame)
                row_entries.append(entry)
            entries.append(row_entries)
        return entries

    def load_sudoku_solutions(self):
        """
        Load Sudoku solutions from a JSON file.

        This method reads a JSON file named 'sudoku_solutions.json' and stores the test cases
        in an instance variable.
        """
        with open('sudoku_solutions.json') as f:
            self.tests = json.load(f)['tests']

    def test_sudoku_solutions(self):
        """
        Test all Sudoku solutions from the JSON file.

        This method iterates through each test case and verifies the Sudoku solution using the
        validate_solution function. It asserts the result against the expected validity.
        """
        for test in self.tests:
            label = test['label']
            solution = test['solution']
            expected_validity = test['valid']

            Style.RESET_ALL
            print(f"Testes iniciados para {Fore.CYAN}'{label}'{Style.RESET_ALL} (Esperado: {Fore.CYAN}{expected_validity and 'Valido' or 'Invalido'}{Style.RESET_ALL})")

            self.fill_entries(solution)
            # Usar uma estrutura de Mock para simular o Frame
            mock_frame = self.create_mock_frame(solution)
            result = validate_solution(mock_frame)

            self.assertEqual(result, expected_validity, f"{Fore.RED}Falha no teste: {Fore.CYAN}'{label}'{Fore.RED}. Esperado: {expected_validity}, Obtido: {result}\n")
            print(f"{Fore.GREEN}Após assertEqual {Fore.CYAN}'{label}'{Fore.GREEN} teve o resultado: {Fore.CYAN}{'Valido' if result else 'Invalido'}{Style.RESET_ALL}\n")

    def fill_entries(self, solution):
        """
        Fill the Entry widgets with the given Sudoku solution.

        Args:
            solution (list): A 2D list representing the Sudoku solution.
        """
        for i in range(9):
            for j in range(9):
                self.frame.entries[i][j].insert(0, str(solution[i][j]))

    def create_mock_frame(self, solution):
        """
        Create a mock frame to simulate the Sudoku grid.

        This method creates a mock version of the tkinter Frame that contains Entry widgets,
        allowing for testing without a GUI.

        Args:
            solution (list): A 2D list representing the Sudoku solution.

        Returns:
            MockFrame: A mock frame containing the Sudoku entries.
        """
        class MockFrame:
            def __init__(self, board):
                self.entries = [[MockEntry(value) for value in row] for row in board]

        class MockEntry:
            def __init__(self, value):
                self.value = value
                
            def get(self):
                return self.value

        return MockFrame(solution)

    def tearDown(self):
        """Clean up the tkinter instance."""
        self.root.destroy()

if __name__ == "__main__":
    os.system('cls')
    unittest.main()
