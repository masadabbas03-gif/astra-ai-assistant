from memory_manager.memory_loader import load_tasks


def search_task(keyword):
    tasks = load_tasks()
    results = []

    for task in tasks:
        if keyword.lower() in str(task).lower():
            results.append(task)

    return results