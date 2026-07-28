import sqlite3
import tkinter as tk

from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

DB_FILE = "planner.db"

TASK_STATUSES = (
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
        self.recalculate_all_task_statuses()
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
                status TEXT NOT NULL DEFAULT 'TBD',
                awaiting_confirmed INTEGER NOT NULL DEFAULT 0,
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
                is_done INTEGER NOT NULL DEFAULT 0,
                has_dependency INTEGER NOT NULL DEFAULT 0,
                dependency TEXT,
                position INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (task_id) REFERENCES tasks(id)
            )
            """
        )

        #Upgrade an older tasks table without deleting its contents.
        task_columns = {
            row["name"]
            for row in self.conn.execute(
                "PRAGMA table_info(tasks)"
            ).fetchall()
        }

        if "status" not in task_columns:
            self.conn.execute(
                """
                ALTER TABLE tasks
                ADD COLUMN status TEXT NOT NULL DEFAULT 'TBD'
                """
            )

        if "awaiting_confirmed" not in task_columns:
            self.conn.execute(
                """
                ALTER TABLE tasks
                ADD COLUMN awaiting_confirmed 
                INTEGER NOT NULL DEFAULT 0
                """
            )

        #Upgrade an older steps table
        step_columns = {
            row["name"]
            for row in self.conn.execute(
                "PRAGMA table_info(steps)"
            ).fetchall()
        }

        if "is_done" not in step_columns:
            self.conn.execute(
                """
                ALTER TABLE steps
                ADD COLUMN is_done INTEGER NOT NULL DEFAULT 0
                """
            )

        #Preserve old steps that were already marked as done
        if "status" in step_columns:
            self.conn.execute(
                """
                UPDATE steps
                SET is_done = 1
                WHERE LOWER(status) IN ('done', 'completed')
                """
            )

        if "has_dependency" not in step_columns:
            self.conn.execute(
                """
                ALTER TABLE steps
                ADD COLUMN has_dependency 
                INTEGER NOT NULL DEFAULT 0
                """
            )

        self.conn.execute(
            """
            UPDATE steps
            SET has_dependency = 
                CASE
                    WHEN dependency IS NOT NULL AND TRIM(dependency) != ''
                    THEN 1
                    ELSE 0
                END
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
            "status",
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
            "status",
            text="Status"
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
            "status",
            width=170,
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

        self.complete_awaiting_button = ttk.Button(
            task_button_frame,
            text="Complete awaiting task",
            command=self.complete_awaiting_task
        )

        self.complete_awaiting_button.pack(
            side=tk.RIGHT,
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

        self.step_description_entry = ttk.Entry(
            step_form,
            textvariable=self.step_description_var
        )

        self.step_description_entry.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(2, 8)
        )

        self.new_step_done_var = tk.BooleanVar(value=False)

        new_step_done_checkbox = ttk.Checkbutton(
            step_form,
            text="Done",
            variable=self.new_step_done_var
        )

        new_step_done_checkbox.grid(
            row=2,
            column=0,
            sticky="w",
            pady=(2, 8)
        )

        self.new_step_has_dependency_var = tk.BooleanVar(value=False)

        new_step_dependency_checkbox = ttk.Checkbutton(
            step_form,
            text="Has dependency",
            variable=self.new_step_has_dependency_var,
            command=self.toggle_new_step_dependency
        )

        new_step_dependency_checkbox.grid(
            row=2,
            column=1,
            sticky="w",
            pady=(2, 8)
        )

        step_dependency_label = ttk.Label(
            step_form,
            text="Dependent on "
        )

        step_dependency_label.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="w"
        )

        self.step_dependency_var = tk.StringVar()

        self.step_dependency_entry = ttk.Entry(
            step_form,
            textvariable=self.step_dependency_var,
            state="disabled"
        )

        self.step_dependency_entry.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(2, 8)
        )


        add_step_button = ttk.Button(
            step_form,
            text="Add step",
            command=self.add_step
        )

        add_step_button.grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        step_form.columnconfigure(0, weight=1)
        step_form.columnconfigure(1, weight=1)





        step_columns = (
            "description",
            "done",
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
            "done",
            text="Done"
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
            "done",
            width=70,
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

        self.selected_step_done_var = tk.BooleanVar(value=False)

        selected_done_checkbox = ttk.Checkbutton(
            step_button_frame,
            text="Done",
            variable=self.selected_step_done_var
        )

        selected_done_checkbox.pack(
            side=tk.LEFT
        )

        self.selected_step_has_dependency_var = tk.BooleanVar(value=False)

        selected_dependency_checkbox = ttk.Checkbutton(
            step_button_frame,
            text="Has dependency",
            variable=self.selected_step_has_dependency_var,
            command=self.toggle_selected_step_dependency
        )

        selected_dependency_checkbox.pack(
            side=tk.LEFT,
            padx=(10, 5)
        )

        self.selected_step_dependency_var = tk.StringVar()

        self.selected_step_dependency_entry = ttk.Entry(
            step_button_frame,
            textvariable=self.step_dependency_var,
            state="disabled",
            width=24
        )

        self.selected_step_dependency_entry.pack(
            side=tk.LEFT,
            padx=5
        )

        update_step_button = ttk.Button(
            step_button_frame,
            text="Update step",
            command=self.update_step
        )

        update_step_button.pack(
            side=tk.LEFT,
            padx=5
        )
       
        delete_step_button = ttk.Button(
            step_button_frame,
            text="Delete step",
            command=self.delete_step
        )

        delete_step_button.pack(
            side= tk.RIGHT
        )

    def toggle_new_step_dependency(self):
        if self.new_step_has_dependency_var.get():
            self.step_dependency_entry.config(state="normal")
            self.step_dependency_entry.focus_set()
        else:
            self.step_dependency_var.set("")
            self.step_dependency_entry.config(state="disabled")

    def toggle_selected_step_dependency(self):
        if self.selected_step_has_dependency_var.get():
            self.selected_step_dependency_entry.config(state="normal")
            self.selected_step_dependency_entry.focus_set()
        else:
            self.selected_step_dependency_var.set("")
            self.selected_step_dependency_entry.config(state="disabled")



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

        cursor = self.conn.execute(
            """
            INSERT INTO tasks (
                title,
                deadline,
                dependency,
                status,
                awaiting_confirmed,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                title,
                deadline if deadline else None,
                dependency if dependency else None,
                "TBD",
                0,
                datetime.now().isoformat(timespec="seconds")
            )
        )

        new_task_id = cursor.lastrowid

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
                tasks.id,
                tasks.title,
                tasks.deadline,
                tasks.dependency,
                tasks.status,

                COUNT(steps.id) AS total_steps,

                COALESCE(
                    SUM(
                        CASE
                            WHEN steps.is_done = 1 THEN 1
                            ELSE 0
                        END
                    ),
                    0
                ) AS completed_steps

            FROM tasks

            LEFT JOIN steps
                ON steps.task_id = tasks.id
            
            GROUP BY
                tasks.id,
                tasks.title,
                tasks.deadline,
                tasks.dependency,
                tasks.status
            
            ORDER BY
                CASE
                    WHEN tasks.deadline IS NULL
                        OR tasks.deadline = ''
                    THEN 1
                    ELSE 0
                END,
                tasks.deadline,
                tasks.id DESC
            """
        ).fetchall()

        for task in tasks:
            status = task["status"]
            total_steps = task["total_steps"]
            completed_steps = task["completed_steps"]

            if status == "WIP":
                display_status = (
                    f"WIP - {completed_steps}/{total_steps} steps done"
                )
            else:
                display_status = status

            self.task_tree.insert(
                "",
                tk.END,
                iid=str(task["id"]),
                values=(
                    task["title"],
                    task["deadline"] or "",
                    display_status,
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
        is_done = self.new_step_done_var.get()
        has_dependency = int(self.new_step_has_dependency_var.get())
        dependency = self.step_dependency_var.get().strip()

        if description == "":
            messagebox.showwarning(
                "Missing step description",
                "Please enter a step description."
            )
            return

        if has_dependency and dependency == "":
            messagebox.showwarning(
                "Missing dependency",
                "Please enter a dependency for the step."
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
                is_done,
                has_dependency,
                dependency,
                position
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                self.selected_task_id,
                description,
                is_done,
                has_dependency,
                dependency if has_dependency else None,
                next_position
            )
        )

        self.conn.execute(
            """
            UPDATE tasks
            SET awaiting_confirmed = 0
            WHERE id = ?
            """,
            (self.selected_task_id,)
        )

        self.conn.commit()

        self.step_description_var.set("")
        self.new_step_done_var.set(False)
        self.new_step_has_dependency_var.set(False)
        self.step_dependency_var.set("")
        self.step_dependency_var_entry.config(state="disabled")

        self.recalculate_task_status(self.selected_task_id)
        self.load_steps()
        self.load_tasks()

        self.step_description_entry.focus_set()

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
                is_done,
                has_dependency,
                dependency
            FROM steps
            WHERE task_id = ?
            ORDER BY
                position,
                id
            """,
            (self.selected_task_id,)
        ).fetchall()

        for step in steps:
            done_symbol = "☑" if step["is_done"] else "☐"

            if step["has_dependency"]:
                dependency_display = step["dependency"] or ""
            else:
                dependency_display = ""

            self.step_tree.insert(
                "",
                tk.END,
                iid=str(step["id"]),
                values=(
                    step["description"],
                    done_symbol,
                    dependency_display
                )
            )





    #Detect when a step is selected
    def on_step_selected(self, event=None):
        selected_items = self.step_tree.selection()

        if not selected_items:
            return

        step_id = int(
            selected_items[0]
        )

        step = self.conn.execute(
            """
            SELECT
                is_done,
                has_dependency,
                dependency
            FROM steps
            WHERE id = ?
            """,
            (step_id,)
        ).fetchone()

        if step is None:
            return

        self.selected_step_done_var.set(
            bool(step["is_done"])
        )

        self.selected_step_has_dependency_var.set(
            bool(step["has_dependency"])
        )

        self.selected_step_dependency_var.set(
            step["dependency"] or ""
        )

        if step["has_dependency"]:
            self.selected_step_dependency_entry.config(state="normal")
        else:
            self.selected_step_dependency_entry.config(state="disabled")






    #Update a step's status
    def update_step(self):
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

        is_done = int(
            self.selected_step_done_var.get()
        )

        has_dependency = int(
            self.selected_step_has_dependency_var.get()
        )

        dependency = (self.selected_step_dependency_var.get().strip())

        if has_dependency and dependency == "":
            messagebox.showwarning(
                "Missing dependency",
                "Please enter a dependency for the step."
            )

            return

        self.conn.execute(
            """
            UPDATE steps
            SET
                is_done = ?,
                has_dependency = ?,
                dependency = ?
            WHERE id = ?
            """,
            (
                is_done,
                has_dependency,
                dependency if has_dependency else None,
                step_id
            )
        )

        self.conn.execute(
            """
            UPDATE tasks
            SET awaiting_confirmed = 0
            WHERE id = ?
            """,
            (self.selected_task_id,)
        )

        self.conn.commit()

        self.recalculate_task_status(self.selected_task_id)
        self.load_steps()
        self.load_tasks()

    def recalculate_task_status(self, task_id):
        task = self.conn.execute(
            """
            SELECT
                dependency,
                awaiting_confirmed
            FROM tasks
            WHERE id = ?
            """,
            (task_id,)
        ).fetchone()

        if task is None:
            return

        step_summary = self.conn.execute(
            """
            SELECT
                COUNT(*) AS total_steps,
                
                COALESCE(
                    SUM(
                        CASE
                            WHEN is_done = 1 THEN 1
                            ELSE 0
                        END
                    ),
                    0
                ) AS completed_steps,

                COALESCE(
                    SUM(
                        CASE
                            WHEN has_dependency = 1
                                AND dependency IS NOT NULL
                                AND TRIM(dependency) != ''
                            THEN 1
                            ELSE 0
                        END
                    ),
                    0
                ) AS dependent_steps
            
            FROM steps
            WHERE task_id = ?
            """,
            (task_id,)
        ).fetchone()

        total_steps = step_summary["total_steps"]
        completed_steps = step_summary["completed_steps"]
        dependent_steps = step_summary["dependent_steps"]

        task_has_dependency = bool(
            task["dependency"]
            and task["dependency"].strip()
        )

        has_any_dependency =(
            task_has_dependency
            or dependent_steps > 0
        )

        if total_steps == 0:
            new_status = "TBD"

        elif completed_steps == 0:
            new_status = "TBD"

        elif completed_steps < total_steps:
            new_status = "WIP"

        elif has_any_dependency:
            if task["awaiting_confirmed"]:
                new_status = "Completed"
            else:
                new_status = "Awaiting"

        else:
            new_status = "Completed"

        self.conn.execute(
            """
            UPDATE tasks
            SET status = ?
            WHERE id = ?
            """,
            (new_status, 
             task_id
            )
        )

        self.conn.commit()


    def recalculate_all_task_statuses(self):
        task_ids = self.conn.execute(
            """
            SELECT id
            FROM tasks
            """
        ).fetchall()

        for task in task_ids:
            self.recalculate_task_status(task["id"])


    def complete_awaiting_task(self):
        if self.selected_task_id is None:
            messagebox.showwarning(
                "No task selected",
                "Please select a task first."
            )
            return

        task = self.conn.execute(
            """
            SELECT status
            FROM tasks
            WHERE id = ?
            """,
            (self.selected_task_id,)
        ).fetchone()

        if task is None:
            return

        if task["status"] != "Awaiting":
            messagebox.showinfo(
                "Task not awaiting",
                "The selected task is not in 'Awaiting' status."
            )
            return

        should_complete = messagebox.askyesno(
            "Complete awaiting task",
            (
                "Confirm that the dependencies for this task are resolved and mark it as completed?"
            )
        )

        if not should_complete:
            return

        self.conn.execute(
            """
            UPDATE tasks
            SET
                awaiting_confirmed = 1,
                status = 'Completed'
            WHERE id = ?
            """,
            (self.selected_task_id,)
        )

        self.conn.commit()
        self.load_tasks()








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

        if self.selected_task_id is None:
            return

        step_count = self.conn.execute(
            """
            SELECT COUNT(*)
            FROM steps
            WHERE task_id = ?
            """,
            (self.selected_task_id,)
        ).fetchone()[0]

        if step_count <= 1:
            messagebox.showwarning(
                "Step required",
                "A task must contain at least one step."
            )
            return

        step_id = int(selected_items[0])

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

        self.recalculate_task_status(self.selected_task_id)
        self.load_steps()
        self.load_tasks()





    #Closing the database
    def close_app(self):
        tasks_without_steps = self.conn.execute(
            """
            SELECT COUNT(*)
            FROM tasks
            WHERE NOT EXISTS (
                SELECT 1
                FROM steps
                WHERE steps.task_id = tasks.id
            )
            """
        ).fetchone()[0]

        if tasks_without_steps > 0:
            should_close = messagebox.askyesno(
                "Tasks without steps",
                (
                    f"There are {tasks_without_steps} tasks without any steps. "
                    "Are you sure you want to exit?"
                )
            )

            if not should_close:
                return

            
        self.conn.close()
        self.destroy()








#Start the program
if __name__ == "__main__":
    app = PlannerApp()
    app.mainloop()