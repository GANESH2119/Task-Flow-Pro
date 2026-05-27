import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.prompt import Prompt
from rich.align import Align
from rich.text import Text

console = Console()

# Load tasks from JSON
try:
    with open("tasks.json", "r") as file:
        tasks = json.load(file)
except:
    tasks = []

while True:

    # Header
    title = Text("🚀 TaskFlow Pro", style="bold green")
    subtitle = Text("Smart Task Management System", style="white")

    console.print(
        Panel.fit(
            Align.center(f"{title}\n{subtitle}"),
            border_style="green",
            padding=(1, 5)
        )
    )

    # Menu
    menu = Table(
        title="📋 MAIN MENU",
        box=box.DOUBLE_EDGE,
        border_style="cyan"
    )

    menu.add_column("Option", justify="center", style="bold cyan")
    menu.add_column("Feature", style="bold green")

    menu.add_row("1", "➕ Add Task")
    menu.add_row("2", "📋 View Tasks")
    menu.add_row("3", "✅ Complete Task")
    menu.add_row("4", "❌ Delete Task")
    menu.add_row("5", "📊 Statistics")
    menu.add_row("6", "🚪 Exit")

    console.print(menu)

    choice = Prompt.ask("\n[bold yellow]Choose Option[/bold yellow]")

    # ================= ADD TASK =================
    if choice == "1":

        console.print("\n[bold cyan]━━━━━━━━ ADD NEW TASK ━━━━━━━━[/bold cyan]\n")

        task_name = Prompt.ask("📝 Enter Task")
        priority = Prompt.ask(
            "🔥 Priority (High/Medium/Low)"
        )
        due_date = Prompt.ask("📅 Due Date")

        task = {
            "task": task_name,
            "priority": priority,
            "due": due_date,
            "status": "⌛ Pending"
        }

        tasks.append(task)

        with open("tasks.json", "w") as file:
            json.dump(tasks, file, indent=4)

        console.print(
            "\n[bold green]✅ Task Added Successfully![/bold green]\n"
        )

    # ================= VIEW TASKS =================
    elif choice == "2":

        table = Table(
            title="📋 ALL TASKS",
            box=box.ROUNDED,
            border_style="green"
        )

        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Task", style="bold white")
        table.add_column("Priority", style="yellow")
        table.add_column("Due Date", style="magenta")
        table.add_column("Status", style="green")

        for index, task in enumerate(tasks, start=1):

            priority_style = task["priority"]

            if priority_style.lower() == "high":
                priority_style = "🔥 High"

            elif priority_style.lower() == "medium":
                priority_style = "⭐ Medium"

            else:
                priority_style = "🟢 Low"

            table.add_row(
                str(index),
                task["task"],
                priority_style,
                task["due"],
                task["status"]
            )

        console.print(table)

    # ================= COMPLETE TASK =================
    elif choice == "3":

        task_id = int(
            Prompt.ask("✅ Enter Task ID to mark as completed")
        )

        if 0 < task_id <= len(tasks):

            tasks[task_id - 1]["status"] = "✅ Completed"

            with open("tasks.json", "w") as file:
                json.dump(tasks, file, indent=4)

            console.print(
                "\n[bold green]🎉 Task Completed Successfully![/bold green]\n"
            )

        else:
            console.print(
                "\n[bold red]⚠ Invalid Task ID![/bold red]\n"
            )

    # ================= DELETE TASK =================
    elif choice == "4":

        task_id = int(
            Prompt.ask("❌ Enter Task ID to delete")
        )

        if 0 < task_id <= len(tasks):

            deleted_task = tasks.pop(task_id - 1)

            with open("tasks.json", "w") as file:
                json.dump(tasks, file, indent=4)

            console.print(
                f"\n[bold red]🗑 Deleted: {deleted_task['task']}[/bold red]\n"
            )

        else:
            console.print(
                "\n[bold red]⚠ Invalid Task ID![/bold red]\n"
            )

    # ================= STATISTICS =================
    elif choice == "5":

        total_tasks = len(tasks)

        completed_tasks = sum(
            1 for task in tasks
            if task["status"] == "✅ Completed"
        )

        pending_tasks = total_tasks - completed_tasks

        stats = Table(
            title="📊 TASK ANALYTICS",
            box=box.HEAVY,
            border_style="blue"
        )

        stats.add_column("Type", style="cyan")
        stats.add_column("Count", style="green")

        stats.add_row("📋 Total Tasks", str(total_tasks))
        stats.add_row("✅ Completed", str(completed_tasks))
        stats.add_row("⌛ Pending", str(pending_tasks))

        console.print(stats)

    # ================= EXIT =================
    elif choice == "6":

        console.print(
            "\n[bold red]🚪 Exiting TaskFlow Pro...[/bold red]\n"
        )

        break

    # ================= INVALID OPTION =================
    else:

        console.print(
            "\n[bold red]⚠ Invalid Option![/bold red]\n"
        )