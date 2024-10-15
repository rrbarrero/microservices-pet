from domain.task import Task


class TaskInMemoryRepository:
    def __init__(self, initial_data: list[Task] = []):
        self.tasks: list[Task] = initial_data

    async def save(self, task: Task):
        if task.id is None:
            task.id = len(self.tasks) + 1
        self.tasks.append(task)

    async def get_all(self) -> list[Task]:
        return self.tasks.copy()

