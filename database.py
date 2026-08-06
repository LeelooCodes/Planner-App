import sqlite3

from datetime import datetime

DB_FILE = "planner.db"


class PlannerDatabase:
    def __init__(self, db_file=DB_FILE):
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = sqlite3.Row

        self.create_tables()
        self.recalculate_all_task_statuses()

    def create_tables(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                deadline TEXT,
                dependency TEXT,
                status TEXT NOT NULL DEFAULT 'TBD',
                dependency_resolved INTEGER NOT NULL DEFAULT 0,
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
                dependency_resolved INTEGER NOT NULL DEFAULT 0,
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
        self.migrate_database()

    def migrate_database(self):
        task_columns = {
            row["name"]
            for row in self.conn.execute(
                "PRAGMA table_info(tasks)"
            ).fetchall()
        }
        

        if "dependency_resolved" not in task_columns:
            self.conn.execute(
                """
                ALTER TABLE tasks
                ADD COLUMN dependency_resolved
                INTEGER NOT NULL DEFAULT 0
                """
            )

        step_columns = {
            row["name"]
            for row in self.conn.execute(
                "PRAGMA table_info(steps)"
            ).fetchall()
        }

        if "dependency_resolved" not in step_columns:
            self.conn.execute(
                """
                ALTER TABLE steps
                ADD COLUMN dependency_resolved
                INTEGER NOT NULL DEFAULT 0
                """
            )

        self.conn.commit()

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

    def recalculate_task_status(self, task_id):
        task = self.conn.execute(
            """
            SELECT
                dependency,
                dependency_resolved
            FROM tasks
            WHERE id = ?
            """,
            (task_id, )
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
                                AND dependency_resolved = 0
                            THEN 1
                            ELSE 0
                        END
                    ),
                    0
                ) AS unresolved_step_dependencies
            
            FROM steps
            WHERE task_id = ?
            """,
            (task_id,)
        ).fetchone()

        total_steps = step_summary["total_steps"]
        completed_steps = step_summary["completed_steps"]

        unresolved_step_dependencies = (
            step_summary["unresolved_step_dependencies"]
        )

        task_has_unresolved_dependency = bool(
            task["dependency"]
            and task["dependency"].strip()
            and not bool(task["dependency_resolved"])
        )

        has_unresolved_dependency = (
            task_has_unresolved_dependency
            or unresolved_step_dependencies > 0
        )

        if total_steps == 0:
            new_status = "TBD"

        elif completed_steps == 0:
            new_status = "TBD"

        elif completed_steps < total_steps:
            new_status = "WIP"

        elif has_unresolved_dependency:
            new_status = "Awaiting"

        else:
            new_status = "Completed"

        self.conn.execute(
            """
            UPDATE tasks
            SET status = ?
            WHERE id = ?
            """,
            (
                new_status,
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
            self.recalculate_task_status(
                task["id"]
            )
                
    def get_tasks(self):
        tasks = self.conn.execute(
            """
            SELECT
                tasks.id,
                tasks.title,
                tasks.deadline,
                tasks.dependency,
                tasks.status,
                tasks.dependency_resolved,
                tasks.created_at,

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
                tasks.status,
                tasks.dependency_resolved,
                tasks.created_at
            
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

        task_list = []

        for task in tasks:
            status = task["status"]
            total_steps = task["total_steps"]
            completed_steps = task["completed_steps"]

            if status == "WIP":
                display_status = (
                    f"WIP - {completed_steps}/{total_steps} steps done."
                    )

            else:
                display_status = status


            task_list.append(
                {
                    "id": task["id"],
                    "title": task["title"],
                    "deadline": task["deadline"] or "",
                    "dependency": task["dependency"] or "",
                    "status": status,
                    "display_status": display_status,
                    "dependency_resolved": bool(
                        task["dependency_resolved"]
                    ),
                    "created_at": task["created_at"],
                    "total_steps": total_steps,
                    "completed_steps": completed_steps
                }
            )

        return task_list

    def get_task(self, task_id):
        task = self.conn.execute(
            """
            SELECT
                id,
                title,
                deadline,
                dependency,
                status,
                dependency_resolved,
                created_at
            FROM tasks
            WHERE id = ?
            """,
            (task_id,)
        ).fetchone()

        if task is None:
            return None

        return {
            "id": task["id"],
            "title": task["title"],
            "deadline": task["deadline"] or "",
            "dependency": task["dependency"] or "",
            "status": task["status"],
            "dependency_resolved": bool(
                task["dependency_resolved"]
            ),
            "created_at": task["created_at"]
        }

    def get_steps(self, task_id):
        steps = self.conn.execute(
            """
            SELECT
                id,
                task_id,
                description,
                is_done,
                has_dependency,
                dependency,
                dependency_resolved,
                position
            FROM steps
            WHERE task_id = ?
            ORDER BY
                position,
                id
            """,
            (task_id,)
        ).fetchall()

        step_list = []

        for step in steps:
            step_list.append(
                {
                    "id": step["id"],
                    "task_id": step["task_id"],
                    "description": step["description"],
                    "is_done": bool(step["is_done"]),
                    "has_dependency": bool(
                        step["has_dependency"]
                    ),
                    "dependency": step["dependency"] or "",
                    "dependency_resolved": bool(
                        step["dependency_resolved"]
                    ),
                    "position": step["position"]
                }
            )

        return step_list

    def get_step(self, step_id):
        step = self.conn.execute(
            """
            SELECT
                id,
                task_id,
                description,
                is_done,
                has_dependency,
                dependency,
                dependency_resolved,
                position
            FROM steps
            WHERE id = ?
            """,
            (step_id, )
        ).fetchone()

        if step is None:
            return None

        return {
            "id": step["id"],
            "task_id": step["task_id"],
            "description": step["description"],
            "is_done": bool(step["is_done"]),
            "has_dependency": bool(
                step["has_dependency"]
            ),
            "dependency": step["dependency"] or "",
            "dependency_resolved": bool(
                step["dependency_resolved"]
            ),
            "position": step["position"]
        }

    def add_task(
        self,
        title,
        deadline="",
        dependency=""
    ):
        title = title.strip()
        deadline = deadline.strip()
        dependency = dependency.strip()

        if title == "":
            raise ValueError("Task title cannot be empty.")

        if not self.validate_deadline(deadline):
            raise ValueError(
                "Invalid deadline format. Use YYYY-MM-DD."
            )

        cursor = self.conn.execute(
            """
            INSERT INTO tasks (
                title,
                deadline,
                dependency,
                dependency_resolved,
                status,
                created_at
            ) 
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                title,
                deadline if deadline else None,
                dependency if dependency else None,
                0,
                "TBD",
                datetime.now().isoformat(timespec="seconds")
            )
        )

        self.conn.commit()

        return cursor.lastrowid

    def add_step(
        self,
        task_id,
        description,
        is_done=False,
        has_dependency=False,
        dependency="",
    ):
        description = description.strip()
        dependency = dependency.strip()

        if description == "":
            raise ValueError(
                "Step description cannot be empty."
            )

        if has_dependency and dependency == "":
            raise ValueError(
                "Please enter who or what the step is dependent on."
            )

        task = self.get_task(task_id)

        if task is None:
            raise ValueError(
                f"The selected task does not exist."
            )

        result = self.conn.execute(
            """
            SELECT COALESCE(MAX(position), 0) + 1
            FROM steps
            WHERE task_id = ?
            """,
            (task_id,)
        ).fetchone()

        next_position = result[0] 

        cursor = self.conn.execute(
            """
            INSERT INTO steps (
                task_id,
                description,
                is_done,
                has_dependency,
                dependency,
                dependency_resolved,
                position
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                task_id,
                description,
                int(bool(is_done)),
                int(bool(has_dependency)),
                dependency if has_dependency else None,
                0,
                next_position
            )
        )

        self.conn.commit()
        self.recalculate_task_status(task_id)

        return cursor.lastrowid

    def update_step(
        self,
        step_id,
        description,
        has_dependency=False,
        dependency=""
    ):
        description = description.strip()
        dependency = dependency.strip()

        if description == "":
            raise ValueError(
                "Step description cannot be empty."
            )

        if has_dependency and dependency == "":
            raise ValueError(
                "Please enter who or what "
                "the step is dependent on."
            )

        existing_step = self.get_step(step_id)

        if existing_step is None:
            raise ValueError(
                "The selected step does not exist."
            )

        task_id = existing_step["task_id"]

        dependency_changed = (
            existing_step["has_dependency"]
            != bool(has_dependency)
            or existing_step["dependency"]
            != dependency
        )

        if not has_dependency:
            saved_dependency = None
            dependency_resolved = 0
        else:
            saved_dependency = dependency

            if dependency_changed:
                dependency_resolved = 0
            else:
                dependency_resolved = int(
                    existing_step["dependency_resolved"]
                )

        self.conn.execute(
            """
            UPDATE steps
            SET
                description = ?,
                has_dependency = ?,
                dependency = ?,
                dependency_resolved = ?
            WHERE id = ?
            """,
            (
                description,
                int(bool(has_dependency)),
                saved_dependency,
                dependency_resolved,
                step_id
            )
        )

        self.conn.commit()

        self.recalculate_task_status(task_id)

        return task_id

    def delete_step(self, step_id):
        step = self.get_step(step_id)

        if step is None:
            raise ValueError(
                "The selected step does not exist."
            )

        task_id = step["task_id"]

        self.conn.execute(
            """
            DELETE FROM steps
            WHERE id = ?
            """,
            (step_id, )
        )

        self.conn.commit()

        self.recalculate_task_status(task_id)

        return task_id

    def set_step_done(self, step_id, is_done):
        step = self.conn.execute(
            """
            SELECT task_id
            FROM steps
            WHERE id = ?
            """,
            (step_id, )
        ).fetchone()

        if step is None:
            raise ValueError(
                "The selected step does not exist."
            )

        task_id = step["task_id"]

        self.conn.execute(
            """
            UPDATE steps
            SET is_done = ?
            WHERE id = ?
            """,
            (
                int(bool(is_done)),
                step_id
            )
        )

        self.conn.commit()

        self.recalculate_task_status(task_id)

        return task_id

    def set_step_dependency_resolved(
            self,
            step_id,
            is_resolved
    ):
        step = self.get_step(step_id)

        if step is None:
            raise ValueError(
                "The selected step does not exist."
            )

        if not step["has_dependency"]:
            raise ValueError(
                "This step does not have a dependency."
            )

        task_id = step["task_id"]

        self.conn.execute(
            """
            UPDATE steps
            SET dependency_resolved = ?
            WHERE id = ?
            """,
            (
                int(bool(is_resolved)),
                step_id
            )
        )

        self.conn.commit()

        self.recalculate_task_status(task_id)

        return task_id

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    database = PlannerDatabase()

    print("Database connection successful.")
    print("Tables created or verified successfully.")
    print("Dependency-resolution migration successful.")
    print("Task statuses recalculated successfully.")

    tasks = database.get_tasks()

    print(f"Tasks found: {len(tasks)}")

    database.close()