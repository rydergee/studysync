from task_manager import *
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai
from dateutil.parser import parse as parse_date
from datetime import date
import re
from icalendar import Calendar, Event
from datetime import datetime
from uuid import uuid4

# Write schedule to ics file
def write_daily_schedule_to_ics(scheduled_chunks, tasks, filename="generated_schedule.ics"):
    cal = Calendar()
    cal.add('prodid', '-//StudySync Daily Schedule//')
    cal.add('version', '2.0')

    for chunk in scheduled_chunks:
        task_id = chunk['id']
        start = datetime.fromisoformat(chunk['start'])
        end = datetime.fromisoformat(chunk['end'])

        # Get the corresponding task by ID
        task = next((t for t in tasks if t['id'] == task_id), None)
        summary = task['summary'] if task and 'summary' in task else f"Task {task_id}"

        event = Event()
        event.add('summary', chunk['title'])  # <- This sets the name of the calendar event
        event.add('description', chunk['description'])
        event.add('dtstart', start)
        event.add('dtend', end)
        event.add('dtstamp', datetime.now())
        event['uid'] = str(uuid4()) + "@studysync"

        cal.add_component(event)

    with open(filename, 'wb') as f:
        f.write(cal.to_ical())

    print(f"✅ Wrote schedule to {filename}")


load_dotenv()

def get_active_tasks_for_day(tasks, today):
    three_weeks_from_now = today + timedelta(weeks=3)
    active = []

    for task in tasks:
        if task.get("completed"):
            continue

        due_str = task.get("due")
        if due_str:
            try:
                due_date = datetime.fromisoformat(due_str).date()
                if due_date < today or due_date > three_weeks_from_now:
                    continue
            except ValueError:
                continue  # skip invalid date formats

        active.append(task)

    return active

def create_gemini_prompt(tasks, study_blocks):
    # Creating the prompt string
    prompt = f"""
    You are a smart personal task scheduler. Based on the following study blocks and task list for today, create an optimal schedule to maximize efficiency and ensure upcoming deadlines are met. Fit tasks into the available blocks. Respond with a JSON list of scheduled chunks.

    Study blocks:
    {json.dumps(study_blocks, indent=2)}

    Tasks:
    {json.dumps(tasks, indent=2)}

    Each item in your response should be: (Title should be your recommended title)
    {{"id": ..., "title": ..., "description": ...,  "start": "...", "end": "..."}}
    The description value should include the due date, and why you have prioritised this with this amount of time

    **NOTE** Quizes & Code Runners only open a week prior to their due date
    """

    # Print the final prompt (for debugging)
    #print(prompt)
    
    return prompt

# Connecting to Gemini
genai.configure(api_key=os.getenv("API_KEY"))

def get_optimized_schedule_from_gemini(prompt):
    model = genai.GenerativeModel("gemini-2.5-pro-exp-03-25")
    response = model.generate_content(prompt)
    content = response.text.strip()

    print("📥 Raw Gemini Response:")
    print(content)

    # Strip out Markdown code block if present
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", content, re.DOTALL)
    if match:
        content = match.group(1)

    try:
        schedule = json.loads(content)
        print("✅ Parsed JSON schedule successfully.")
        return schedule
    except json.JSONDecodeError as e:
        print("❌ Failed to decode JSON:", e)
        print("⚠️ Gemini response not JSON-decodable. Output:\n", content)
        return []
    
# Edit the task instances and update time_spent
def apply_scheduled_chunks_to_tasks(scheduled_blocks, tasks):
    for chunk in scheduled_blocks:
        task_id = chunk["id"]
        start = parse_date(chunk["start"])
        end = parse_date(chunk["end"])
        duration_hours = (end - start).total_seconds() / 3600

        for task in tasks:
            if task["id"] == task_id:
                task["time_spent"] = max(task["time_spent"] + duration_hours, 0)
        save_tasks([t for t in tasks if t["source"] == "canvas"])
        save_custom_tasks([t for t in tasks if t["source"] == "custom"])

# Main ai schedule planner function
def ai_schedule():
    today = date.today()

    # load tasks
    tasks = initialize_tasks()

    active_tasks = get_active_tasks_for_day(tasks, today)
    study_blocks = get_study_blocks_for_day(today)

    if(study_blocks == []):
        print("No study blocks on this day.")
        return
    
    active_tasks = get_active_tasks_for_day(tasks, today)
    if not active_tasks:
        print("No active tasks for today!")
        return

    # Create gemini prompt
    print("🔧 Creating prompt for Gemini...")
    prompt = create_gemini_prompt(active_tasks, [
        {"start": start.isoformat(), "end": end.isoformat()}
        for start, end in study_blocks
    ])

    print("🧠 Sending prompt to Gemini for optimized scheduling...")
    response = get_optimized_schedule_from_gemini(prompt)
    print("✅ Received response from Gemini!")

    print("📝 Applying scheduled chunks to task time tracking...")
    apply_scheduled_chunks_to_tasks(response, tasks)
    print("✅ Task time updated based on Gemini's schedule.")

    print("📅 Writing today's schedule to ICS file...")
    write_daily_schedule_to_ics(response, tasks)
    print("✅ ICS calendar updated with today's plan!")
