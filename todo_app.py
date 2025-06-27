import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import json, os, threading, datetime
from plyer import notification

TASK_FILE = "tasks.json"

# — Load & Save —
def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            tasks = json.load(f)
        today = datetime.date.today().isoformat()
        for t in tasks:
            t.setdefault("due_date", today)
        return tasks
    return []

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

class ToDoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("📝 To-Do List")
        self.geometry("480x600")

        # Flag for notification thread
        self.running = True
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Load tasks
        self.tasks = load_tasks()

        # — Themed widgets via ttk —
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TButton", padding=6, font=("Arial", 11))
        style.configure("TEntry", padding=5)
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TCheckbutton", font=("Arial", 11))

        # — Input Frame —
        inp = ttk.Frame(self, padding=10)
        inp.pack(fill="x")
        self.task_var = tk.StringVar()
        ttk.Entry(inp, textvariable=self.task_var, width=25).grid(row=0, column=0, padx=5)

        self.date_entry = DateEntry(inp, width=12, background='darkblue',
                                    foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=0, column=1, padx=5)

        self.priority_var = tk.StringVar(value="Normal")
        ttk.Combobox(inp, textvariable=self.priority_var,
                     values=["Low", "Normal", "High"], width=8).grid(row=0, column=2, padx=5)

        ttk.Button(inp, text="➕ Add Task", command=self.add_task).grid(row=0, column=3, padx=5)

        # — Task List (scrollable) —
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, pady=10, padx=10)
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.list_frame = ttk.Frame(canvas)

        self.list_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.list_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # — Control Buttons —
        ctrl = ttk.Frame(self, padding=10)
        ctrl.pack(fill="x")
        ttk.Button(ctrl, text="✅ Mark Done", command=self.mark_done).pack(side="left", padx=5)
        ttk.Button(ctrl, text="🗑 Delete Done", command=self.delete_done).pack(side="left", padx=5)
        ttk.Button(ctrl, text="🔄 Refresh", command=self.refresh).pack(side="left", padx=5)

        self.check_vars = []
        self.display_tasks()

        # Start notification loop
        self.notify_thread = threading.Thread(target=self.notify_loop, daemon=True)
        self.notify_thread.start()

    def on_close(self):
        # Stop the notification loop and then close
        self.running = False
        self.destroy()

    def notify_loop(self):
        while self.running:
            now = datetime.datetime.now()
            for task in self.tasks:
                if not task.get("done") and "due_date" in task:
                    try:
                        due = datetime.datetime.fromisoformat(task["due_date"])
                    except:
                        continue
                    delta = (due - now).total_seconds()
                    if 0 <= delta <= 3600 and not task.get("notified", False):
                        notification.notify(
                            title="Task Due Soon",
                            message=f"{task['text']} due at {due.strftime('%H:%M')}",
                            timeout=8
                        )
                        task["notified"] = True
            save_tasks(self.tasks)
            # sleep for 5 minutes or until closed
            for _ in range(300):
                if not self.running:
                    break
                time.sleep(1)

    def display_tasks(self):
        # Clear
        for w in self.list_frame.winfo_children():
            w.destroy()
        self.check_vars.clear()

        # Sort by date then priority
        prio_rank = {"High": 0, "Normal": 1, "Low": 2}
        def keyfn(t):
            return (t.get("due_date", ""), prio_rank.get(t.get("priority","Normal"),1))
        self.tasks.sort(key=keyfn)

        # Rebuild
        for i, task in enumerate(self.tasks):
            done = task.get("done", False)
            due = task.get("due_date", "")
            txt = f"{task['text']} [{task['priority']}] — Due: {due}"
            var = tk.BooleanVar(value=done)
            cb = ttk.Checkbutton(self.list_frame, text=txt, variable=var)
            cb.pack(anchor="w", pady=2)
            self.check_vars.append(var)

    def add_task(self):
        text = self.task_var.get().strip()
        if not text:
            messagebox.showwarning("Input Error", "Task cannot be empty.")
            return
        new = {
            "text": text,
            "done": False,
            "priority": self.priority_var.get(),
            "due_date": self.date_entry.get_date().isoformat()
        }
        self.tasks.append(new)
        save_tasks(self.tasks)
        self.task_var.set("")
        self.refresh()

    def mark_done(self):
        for i, var in enumerate(self.check_vars):
            self.tasks[i]["done"] = var.get()
        save_tasks(self.tasks)
        self.refresh()

    def delete_done(self):
        self.tasks = [t for i, t in enumerate(self.tasks) if not self.check_vars[i].get()]
        save_tasks(self.tasks)
        self.refresh()

    def refresh(self):
        self.display_tasks()

if __name__ == "__main__":
    import time  # needed for notify_loop sleep
    # pip install tkcalendar plyer
    app = ToDoApp()
    app.mainloop()
