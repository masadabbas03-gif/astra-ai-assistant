from memory_manager.load_memory import load_tasks


def search_task(keyword):

    tasks = load_tasks()

    results = []

    for task in tasks:

        if keyword.lower() in task.lower():

            results.append(task)

    return results