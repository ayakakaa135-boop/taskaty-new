from datetime import date

class Task:
    def __init__(self, title, description=None, start_date=None, end_date=None,
                 done=False, priority="low", canceled=False):
        self.title = title
        self.description = description
        self.start_date = start_date or date.today().isoformat()
        self.end_date = end_date
        self.done = done
        self.priority = priority.lower()
        self.canceled = canceled

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "done": self.done,
            "priority": self.priority,
            "canceled": self.canceled
        }

    def __str__(self):
        return f"{self.title} ({self.priority})"
