# AI-Enhanced Personal Scheduler (StudySync)

A Python-based command-line tool that leverages the Google Gemini API to automatically generate an optimized weekly study schedule. It integrates tasks from a Canvas calendar export (.ics) and custom user-defined tasks, fitting them into predefined study blocks. The output is an `.ics` file ready to be imported into your favorite calendar application.

## Features

*   **Task Integration:** Imports tasks directly from a Canvas calendar `.ics` export.
*   **Custom Tasks:** Allows adding custom tasks with estimated hours and due dates via the CLI.
*   **Study Blocks:** Define your recurring weekly availability for study sessions.
*   **AI-Powered Scheduling:** Uses Google Gemini to intelligently prioritize tasks and schedule them into available blocks based on due dates and other factors (like quiz availability).
*   **Calendar Export:** Generates a weekly schedule as an `.ics` file (`weekly_schedule.ics`).
*   **Task Management:** List pending tasks and mark tasks as complete.
*   **Simple CLI:** Easy-to-use command-line interface for managing tasks and generating schedules.

## Prerequisites

*   Python 3.x
*   Google Gemini API Key
*   Canvas Calendar Export (`.ics` file)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone (https://github.com/rydergee/studysync)
    cd [studysync]
    ```

2.  **Install dependencies:**
    ```bash
    pip install google-generativeai python-dotenv python-dateutil icalendar
    ```
    *(Consider creating a `requirements.txt` file for easier dependency management)*

## Configuration

1.  **API Key:**
    *   Create a file named `.env` in the project root directory.
    *   Add your Google Gemini API key to this file:
        ```dotenv
        API_KEY=YOUR_GEMINI_API_KEY
        ```

2.  **Canvas ICS File:**
    *   Export your calendar from Canvas as an `.ics` file.
    *   Place this file in the project root directory.
    *   By default, the script looks for `user_qnST2MdyBUrxKU3OE9urleIJfd69bD8CESPNrXWv.ics`. If your filename is different, update the `ICS_FILE` variable near the top of `task_manager.py`.

3.  **Study Blocks:**
    *   Define your regular weekly study availability by editing the `STUDY_BLOCKS` dictionary within the `task_manager.py` file. The format is `{"Weekday": [("HH:MM", "HH:MM"), ...]}`.

## Usage

The main interface is through `scheduler.py` via the command line.

*   **Show Help:**
    ```bash
    python scheduler.py --help
    ```

*   **Add a Custom Task:**
    ```bash
    # Example: Add a task named "Research Paper Outline" estimated to take 4 hours, due Oct 26, 2024
    python scheduler.py add --name "Research Paper Outline" --hours 4 --due "2024-10-26"

    # Example: Add a task with no specific due date
    python scheduler.py add --name "Review Lecture Notes" --hours 2
    ```
    *Custom tasks are saved in `custom_tasks.json`.*

*   **List Active Tasks:**
    ```bash
    python scheduler.py list
    ```
    *Lists both Canvas and custom tasks that are not marked as complete.*

*   **Mark a Task as Complete:**
    ```bash
    # Replace <task_id> with the actual ID from the list command
    python scheduler.py complete <task_id>
    ```

*   **Generate the AI Schedule:**
    ```bash
    python scheduler.py schedule
    ```
    *This command will:*
    1.  Load Canvas and custom tasks.
    2.  Identify tasks due within the next few weeks.
    3.  Fetch your defined study blocks for the upcoming week.
    4.  Send this information to the Google Gemini API.
    5.  Receive the optimized schedule.
    6.  *(Note: The script currently updates the `time_spent` field based on the *scheduled* duration from Gemini, not actual time tracked.)*
    7.  Generate the `weekly_schedule.ics` file in the project root directory. You can then import this file into your calendar application (Google Calendar, Outlook Calendar, Apple Calendar, etc.).

## How it Works

1.  **Task Loading:** `task_manager.py` loads tasks from the specified Canvas `.ics` file (using `ics_parser.py`) and the `custom_tasks.json` file. It assigns unique IDs to all tasks.
2.  **Filtering:** `ai_prioritizer.py` filters for active (non-completed) tasks relevant to the upcoming period (currently set to 21 days).
3.  **Study Blocks:** It retrieves the defined study blocks for the next 7 days from `task_manager.py`.
4.  **Prompt Generation:** A detailed prompt is constructed, including the filtered tasks (with due dates, estimated time, etc.) and the available study blocks.
5.  **Gemini API Call:** The prompt is sent to the Google Gemini API (`gemini-2.5-pro-exp-03-25` model).
6.  **Response Parsing:** The script expects a JSON response from Gemini, listing the scheduled task chunks with start/end times and descriptions.
7.  **Task Update:** The `time_spent` attribute on tasks is updated based on the total time allocated to them in the generated schedule. *Note: This reflects scheduled time, not necessarily time worked.*
8.  **ICS Generation:** The scheduled chunks are formatted into an `.ics` calendar file using the `icalendar` library.

## Future Improvements / TODO

*   More robust error handling, especially for Gemini API responses and JSON parsing.
*   Allow configuration of study blocks and ICS file path via a separate config file instead of hardcoding.
*   Implement actual time tracking instead of just updating based on scheduled duration.
*   Add support for task dependencies.
*   More flexible study block definitions (e.g., one-off availability/unavailability).
*   Consider adding task priorities beyond just due dates.
*   Web interface or GUI?

## License

[Choose an appropriate license, e.g., MIT License]
