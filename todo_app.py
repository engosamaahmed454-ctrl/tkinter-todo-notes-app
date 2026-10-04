"""
To-Do / Notes App
A simple desktop to-do list built with Python's Tkinter library.

Tasks are saved to tasks.json in the same folder, so your list
persists between runs. You can add tasks, mark them done/undone,
and delete them.

Run with: python todo_app.py
"""

import json
import os
import tkinter as tk
from tkinter import messagebox

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")


class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("To-Do List")
        self.geometry("360x480")
        self.configure(bg="#f5f5f5")

        self.tasks = self._load_tasks()

        self._build_input_row()
        self._build_task_list()
        self._refresh_list()

    # ---------- persistence ----------
    def _load_tasks(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return []
        return []

    def _save_tasks(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, indent=2)

    # ---------- UI ----------
    def _build_input_row(self):
        frame = tk.Frame(self, bg="#f5f5f5")
        frame.pack(fill="x", padx=10, pady=10)

        self.entry = tk.Entry(frame, font=("Segoe UI", 12))
        self.entry.pack(side="left", fill="x", expand=True, ipady=6)
        self.entry.bind("<Return>", lambda event: self._add_task())

        add_btn = tk.Button(frame, text="Add", command=self._add_task, bg="#4caf50", fg="white")
        add_btn.pack(side="left", padx=(8, 0))

    def _build_task_list(self):
        self.list_frame = tk.Frame(self, bg="#f5f5f5")
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        for index, task in enumerate(self.tasks):
            row = tk.Frame(self.list_frame, bg="white", bd=1, relief="solid")
            row.pack(fill="x", pady=4)

            text = task["title"]
            done = task["done"]

            check_var = tk.BooleanVar(value=done)
            check = tk.Checkbutton(
                row,
                variable=check_var,
                bg="white",
                command=lambda i=index, v=check_var: self._toggle_task(i, v),
            )
            check.pack(side="left")

            label = tk.Label(
                row,
                text=text,
                bg="white",
                anchor="w",
                font=("Segoe UI", 11, "overstrike" if done else "normal"),
                fg="#888888" if done else "#222222",
            )
            label.pack(side="left", fill="x", expand=True, padx=4, pady=6)

            delete_btn = tk.Button(
                row, text="✕", bg="white", bd=0, fg="#e53935",
                command=lambda i=index: self._delete_task(i),
            )
            delete_btn.pack(side="right", padx=6)

    # ---------- actions ----------
    def _add_task(self):
        title = self.entry.get().strip()
        if not title:
            return
        self.tasks.append({"title": title, "done": False})
        self.entry.delete(0, tk.END)
        self._save_tasks()
        self._refresh_list()

    def _toggle_task(self, index, var):
        self.tasks[index]["done"] = var.get()
        self._save_tasks()
        self._refresh_list()

    def _delete_task(self, index):
        if messagebox.askyesno("Delete task", f"Delete '{self.tasks[index]['title']}'?"):
            del self.tasks[index]
            self._save_tasks()
            self._refresh_list()


if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
