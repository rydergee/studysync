import argparse
from task_manager import *

# Command line interface
def schedule(args):
    tasks = initialize_tasks()

    if args.command == "add":
        task = create_task(args.name, due_date=args.due, est_hours=args.hours)
        tasks.append(task)
        if(task["source"] == "custom"):
            save_custom_tasks(load_custom_tasks() + [task])
        print(f"Added task: {task['summary']}")
    
    elif arg.command == "complete":
        task_id = int(args.id)
        mark_complete(task_id, tasks)
        if task:
            print(f"Task '{task['summary']}' marked as complete.")
        else:
            print(f"Task with ID {task_id} not found.")
            