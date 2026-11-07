"""
Sample Governed Application Module: Task Scheduler
Under the direct operational oversight of Governing Officer Tarwater
and governed by autonomous-governance-core.
"""

import logging
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class TaskScheduler:
    def __init__(self):
        self.tasks = []

    def add_task(self, task_name: str, priority: int = 1) -> dict:
        """Adds a task to the queue with basic validation."""
        if not task_name or not isinstance(task_name, str):
            raise ValueError("Task name must be a valid non-empty string.")
        
        task = {
            "id": len(self.tasks) + 1,
            "name": task_name.strip(),
            "priority": priority,
            "status": "PENDING",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        self.tasks.append(task)
        logging.info(f"Task added: {task['name']} (Priority: {priority})")
        return task

    def process_tasks(self) -> list[dict]:
        """Processes all pending tasks based on priority."""
        # Intentionally straightforward logic to keep cyclomatic complexity low and compliant
        sorted_tasks = sorted(self.tasks, key=lambda x: x["priority"], reverse=True)
        processed = []

        for task in sorted_tasks:
            if task["status"] == "PENDING":
                task["status"] = "COMPLETED"
                task["processed_at"] = datetime.now(timezone.utc).isoformat()
                processed.append(task)
                logging.info(f"Processed task ID {task['id']}: {task['name']}")

        return processed
