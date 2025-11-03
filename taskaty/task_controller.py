import json
import os
from datetime import date
from tabulate import tabulate
from colorama import Fore, Style
from taskaty.task import Task


class TaskController:
    def __init__(self, file_name):
        self.file_name = file_name
        if not os.path.exists(self.file_name):
            with open(self.file_name, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _load_tasks(self):
        with open(self.file_name, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_tasks(self, tasks):
        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=4)

    def add_task(self, args):
        tasks = self._load_tasks()
        task = Task(
            title=args.title,
            description=args.description,
            start_date=args.start_date or date.today().isoformat(),
            end_date=args.end_date,
            priority=args.priority or "low"
        )
        tasks.append(task.to_dict())
        self._save_tasks(tasks)
        print(Fore.GREEN + f"✅ Task '{task.title}' added successfully!" + Style.RESET_ALL)

    def list_all_tasks(self):
        tasks = self._load_tasks()
        if not tasks:
            print(Fore.YELLOW + "⚠️ No tasks found." + Style.RESET_ALL)
            return

        formatted = []
        for i, task in enumerate(tasks, 1):
            color = Fore.WHITE
            if task["canceled"]:
                color = Fore.LIGHTBLACK_EX
            elif task["done"]:
                color = Fore.GREEN
            elif task["priority"] == "high":
                color = Fore.RED

            formatted.append({
                "#": f"{color}{i}{Style.RESET_ALL}",
                "Title": f"{color}{task['title']}{Style.RESET_ALL}",
                "Priority": f"{color}{task['priority'].capitalize()}{Style.RESET_ALL}",
                "Status": "✅ Done" if task["done"] else ("🚫 Canceled" if task["canceled"] else "🕓 Pending"),
                "Start Date": task["start_date"],
                "End Date": task["end_date"] or "N/A"
            })

        print(tabulate(formatted, headers="keys", tablefmt="fancy_grid"))

    def mark_done(self, task_id):
        tasks = self._load_tasks()
        if task_id <= 0 or task_id > len(tasks):
            print(Fore.RED + "❌ Invalid task ID." + Style.RESET_ALL)
            return
        tasks[task_id - 1]["done"] = True
        self._save_tasks(tasks)
        print(Fore.GREEN + f"✅ Task {task_id} marked as done!" + Style.RESET_ALL)

    def cancel_task(self, task_id):
        tasks = self._load_tasks()
        if task_id <= 0 or task_id > len(tasks):
            print(Fore.RED + "❌ Invalid task ID." + Style.RESET_ALL)
            return
        tasks[task_id - 1]["canceled"] = True
        self._save_tasks(tasks)
        print(Fore.LIGHTBLACK_EX + f"🚫 Task {task_id} has been canceled." + Style.RESET_ALL)

    def filter_by_priority(self, level):
        tasks = [t for t in self._load_tasks() if t["priority"] == level.lower()]
        if not tasks:
            print(Fore.YELLOW + f"⚠️ No {level} priority tasks found." + Style.RESET_ALL)
            return
        self.print_table(tasks)

    def show_stats(self):

        tasks = self._load_tasks()
        if not tasks:
            print(Fore.YELLOW + "⚠️ No tasks found." + Style.RESET_ALL)
            return

        total = len(tasks)
        done = sum(1 for t in tasks if t["done"])
        canceled = sum(1 for t in tasks if t["canceled"])
        high_priority = sum(1 for t in tasks if t["priority"] == "high")
        low_priority = sum(1 for t in tasks if t["priority"] == "low")
        pending = total - done - canceled

        print(Fore.CYAN + "\n📊 TASKS SUMMARY" + Style.RESET_ALL)
        print(Fore.WHITE + "──────────────────────────────" + Style.RESET_ALL)
        print(Fore.GREEN + f"✅ Done: {done}" + Style.RESET_ALL)
        print(Fore.LIGHTBLACK_EX + f"🚫 Canceled: {canceled}" + Style.RESET_ALL)
        print(Fore.RED + f"🔴 High Priority: {high_priority}" + Style.RESET_ALL)
        print(Fore.WHITE + f"⚪ Low Priority: {low_priority}" + Style.RESET_ALL)
        print(Fore.BLUE + f"🕓 Pending: {pending}" + Style.RESET_ALL)
        print(Fore.CYAN + f"📋 Total Tasks: {total}\n" + Style.RESET_ALL)


    def print_table(self, tasks):
        formatted = []
        for number, task in enumerate(tasks, 1):
            formatted.append({
                "#": number,
                "Title": task['title'],
                "Priority": task['priority'],
                "Done": "✅" if task['done'] else "❌",
                "Canceled": "🚫" if task['canceled'] else "",
                "Start": task['start_date'],
                "End": task['end_date'] or "N/A"
            })
        print(tabulate(formatted, headers="keys", tablefmt="fancy_grid"))
