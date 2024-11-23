import tkinter as tk
import gui

# This is the project root script 
if __name__ == "__main__":
    root = tk.Tk()
    gui = gui.SudokuGUI(root)
    root.mainloop()