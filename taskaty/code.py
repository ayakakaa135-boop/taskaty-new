import argparse
from taskaty.task_controller import TaskController


def main():
    controller = TaskController("tasks.json")

    parser = argparse.ArgumentParser(
        description="📝 Taskaty CLI — مدير مهام بسيط من سطر الأوامر"
    )
    subparsers = parser.add_subparsers(dest="command")

    # -----------------------------
    # 1️⃣ إضافة مهمة جديدة
    # -----------------------------
    add_task = subparsers.add_parser("add", help="Add a new task")
    add_task.add_argument("title", type=str, help="Title of the task")
    add_task.add_argument("-d", "--description", type=str, default="", help="Task description")
    add_task.add_argument("-s", "--start_date", type=str, default=None, help="Start date (YYYY-MM-DD)")
    add_task.add_argument("-e", "--end_date", type=str, default=None, help="End date (YYYY-MM-DD)")
    add_task.add_argument("-p", "--priority", type=str, choices=["low", "high"], default="low", help="Task priority")
    add_task.add_argument("--done", action="store_true", help="Mark task as done upon creation")

    # -----------------------------
    # 2️⃣ عرض المهام (غير المنجزة)
    # -----------------------------
    list_task = subparsers.add_parser("list", help="List unfinished tasks")
    list_task.add_argument("-a", "--all", action="store_true", help="List all tasks (including done/canceled)")

    # -----------------------------
    # 3️⃣ تعليم كمكتملة
    # -----------------------------
    done_task = subparsers.add_parser("done", help="Mark a task as completed")
    done_task.add_argument("task_id", type=int, help="ID of the task to mark as done")

    # -----------------------------
    # 4️⃣ إلغاء مهمة
    # -----------------------------
    cancel_task = subparsers.add_parser("cancel", help="Cancel a task")
    cancel_task.add_argument("task_id", type=int, help="ID of the task to cancel")

    # -----------------------------
    # 5️⃣ فلترة حسب الأولوية
    # -----------------------------
    filter_task = subparsers.add_parser("filter", help="Filter tasks by priority")
    filter_task.add_argument("priority", choices=["high", "low"], help="Priority to filter by")

    # -----------------------------
    # 6️⃣ إحصائيات
    # -----------------------------
    stats_task = subparsers.add_parser("stats", help="Show tasks statistics")

    args = parser.parse_args()

    # تنفيذ الأوامر
    if args.command == "add":
        controller.add_task(args)

    elif args.command == "list":
        tasks = controller.list_all_task() if args.all else controller.list_task()
        controller.print_table(tasks)

    elif args.command == "done":
        controller.mark_done(args.task_id)

    elif args.command == "cancel":
        controller.cancel_task(args.task_id)

    elif args.command == "filter":
        filtered = controller.filter_tasks(args.priority)
        controller.print_table(filtered)

    elif args.command == "stats":
        controller.show_stats()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
