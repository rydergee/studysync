import json
import os

TASKS_PATH = "tasks.json"

def load_custom_tasks():
    if not os.path.exists(TASKS_PATH):
        return []
    with open(TASKS_PATH, "r") as f:
        return json.load(f)
    
def save_custom_tasks(tasks):
    with open(TASKS_PATH, "w") as f:
        json.dump(tasks, f, indent=2, default=str)

def create_task(summary, due_date=None, est_hours=None, source="custom"):
    return {
        "id": None,
        "summary": summary,
        "due": due_date,
        "estimated_time": est_hours,
        "remaining_time": est_hours,
        "completed": False,
        "source": source
    }
