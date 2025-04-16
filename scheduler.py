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
    
    elif args.command == "complete":
        task_id = int(args.id)
        task = mark_complete(task_id, tasks)
        if task:
            print(f"Task '{task['summary']}' marked as complete.")
        else:
            print(f"Task with ID {task_id} not found.")
    
    elif args.command == "list":
        for task in tasks:
            status = "Complete" if task["completed"] else "Pending"
            print(f"ID: {task['id']} | {task['summary']} | Due: {task["due"]} | Status: {status}")

# Main function to handle arguments
def main():
    parser = argparse.ArgumentParser(description="AI-Enhanced Personal Scheduler")
    subparsers = parser.add_subparsers(dest="command")
    
    # Add custom task
    add_parser = subparsers.add_parser("add", help="Add a custom task")
    add_parser.add_argument("--name", required=True, help="Task name/summary")
    add_parser.add_argument("--hours", required=True, type=int, help="Estimated hours for the task")
    add_parser.add_argument("--due", required=False, help="Task due date (optional)")

    # Complete a task
    complete_parser = subparsers.add_parser("complete", help="Mark task as complete")
    complete_parser.add_argument("id", help="ID of the task to mark as complete")
    
    # List active tasks
    subparsers.add_parser("list", help="List all active tasks")
    
    args = parser.parse_args()
    schedule(args)

if __name__ == "__main__":
    main()