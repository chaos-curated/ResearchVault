import tkinter as tk
from tkinter import ttk

root = tk.Tk()

root.title("ResearchVault")
root.geometry("900x600")
root.configure(bg="white")

title = tk.Label(
    root,
    text="ResearchVault",
    font=("Arial", 22, "bold"),
    bg="white"
)

title.pack(pady=20)

frame = tk.Frame(root, bg="white")
frame.pack(fill="both", expand=True)

title_entry = tk.Entry(frame)
title_entry.pack(pady=10)

add_button = tk.Button(
    frame,
    text="Add Research Paper"
)
add_button.pack(pady=10)

root.mainloop()


import tkinter as tk
from tkinter import messagebox

def add_paper():
    title = title_entry.get().strip()

    if not title:
        messagebox.showwarning(
            "Warning",
            "Please enter a paper title"
        )
        return

    save_paper(title)

    messagebox.showinfo(
        "Success",
        "Research paper added successfully"
    )

root = tk.Tk()

title_entry = tk.Entry(root)
title_entry.pack()

add_button = tk.Button(
    root,
    text="Add Paper",
    command=add_paper
)
add_button.pack()

root.mainloop()