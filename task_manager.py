import json
import os
from ics_parser import load_ics_events
from datetime import datetime, timedelta, time


TASKS_PATH = "tasks.json"
CUSTOM_TASKS_PATH = "custom_tasks.json"
ICS_FILE = "user_qnST2MdyBUrxKU3OE9urleIJfd69bD8CESPNrXWv.ics"

# Json Storage

def load_tasks():
    if not os.path.exists(TASKS_PATH) or os.path.getsize(TASKS_PATH) == 0:
        return []
    with open(TASKS_PATH, "r") as f:
        return json.load(f)
    
def save_tasks(tasks):
    with open(TASKS_PATH, "w") as f:
        json.dump(tasks, f, indent=2, default=str)

def load_custom_tasks():
    if not os.path.exists(CUSTOM_TASKS_PATH) or os.path.getsize(CUSTOM_TASKS_PATH) == 0:
        return []
    with open(CUSTOM_TASKS_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []
    
def save_custom_tasks(tasks):
    with open(CUSTOM_TASKS_PATH, "w") as f:
        json.dump(tasks, f, indent=2, default=str)

# Initialization

def initialize_tasks():
    saved_canvas = load_tasks()
    if not saved_canvas:
        canvas_tasks = load_ics_events(ICS_FILE)
        save_tasks(canvas_tasks)
        saved_canvas = load_tasks()
    saved_custom = load_custom_tasks()
    all_tasks = saved_canvas + saved_custom
    return assign_task_ids(all_tasks)

# Task Management

def create_task(summary, due_date=None, hours=0, source="custom"):
    return {
        "id": None,
        "summary": summary,
        "due": due_date,
        "time_spent": hours,
        "completed": False,
        "source": source
    }

def assign_task_ids(tasks):
    for idx, task in enumerate(tasks):
        task["id"] = idx
    return tasks

def mark_complete(task_id, tasks):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks([t for t in tasks if t["source"] == "canvas"])
            save_custom_tasks([t for t in tasks if t["source"] == "custom"])
            return task
    return None

# Free study periods during the week
STUDY_BLOCKS = {
    "Monday": [("13:00", "16:00"), ("18:00", "20:00")],
    "Tuesday": [("13:00", "16:00"), ("18:00", "20:00")],
    "Wednesday": [("13:00", "16:00"), ("18:00", "20:00")],
    "Thursday": [("13:00", "16:00"), ("18:00", "20:00")],
    "Friday": [("13:00", "16:00"), ("18:00", "20:00")],
    "Saturday": [],
    "Sunday": [("12:00", "15:00"), ("17:00", "18:00"), ("19:00", "21:00")]
}

# Study block management
def get_study_blocks_for_week(start_date: datetime.date):
    study_blocks_for_week = []
    
    for i in range(7):  # Looping over the next 7 days (one week)
        day = start_date + timedelta(days=i)
        weekday = day.strftime("%A")  # e.g. "Monday"
        blocks = STUDY_BLOCKS.get(weekday, [])
        result = []
        
        for start_str, end_str in blocks:
            start_time = datetime.combine(day, datetime.strptime(start_str, "%H:%M").time())
            end_time = datetime.combine(day, datetime.strptime(end_str, "%H:%M").time())
            result.append((start_time, end_time))
        
        study_blocks_for_week.append((day, result))
    
    return study_blocks_for_week
