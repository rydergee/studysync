from icalendar import Calendar
from datetime import datetime
def load_ics_events(filepath):
    with open(filepath, 'r') as f:
        cal = Calendar.from_ical(f.read())

    events = []
    for event in cal.walk():
        if event.name == "VEVENT":
            dt = event.get("dtstart").dt
            if(isinstance(dt,datetime) is False):
                dt = datetime.combine(dt,datetime.max.time().replace(microsecond=0))
    
            events.append({
                "id": None,
                "summary": str(event.get("summary")),
                "time_spent": 0,
                "due": dt,
                "completed": False,
                "source": "canvas"
            })
    return events