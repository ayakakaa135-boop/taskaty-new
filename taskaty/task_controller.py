import os
import json
from datetime import date
from tabulate import tabulate
from colorama import Fore, Style
from taskaty.task import Task


class TaskController:
    def __init__(self, file_name):
        self.file_name = file_name

    # تحميل المهام من JSON
    def _load_tasks(self):
        if not os.path.exists(self.file_name):
            return []
        with open(self.file_name, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Task.from_dict(task) for task in data]

    # حفظ المهام
    def _save_tasks(self, tasks):
        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in tasks], f, indent=4, ensure_ascii=False)

    # إضافة مهمة جديدة
    def add_task(self, args):
        if not args.start_date:
            args.start_date = date.today().isoformat()

        if args.end_date:
            try:
                date.fromisoformat(args.end_date)
            except ValueError:
                print(f"⚠️ Invalid end date format: {args.end_date}. Use YYYY-MM-DD format.")
                return

        new_task = Task(
            title=args.title,
            description=args.description,
            start_date=args.start_date,
            end_date=args.end_date,
            done=args.done,
            priority=args.priority
        )

        tasks = self._load_tasks()
        tasks.append(new_task)
        self._save_tasks(tasks)
        print(Fore.GREEN + f"✅ Task '{args.title}' added successfully!" + Style.RESET_ALL)

    # عرض المهام غير المنجزة
    def list_task(self):
        return [t for t in self._load_tasks() if not t.done and not t.canceled]

    # عرض كل المهام
    def list_all_task(self):
        return self._load_tasks()

    # تعليم مهمة كمكتملة
    def mark_done(self, task_id):
        tasks = self._load_tasks()
        try:
            task = tasks[task_id - 1]
            if task.done:
                print(Fore.YELLOW + "⚠️ Task already marked as done." + Style.RESET_ALL)
                return
            task.done = True
            self._save_tasks(tasks)
            print(Fore.GREEN + f"✅ Task '{task.title}' marked as done!" + Style.RESET_ALL)
        except IndexError:
            print(Fore.RED + "❌ Invalid task ID." + Style.RESET_ALL)

    # إلغاء مهمة
    def cancel_task(self, task_id):
        tasks = self._load_tasks()
        try:
            task = tasks[task_id - 1]
            if task.canceled:
                print(Fore.YELLOW + "⚠️ Task already canceled." + Style.RESET_ALL)
                return
            task.canceled = True
            self._save_tasks(tasks)
            print(Fore.RED + f"🚫 Task '{task.title}' has been canceled." + Style.RESET_ALL)
        except IndexError:
            print(Fore.RED + "❌ Invalid task ID." + Style.RESET_ALL)

    # فلترة حسب الأولوية
    def filter_tasks(self, priority):
        tasks = self._load_tasks()
        filtered = [t for t in tasks if t.priority.lower() == priority.lower()]
        return filtered

    # حساب المدة بين تاريخين
    def due_date(self, start=None, end=None):
        if not start or not end:
            return "⚠️ Missing dates"
        start_date = date.fromisoformat(start)
        end_date = date.fromisoformat(end)
        return f"{(end_date - start_date).days} day(s) left"

    # عرض إحصائيات عامة
    def show_stats(self):
        tasks = self._load_tasks()
        total = len(tasks)
        done = sum(t.done for t in tasks)
        canceled = sum(t.canceled for t in tasks)
        high = sum(t.priority == "high" for t in tasks)
        low = sum(t.priority == "low" for t in tasks)
        pending = total - done - canceled

        print(Fore.CYAN + "\n📊 TASKS SUMMARY" + Style.RESET_ALL)
        print("──────────────────────────────")
        print(Fore.GREEN + f"✅ Done: {done}" + Style.RESET_ALL)
        print(Fore.RED + f"🚫 Canceled: {canceled}" + Style.RESET_ALL)
        print(Fore.MAGENTA + f"🔴 High Priority: {high}" + Style.RESET_ALL)
        print(Fore.WHITE + f"⚪ Low Priority: {low}" + Style.RESET_ALL)
        print(Fore.YELLOW + f"🕓 Pending: {pending}" + Style.RESET_ALL)
        print(Fore.CYAN + f"📋 Total Tasks: {total}\n" + Style.RESET_ALL)

    # عرض المهام بجدول ملوّن
    def print_table(self, tasks):
        if not tasks:
            print("⚠️ No tasks found.")
            return

        formatted = []
        for i, t in enumerate(tasks, 1):
            due = self.due_date(t.start_date, t.end_date) if t.end_date else "open"

            color = Style.RESET_ALL
            if t.priority == "high":
                color = Fore.RED
            elif t.done:
                color = Fore.GREEN
            elif t.canceled:
                color = Fore.LIGHTBLACK_EX

            formatted.append([
                color + str(i) + Style.RESET_ALL,
                color + t.title + Style.RESET_ALL,
                color + t.description + Style.RESET_ALL,
                t.start_date,
                t.end_date or "N/A",
                due,
                "✅" if t.done else ("🚫" if t.canceled else "🕓"),
                t.priority
            ])

        print(tabulate(
            formatted,
            headers=["#", "Title", "Description", "Start", "End", "Due", "Status", "Priority"],
            tablefmt="fancy_grid"
        ))
