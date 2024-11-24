# main.py

import tkinter as tk
from gui import set_gui

def main():
    print("Begin Program...")

    # GUI base setup
    root = tk.Tk()
    root.title("Sound Wave Analysis")
    root.geometry("1800x800")

    set_gui(root)
    root.mainloop()

if __name__ == "__main__":
    main()