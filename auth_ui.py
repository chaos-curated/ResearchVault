import tkinter as tk
from tkinter import messagebox

from auth import register_user, login_user
from dashboard import show_dashboard

BG = "#FFFFFF"
TEXT = "#171717"
MUTED = "#737373"
BORDER = "#E5E5E5"
BUTTON = "#171717"


def clear_window(root):
    for widget in root.winfo_children():
        widget.destroy()


def make_label(parent, text, size=11, color=TEXT, bold=False):
    return tk.Label(
        parent,
        text=text,
        bg=BG,
        fg=color,
        font=("Segoe UI", size, "bold" if bold else "normal")
    )


def make_entry(parent, show=None):
    return tk.Entry(
        parent,
        show=show or "",
        bg=BG,
        fg=TEXT,
        insertbackground=TEXT,
        relief="flat",
        font=("Segoe UI", 11),
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=TEXT
    )


def make_button(parent, text, command):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=BUTTON,
        fg="#FFFFFF",
        activebackground="#333333",
        activeforeground="#FFFFFF",
        relief="flat",
        cursor="hand2",
        font=("Segoe UI", 10, "bold"),
        pady=10
    )


def start_auth(root):
    show_login(root)


def show_login(root):
    clear_window(root)

    container = tk.Frame(root, bg=BG)
    container.place(relx=0.5, rely=0.5, anchor="center", width=360)

    make_label(
        container, "ResearchVault", 25, TEXT, True
    ).pack(anchor="w")

    make_label(
        container, "Your personal research library", 10, MUTED
    ).pack(anchor="w", pady=(5, 28))

    make_label(container, "Email address", 10, TEXT, True).pack(
        anchor="w", pady=(0, 7)
    )

    email_entry = make_entry(container)
    email_entry.pack(fill="x", ipady=9, pady=(0, 17))

    make_label(container, "Password", 10, TEXT, True).pack(
        anchor="w", pady=(0, 7)
    )

    password_entry = make_entry(container, "*")
    password_entry.pack(fill="x", ipady=9, pady=(0, 22))

    def login():
        email = email_entry.get()
        password = password_entry.get()

        user, message = login_user(email, password)

        if user:
            show_dashboard(root, user, lambda: show_login(root))
        else:
            messagebox.showerror("Login failed", message)

    make_button(container, "Log in", login).pack(fill="x")

    footer = tk.Frame(container, bg=BG)
    footer.pack(fill="x", pady=(18, 0))

    make_label(footer, "New to ResearchVault?", 10, MUTED).pack(
        side="left"
    )

    tk.Button(
        footer,
        text="Create account",
        command=lambda: show_signup(root),
        bg=BG,
        fg=TEXT,
        activebackground=BG,
        activeforeground=TEXT,
        relief="flat",
        cursor="hand2",
        font=("Segoe UI", 10, "bold")
    ).pack(side="left", padx=(5, 0))

    email_entry.focus_set()
    root.bind("<Return>", lambda event: login())


def show_signup(root):
    clear_window(root)

    container = tk.Frame(root, bg=BG)
    container.place(relx=0.5, rely=0.5, anchor="center", width=360)

    make_label(
        container, "Create your account", 23, TEXT, True
    ).pack(anchor="w")

    make_label(
        container, "Start organizing your research", 10, MUTED
    ).pack(anchor="w", pady=(5, 25))

    make_label(container, "Full name", 10, TEXT, True).pack(
        anchor="w", pady=(0, 7)
    )

    name_entry = make_entry(container)
    name_entry.pack(fill="x", ipady=9, pady=(0, 15))

    make_label(container, "Email address", 10, TEXT, True).pack(
        anchor="w", pady=(0, 7)
    )

    email_entry = make_entry(container)
    email_entry.pack(fill="x", ipady=9, pady=(0, 15))

    make_label(container, "Password (minimum 8 characters)", 10, TEXT, True).pack(
        anchor="w", pady=(0, 7)
    )

    password_entry = make_entry(container, "*")
    password_entry.pack(fill="x", ipady=9, pady=(0, 15))

    make_label(container, "Confirm password", 10, TEXT, True).pack(
        anchor="w", pady=(0, 7)
    )

    confirm_entry = make_entry(container, "*")
    confirm_entry.pack(fill="x", ipady=9, pady=(0, 22))

    def signup():
        name = name_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get()
        confirm = confirm_entry.get()

        if not name or not email or not password or not confirm:
            messagebox.showwarning(
                "Missing information", "Please complete every field."
            )
            return

        if password != confirm:
            messagebox.showerror(
                "Password mismatch", "The passwords do not match."
            )
            return

        success, message = register_user(name, email, password)

        if success:
            messagebox.showinfo("Success", message)
            show_login(root)
        else:
            messagebox.showerror("Registration failed", message)

    make_button(container, "Create account", signup).pack(fill="x")

    tk.Button(
        container,
        text="Back to login",
        command=lambda: show_login(root),
        bg=BG,
        fg=TEXT,
        activebackground=BG,
        activeforeground=TEXT,
        relief="flat",
        cursor="hand2",
        font=("Segoe UI", 10)
    ).pack(anchor="w", pady=(15, 0))

    name_entry.focus_set()
    root.bind("<Return>", lambda event: signup())