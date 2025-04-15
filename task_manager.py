
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