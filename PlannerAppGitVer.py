import sqlite3
import tkinter as tk

from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

DB_FILE = "planner.db"

STATUSES = (
    "TBD",
    "WIP",
    "Awaiting",
    "Done"
)

class PlannerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Task Planner")
        self.geometry("1100x700")
        self.minsize(900, 600)

        self.conn = sqlite3.connect(DB_FILE)
        self.conn.row_factory = sqlite3.Row

        self.create_tables()

        self.selected_task_id = None

        self.build_interface()
        self.load_tasks()

        self.protocol("WM_DELETE_WINDOW", self.close_app)

    def create_tables(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                deadline TEXT,
                dependency TEXT,
                created_at TEXT NOT NULL
            )
            """
        )

        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS steps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'TBD',
            dependency TEXT,
            position INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
            )
            """
        )

        self.conn.commit()

    def build_interface(self):
        main_panel = ttk.Panedwindow(
            self,
            orient=tk.HORIZONTAL
        )

        main_panel.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=10
        )

        task_frame = ttk.Frame(
            main_panel,
            padding=10
        )

        step_frame = ttk.Frame(
            main_panel,
            padding=10
        )

        main_panel.add(task_frame, weight=1)
        main_panel.add(step_frame, weight=2)

        self.build_task_section(task_frame)
        self.build_step_section(step_frame)

    def build_task_section(self, task_frame):
        title_label = ttk.Label(
            task_frame,
            text="Tasks",
            font=("TkDefaultFont", 16, "bold")
        )

        title_label.pack(
            anchor="w",
            pady=(0,10)
        )

        task_form = ttk.LabelFrame(
            task_frame,
            text="Add a task",
            padding=10
        )

        task_form.pack(
            fill=tk.X,
            pady=(0, 10)
        )

        task_name_label = ttk.Label(
            task_form,
            text="Task name"
        )

        task_name_label.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w"
        )

        self.task_title_var = tk.StringVar()

        task_name_entry = ttk.Entry(
            task_form,
            textvariable=self.task_title_var
        )

        task_name_entry.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(2, 8)
        )

        deadline_label = ttk.Label(
            task_form,
            text="Deadline (optional, YYYY-MM-DD)"
        )

        deadline_label.grid(
            row=2,
            column=0,
            sticky="w"
        )

        self.task_deadline_var = tk.StringVar()

        deadline_entry = ttk.Entry(
            task_form,
            textvariable=self.task_deadline_var
        )

        deadline_entry.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=(2, 8),
            padx=(0, 5)
        )

        dependency_label = ttk.Label(
            task_form,
            text="Dependent on (optional)"
        )

        dependency_label.grid(
            row=2,
            column=1,
            sticky="w"
        )

        self.task_dependency_var = tk.StringVar()

        dependency_entry = ttk.Entry(
            task_form,
            textvariable=self.task_dependency_var
        )

        dependency_entry.grid(
            row=3,
            column=1,
            sticky="ew",
            pady=(2, 8),
            padx=(5, 0)
        )



        add_task_button = ttk.Button(
            task_form,
            text="Add task",
            command=self.add_task
        )

        add_task_button.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        task_form.columnconfigure(0, weight=1)
        task_form.columnconfigure(1, weight=1)




        task_columns = (
            "title",
            "deadline",
            "dependency"
        )

        self.task_tree = ttk.Treeview(
            task_frame,
            columns=task_columns,
            show="headings",
            selectmode="browse"
        )

        self.task_tree.heading(
            "title",
            text="Task"
        )

        self.task_tree.heading(
            "deadline",
            text="Deadline"
        )

        self.task_tree.heading(
            "dependency",
            text="Dependent on"
        )

        self.task_tree.column(
            "title",
            width=220
        )

        self.task_tree.column(
            "deadline",
            width=100,
            anchor="center"
        )

        self.task_tree.column(
            "dependency",
            width=140
        )





        task_scrollbar = ttk.Scrollbar(
            task_frame,
            orient=tk.VERTICAL,
            command=self.task_tree.yview
        )

        self.task_tree.configure(
            yscrollcommand=task_scrollbar.set
        )

        self.task_tree.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        task_scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

        self.task_tree.bind(
            "<<TreeviewSelect>>",
            self.on_task_selected
        )




        task_button_frame = ttk.Frame(task_frame)

        task_button_frame.pack(
            fill=tk.X,
            pady=(10, 0)
        )

        delete_task_button = ttk.Button(
            task_button_frame,
            text="Delete selected task",
            command=self.delete_task
        )

        delete_task_button.pack(
            side=tk.LEFT
        )




    def build_step_section(self, step_frame):

        self.step_title_label = ttk.Label(
            step_frame,
            text="Select a task to view its steps",
            font=("TkDefaultFont", 16, "bold")
        )

        self.step_title_label.pack(
            anchor="w",
            pady=(0, 10)
        )

        step_form = ttk.LabelFrame(
            step_frame,
            text="Add a step",
            padding=10
        )

        step_form.pack(
            fill=tk.X,
            pady=(0, 10)
        )




        step_description_label = ttk.Label(
            step_form,
            text="Step description"
        )

        step_description_label.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w"
        )

        self.step_description_var = tk.StringVar()

        step_description_entry = ttk.Entry(
            step_form,
            textvariable=self.step_description_var
        )

        step_description_entry.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(2, 8)
        )




        status_label = ttk.Label(
            step_form,
            text="Status"
        )

        status_label.grid(
            row=2,
            column=0,
            sticky="w"
        )

        self.step_status_var = tk.StringVar(
            value="TBD"
        )

        status_dropdown = ttk.Combobox(
            step_form,
            textvariable=self.step_status_var,
            values=STATUSES,
            state="readonly"
        )

        status_dropdown.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=(2, 8),
            padx=(0, 5)
        )






        step_dependency_label = ttk.Label(
            step_form,
            text="Dependent on (optional)"
        )

        step_dependency_label.grid(
            row=2,
            column=1,
            sticky="w"
        )

        self.step_dependency_var = tk.StringVar()

        step_dependency_entry = ttk.Entry(
            step_form,
            textvariable=self.step_dependency_var
        )

        step_dependency_entry.grid(
            row=3,
            column=1,
            sticky="ew",
            pady=(2, 8),
            padx=(5, 0)
        )





        add_step_button = ttk.Button(
            step_form,
            text="Add step",
            command=self.add_step
        )

        add_step_button.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        step_form.columnconfigure(0, weight=1)
        step_form.columnconfigure(1, weight=1)





        step_columns = (
            "description",
            "status",
            "dependency"
        )

        self.step_tree = ttk.Treeview(
            step_frame,
            columns=step_columns,
            show="headings",
            selectmode="browse"
        )

        self.step_tree.heading(
            "description",
            text="Step"
        )

        self.step_tree.heading(
            "status",
            text="Status"
        )

        self.step_tree.heading(
            "dependency",
            text="Dependent on"
        )

        self.step_tree.column(
            "description",
            width=420
        )

        self.step_tree.column(
            "status",
            width=100,
            anchor="center"
        )

        self.step_tree.column(
            "dependency",
            width=160
        )






        step_scrollbar = ttk.Scrollbar(
            step_frame,
            orient=tk.VERTICAL,
            command=self.step_tree.yview
        )

        self.step_tree.configure(
            yscrollcommand=step_scrollbar.set
        )

        self.step_tree.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        step_scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

        self.step_tree.bind(
            "<<TreeviewSelect>>",
            self.on_step_selected
        )





        step_button_frame = ttk.Frame(step_frame)

        step_button_frame.pack(
            fill=tk.X,
            pady=(10, 0)
        )

        status_change_label = ttk.Label(
            step_button_frame,
            text="Change selected step status:"
        )

        status_change_label.pack(
            side=tk.LEFT
        )

        self.selected_status_var = tk.StringVar(
            value="TBD"
        )

        selected_status_dropdown = ttk.Combobox(
            step_button_frame,
            textvariable=self.selected_status_var,
            values=STATUSES,
            state="readonly",
            width=12
        )

        selected_status_dropdown.pack(
            side= tk.LEFT,
            padx=5
        )

        update_status_button = ttk.Button(
            step_button_frame,
            text="Update status",
            command=self.update_step_status
        )

        update_status_button.pack(
            side= tk.LEFT
        )

        delete_step_button = ttk.Button(
            step_button_frame,
            text="Delete step",
            command=self.delete_step
        )

        delete_step_button.pack(
            side= tk.RIGHT
        )




    def validate_deadline(self, deadline):
        if deadline == "":
            return True
        try:
            datetime.strptime(
                deadline,
                "%Y-%m-%d"
            )

            return True
        except ValueError:
            return False






    def add_task(self):
        title = self.task_title_var.get().strip()
        deadline = self.task_deadline_var.get().strip()
        dependency = self.task_dependency_var.get().strip()

        if title == "":
            messagebox.showwarning(
                "Missing task name",
                "Please enter a task name."
            )

            return

        if not self.validate_deadline(deadline):
            messagebox.showwarning(
                "Invalid deadline",
                "Please use YYYY-MM-DD, for example 2026-08-15"
            )

            return

        self.conn.execute(
            """
            INSERT INTO tasks(
                title,
                deadline,
                dependency,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                title,
                deadline if deadline else None,
                dependency if dependency else None,
                datetime.now().isoformat(timespec="seconds")
            )
        )

        self.conn.commit()

        self.task_title_var.set("")
        self.task_deadline_var.set("")
        self.task_dependency_var.set("")

        self.load_tasks()





    def load_tasks(self):
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        tasks = self.conn.execute(
            """
            SELECT
                id,
                title,
                deadline,
                dependency
            FROM tasks
            ORDER BY
                CASE
                    WHEN deadline IS NULL
                    OR deadline = ''
                    THEN 1
                    ELSE 0
                END,
                deadline,
                id DESC
            """
        ).fetchall()

        for task in tasks:
            self.task_tree.insert(
                "",
                tk.END,
                iid=str(task["id"]),
                values=(
                    task["title"],
                    task["deadline"] or "",
                    task["dependency"] or ""
                )
            )






    def on_task_selected(self, event=None):
        selected_items = self.task_tree.selection()

        if not selected_items:
            return

        self.selected_task_id = int(
            selected_items[0]
        )

        task = self.conn.execute(
            """
            SELECT title
            FROM tasks
            WHERE id = ?
            """,
            (self.selected_task_id,)
        ).fetchone()

        if task:
            self.step_title_label.config(
                text=f"Steps for: {task['title']}"
            )

            self.load_steps()





    def add_step(self):
        if self.selected_task_id is None:

            messagebox.showwarning(
                "No task selected",
                "Please select a task before adding a step."
            )

            return

        description = self.step_description_var.get().strip()
        status = self.step_status_var.get()
        dependency = self.step_dependency_var.get().strip()

        if description == "":

            messagebox.showwarning(
                "Missing step description",
                "Please enter a description for the step."
            )

            return
        result = self.conn.execute(
            """
            SELECT COALESCE(MAX(position), 0) + 1
            FROM steps
            WHERE task_id = ?
            """,
            (self.selected_task_id,)
        ).fetchone()

        next_position = result[0]

        self.conn.execute(
            """
            INSERT INTO steps (
                task_id,
                description,
                status,
                dependency,
                position
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                self.selected_task_id,
                description,
                status,
                dependency if dependency else None,
                next_position
            )
        )

        self.conn.commit()

        self.step_description_var.set("")
        self.step_status_var.set("TBD")
        self.step_dependency_var.set("")

        self.load_steps()


    def load_steps(self):
        for item in self.step_tree.get_children():
            self.step_tree.delete(item)

        if self.selected_task_id is None:
            return

        steps = self.conn.execute(
            """
            SELECT
                id,
                description,
                status,
                dependency
            FROM steps
            WHERE task_id = ?
            ORDER BY
                position,
                id
            """,
            (self.selected_task_id, )
        ).fetchall()

        for step in steps:
            self.step_tree.insert(
                "",
                tk.END,
                iid=str(step["id"]),
                values=(
                    step["description"],
                    step["status"],
                    step["dependency"] or ""
                )
            )





    #Detect when a step is selected
    def on_step_selected(self, event=None):
        selected_items = self.step_tree.selection()

        if not selected_items:
            return

        selected_step = selected_items[0]

        values = self.step_tree.item(
            selected_step,
            "values"
        )

        if values:
            self.selected_status_var.set(
                values[1]
            )






    #Update a step's status
    def update_step_status(self):
        selected_items = self.step_tree.selection()

        if not selected_items:
            messagebox.showwarning(
                "No step selected",
                "Please select a step first."
            )

            return

        step_id = int(
            selected_items[0]
        )

        new_status = self.selected_status_var.get()

        self.conn.execute(
            """
            UPDATE steps
            SET status = ?
            WHERE id = ?
            """,
            (
                new_status,
                step_id
            )
        )

        self.conn.commit()

        self.load_steps()







    #Delete a task
    def delete_task(self):
        selected_items = self.task_tree.selection()

        if not selected_items:

            messagebox.showwarning(
                "No task selected",
                "Please select a task to delete."
            )

            return

        task_id = int(
            selected_items[0]
        )

        task_values = self.task_tree.item(
            selected_items[0],
            "values"
        )

        task_title = task_values[0]

        should_delete = messagebox.askyesno(
            "Delete task",
            f'Delete "{task_title}" and all of its steps?'
        )

        if not should_delete:
            return

        self.conn.execute(
            """
            DELETE FROM steps
            WHERE task_id = ?
            """,
            (task_id,)
        )

        self.conn.execute(
            """
            DELETE FROM tasks
            WHERE id = ?
            """,
            (task_id,)
        )

        self.conn.commit()

        self.selected_task_id = None

        self.step_title_label.config(
            text="Select a task to view its steps"
        )

        self.load_tasks()
        self.load_steps()







    #Delete a step
    def delete_step(self):
        selected_items = self.step_tree.selection()

        if not selected_items:
            messagebox.showwarning(
                "No step selected",
                "Please select a step to delete."
            )

            return

        step_id = int(
            selected_items[0]
        )

        step_values = self.step_tree.item(
            selected_items[0],
            "values"
        )

        step_description = step_values[0]

        should_delete = messagebox.askyesno(
            "Delete step",
            f'Delete the step "{step_description}"?'
        )

        if not should_delete:
            return

        self.conn.execute(
            """
            DELETE FROM steps
            WHERE id = ?
            """,
            (step_id,)
        )

        self.conn.commit()

        self.load_steps()





    #Closing the database
    def close_app(self):
        self.conn.close()
        self.destroy()








#Start the program
if __name__ == "__main__":
    app = PlannerApp()
    app.mainloop()