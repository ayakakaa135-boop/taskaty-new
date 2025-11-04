from datetime import date

class Task:
    def __init__(self, title, description, start_date, end_date=None,
                 done=False, priority="low", canceled=False):
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.done = done
        self.priority = priority
        self.canceled = canceled

    def __str__(self):
        return f"{self.title},{self.description},{self.start_date},{self.end_date},{self.done}"

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

    @staticmethod
    def from_dict(data):
        return Task(**data)
