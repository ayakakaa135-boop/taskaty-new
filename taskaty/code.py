from argparse import ArgumentParser
from taskaty.task_controller import TaskController


def main():
    controller = TaskController("tasks.json")
    parser = ArgumentParser(description="📝 Taskaty CLI - Manage your tasks easily")
    subparsers = parser.add_subparsers(dest="command")

    # 📊 show stats
    subparsers.add_parser("stats", help="Show task statistics")

    # ➕ add
    add_task = subparsers.add_parser("add", help="Add a new task")
    add_task.add_argument("title", help="Task title")
    add_task.add_argument("-d", "--description", help="Task description")
    add_task.add_argument("-s", "--start_date", help="Start date (YYYY-MM-DD)")
    add_task.add_argument("-e", "--end_date", help="End date (YYYY-MM-DD)")
    add_task.add_argument("-p", "--priority", help="Priority (high/low)", default="low")

    # 📋 list
    subparsers.add_parser("list", help="List all tasks")

    # ✅ mark done
    done_task = subparsers.add_parser("done", help="Mark task as done")
    done_task.add_argument("task_id", type=int, help="Task ID")

    # 🚫 cancel
    cancel_task = subparsers.add_parser("cancel", help="Cancel a task")
    cancel_task.add_argument("task_id", type=int, help="Task ID")

    # 🔍 filter by priority
    filter_task = subparsers.add_parser("filter", help="Filter tasks by priority")
    filter_task.add_argument("priority", choices=["high", "low"], help="Priority level")

    args = parser.parse_args()

    if args.command == "add":
        controller.add_task(args)
    elif args.command == "list":
        controller.list_all_tasks()
    elif args.command == "done":
        controller.mark_done(args.task_id)
    elif args.command == "cancel":
        controller.cancel_task(args.task_id)
    elif args.command == "filter":
        controller.filter_by_priority(args.priority)
    elif args.command == "stats":
        controller.show_stats()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
