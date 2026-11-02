
import tkinter as tk
from auth_ui import start_auth


def main():
    root = tk.Tk()
    root.title("ResearchVault")
    root.geometry("1000x650")
    root.minsize(800, 550)
    root.configure(bg="#FFFFFF")

    start_auth(root)
    root.mainloop()


if __name__ == "__main__":
    main()
