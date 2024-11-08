

import tkinter as tk
from display import Display

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Simulator")
    app = Display(root, 100, 100, 5)
    root.mainloop()