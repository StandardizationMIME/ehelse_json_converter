import Tkinter as tk #Probably don't need this
from MainController import *


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = MainController(root)
    root.mainloop()