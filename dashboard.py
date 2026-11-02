
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from papers import add_paper, get_papers, update_paper, delete_paper

BG = "#FFFFFF"
TEXT = "#111111"
MUTED = "#666666"
BORDER = "#E0E0E0"
BLACK = "#111111"
WHITE = "#FFFFFF"


def show_dashboard(root, user, on_logout):
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg=BG)
    user_id = user["user_id"]
    all_papers = []

    topbar = tk.Frame(root, bg=WHITE,
                      highlightbackground=BORDER,
                      highlightthickness=1)
    topbar.pack(fill="x")

    tk.Label(topbar, text="ResearchVault", bg=WHITE, fg=TEXT,
             font=("Segoe UI", 17, "bold")).pack(
                 side="left", padx=28, pady=18)

    tk.Button(topbar, text="Log out", command=on_logout,
              bg=BLACK, fg=WHITE, relief="flat",
              cursor="hand2", font=("Segoe UI", 10, "bold"),
              padx=18, pady=8).pack(
                  side="right", padx=28, pady=12)

    content = tk.Frame(root, bg=BG, padx=30, pady=20)
    content.pack(fill="both", expand=True)

    tk.Label(content, text=f"Welcome, {user['full_name']}",
             bg=BG, fg=TEXT,
             font=("Segoe UI", 23, "bold")).pack(anchor="w")

    tk.Label(content,
             text="Your research workspace, all in one place.",
             bg=BG, fg=MUTED,
             font=("Segoe UI", 11)).pack(
                 anchor="w", pady=(4, 15))

    summary = tk.Frame(content, bg=BG)
    summary.pack(fill="x", pady=(0, 15))

    total_var = tk.StringVar(value="Total papers: 0")
    completed_var = tk.StringVar(value="Completed: 0")

    for var in (total_var, completed_var):
        tk.Label(summary, textvariable=var, bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 10, "bold"),
                 padx=15, pady=10,
                 highlightbackground=BORDER,
                 highlightthickness=1).pack(
                     side="left", padx=(0, 10))

    # Add paper form
    form = tk.LabelFrame(content, text=" Add a Research Paper ",
                         bg=WHITE, fg=TEXT,
                         font=("Segoe UI", 11, "bold"),
                         padx=12, pady=8)
    form.pack(fill="x", pady=(0, 12))

    fields = tk.Frame(form, bg=WHITE)
    fields.pack(fill="x")

    entries = {}

    def add_field(label, key, row, col):
        cell = tk.Frame(fields, bg=WHITE)
        cell.grid(row=row, column=col, padx=7, pady=4, sticky="ew")

        tk.Label(cell, text=label, bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 9)).pack(anchor="w")

        entry = tk.Entry(cell, font=("Segoe UI", 10), relief="solid", bd=1)
        entry.pack(fill="x", ipady=4)
        entries[key] = entry

    fields.columnconfigure(0, weight=1)
    fields.columnconfigure(1, weight=1)

    add_field("Paper title *", "title", 0, 0)
    add_field("Authors", "authors", 0, 1)
    add_field("Publication year", "year", 1, 0)
    add_field("Topic", "topic", 1, 1)
    add_field("Research URL", "url", 2, 0)
    add_field("Abstract", "abstract", 2, 1)

    status_row = tk.Frame(form, bg=WHITE)
    status_row.pack(fill="x", padx=7, pady=4)

    tk.Label(status_row, text="Reading status", bg=WHITE, fg=TEXT,
             font=("Segoe UI", 9)).pack(side="left", padx=(0, 10))

    status_var = tk.StringVar(value="To Read")
    ttk.Combobox(status_row, textvariable=status_var,
                 values=["To Read", "Reading", "Completed"],
                 state="readonly", width=15).pack(side="left")

    # Search
    search_row = tk.Frame(content, bg=BG)
    search_row.pack(fill="x", pady=(0, 8))

    tk.Label(search_row, text="Research Library",
             bg=BG, fg=TEXT,
             font=("Segoe UI", 13, "bold")).pack(side="left")

    search_var = tk.StringVar()

    search_entry = tk.Entry(search_row, textvariable=search_var,
                            font=("Segoe UI", 10), width=28,
                            relief="solid", bd=1)
    search_entry.pack(side="right", ipady=5)

    tk.Label(search_row, text="Search title / author / topic",
             bg=BG, fg=MUTED,
             font=("Segoe UI", 9)).pack(side="right", padx=8)

    # Library table
    library = tk.Frame(content, bg=WHITE,
                       highlightbackground=BORDER,
                       highlightthickness=1)
    library.pack(fill="both", expand=True)

    columns = ("id", "title", "authors", "year", "topic", "status")
    table = ttk.Treeview(library, columns=columns,
                         show="headings", height=7)

    headings = {
        "id": ("ID", 40),
        "title": ("Title", 230),
        "authors": ("Authors", 140),
        "year": ("Year", 60),
        "topic": ("Topic", 120),
        "status": ("Reading Status", 110)
    }

    for key, (heading, width) in headings.items():
        table.heading(key, text=heading)
        table.column(key, width=width, anchor="w")

    scrollbar = ttk.Scrollbar(library, orient="vertical",
                              command=table.yview)
    table.configure(yscrollcommand=scrollbar.set)
    table.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def render_table():
        query = search_var.get().strip().lower()

        for item in table.get_children():
            table.delete(item)

        for paper in all_papers:
            searchable = " ".join(str(paper.get(key) or "")
                                  for key in (
                                      "title", "authors", "topic"))
            if query and query not in searchable.lower():
                continue

            table.insert("", "end", iid=str(paper["paper_id"]),
                         values=(
                             paper["paper_id"],
                             paper["title"],
                             paper["authors"] or "",
                             paper["publication_year"] or "",
                             paper["topic"] or "",
                             paper["reading_status"]
                         ))

    def refresh_papers():
        nonlocal all_papers

        try:
            all_papers = get_papers(user_id)
            total_var.set(f"Total papers: {len(all_papers)}")
            completed = sum(
                1 for p in all_papers
                if p["reading_status"] == "Completed"
            )
            completed_var.set(f"Completed: {completed}")
            render_table()
        except Exception as error:
            messagebox.showerror("Database Error", str(error), parent=root)

    def read_year():
        value = entries["year"].get().strip()
        if not value:
            return None
        try:
            year = int(value)
            if not 1000 <= year <= 9999:
                raise ValueError
            return year
        except ValueError:
            messagebox.showwarning(
                "Invalid year", "Enter a valid four-digit year.", parent=root)
            return "INVALID"

    def clear_form():
        for entry in entries.values():
            entry.delete(0, tk.END)
        status_var.set("To Read")

    def save_paper():
        title = entries["title"].get().strip()
        if not title:
            messagebox.showwarning(
                "Missing title", "Enter a paper title.", parent=root)
            return

        year = read_year()
        if year == "INVALID":
            return

        ok, msg = add_paper(
            user_id, title,
            entries["authors"].get().strip(),
            year,
            entries["abstract"].get().strip(),
            entries["url"].get().strip(),
            entries["topic"].get().strip(),
            status_var.get()
        )

        if ok:
            clear_form()
            refresh_papers()
            messagebox.showinfo("Saved", msg, parent=root)
        else:
            messagebox.showerror("Save failed", msg, parent=root)

    def selected_paper():
        selection = table.selection()
        if not selection:
            messagebox.showwarning(
                "Select a paper", "Select a paper from the table first.",
                parent=root)
            return None

        paper_id = int(selection[0])
        return next((p for p in all_papers
                     if p["paper_id"] == paper_id), None)

    def edit_selected():
        paper = selected_paper()
        if paper is None:
            return

        # Editing window
        window = tk.Toplevel(root)
        window.title("Edit Research Paper")
        window.configure(bg=BG)
        window.transient(root)
        window.grab_set()
        window.geometry("520x570")

        edit_entries = {}
        edit_status = tk.StringVar(value=paper["reading_status"])

        edit_form = tk.Frame(window, bg=BG, padx=22, pady=18)
        edit_form.pack(fill="both", expand=True)

        tk.Label(edit_form, text="Edit Research Paper",
                 bg=BG, fg=TEXT,
                 font=("Segoe UI", 17, "bold")).pack(
                     anchor="w", pady=(0, 12))

        values = {
            "title": ("Title *", paper["title"]),
            "authors": ("Authors", paper["authors"] or ""),
            "year": ("Publication year",
                     str(paper["publication_year"] or "")),
            "topic": ("Topic", paper["topic"] or ""),
            "url": ("Research URL", paper["paper_url"] or ""),
            "abstract": ("Abstract", paper["abstract"] or "")
        }

        for key, (label, value) in values.items():
            tk.Label(edit_form, text=label, bg=BG, fg=TEXT,
                     font=("Segoe UI", 9)).pack(anchor="w")

            entry = tk.Entry(edit_form, font=("Segoe UI", 10))
            entry.pack(fill="x", pady=(2, 8), ipady=3)
            entry.insert(0, value)
            edit_entries[key] = entry

        tk.Label(edit_form, text="Reading status",
                 bg=BG, fg=TEXT).pack(anchor="w")

        ttk.Combobox(
            edit_form, textvariable=edit_status,
            values=["To Read", "Reading", "Completed"],
            state="readonly"
        ).pack(fill="x", pady=(3, 12))

        def save_changes():
            title = edit_entries["title"].get().strip()
            if not title:
                messagebox.showwarning(
                    "Missing title", "Enter a paper title.", parent=window)
                return

            year_text = edit_entries["year"].get().strip()
            if year_text:
                try:
                    year = int(year_text)
                    if not 1000 <= year <= 9999:
                        raise ValueError
                except ValueError:
                    messagebox.showwarning(
                        "Invalid year", "Enter a valid four-digit year.",
                        parent=window)
                    return
            else:
                year = None

            ok, msg = update_paper(
                user_id, paper["paper_id"], title,
                edit_entries["authors"].get().strip(),
                year,
                edit_entries["abstract"].get().strip(),
                edit_entries["url"].get().strip(),
                edit_entries["topic"].get().strip(),
                edit_status.get()
            )

            if ok:
                window.destroy()
                refresh_papers()
                messagebox.showinfo("Updated", msg, parent=root)
            else:
                messagebox.showerror("Update failed", msg, parent=window)

        tk.Button(edit_form, text="Save Changes",
                  command=save_changes, bg=BLACK, fg=WHITE,
                  relief="flat", cursor="hand2",
                  padx=16, pady=8).pack(anchor="e")

    def remove_selected():
        paper = selected_paper()
        if paper is None:
            return

        confirm = messagebox.askyesno(
            "Delete Paper",
            f"Delete '{paper['title']}' permanently?",
            parent=root
        )
        if not confirm:
            return

        ok, msg = delete_paper(user_id, paper["paper_id"])

        if ok:
            refresh_papers()
            messagebox.showinfo("Deleted", msg, parent=root)
        else:
            messagebox.showerror("Delete failed", msg, parent=root)

    tk.Button(form, text="Save Research Paper",
              command=save_paper, bg=BLACK, fg=WHITE,
              relief="flat", cursor="hand2",
              font=("Segoe UI", 10, "bold"),
              padx=16, pady=7).pack(anchor="e", pady=(6, 0))

    actions = tk.Frame(content, bg=BG)
    actions.pack(fill="x", pady=(8, 0))

    for label, command in (
        ("Refresh", refresh_papers),
        ("Edit Selected", edit_selected),
        ("Delete Selected", remove_selected)
    ):
        tk.Button(actions, text=label, command=command,
                  bg=WHITE, fg=TEXT,
                  activebackground="#EEEEEE",
                  relief="solid", bd=1, cursor="hand2",
                  font=("Segoe UI", 9, "bold"),
                  padx=13, pady=6).pack(side="left", padx=(0, 8))

    search_var.trace_add("write", lambda *_: render_table())

    refresh_papers()
