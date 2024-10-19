import gc, tkinter as tk

class Gui:
    def __init__(self, root):
        self.root = root
        
        self.size = 9
        self.entries = []
        self.sudoku = []

        self.grid_frame = tk.Frame(root)
        self.grid_frame.pack(padx=10, pady=10)

        self.create_grid_button = tk.Button(self.grid_frame, text="Testar Grid", command=lambda: grid_size_test(self, 50))
        self.create_grid_button.grid(row=0, column=2, padx=5)


def grid_size_test(gui, test_size):
    for i in range(1, test_size + 1):
        # print(i)
        gui.size = i
        results = create_sudoku(gui)
        try:
            print(f"count: {results[0]} | expected: {results[1]}")
            assert results[0] == results[1], 'Grid inválida'
            print('Grid válida!')
        except AssertionError as error:
            print(error)
    print('==== FIM =====')

def create_sudoku(self):
    cont = 0

    expected_total_cells = int(self.size ** 2) 

    for widget in self.grid_frame.winfo_children():
        widget.destroy()

    self.entries = []

    for i in range(self.size):
        row_entries = []
        for j in range(self.size):
            entry = tk.Entry(self.grid_frame)
            entry.grid(row=i, column=j)
            row_entries.append(entry)
            cont += 1
        self.entries.append(row_entries)
    gc.collect()

    return [cont, expected_total_cells]

if __name__ == '__main__':
    root = tk.Tk()
    gui = Gui(root)
    root.mainloop()