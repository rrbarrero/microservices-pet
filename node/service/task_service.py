from repos.task_repository import TaskRepository


class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def save(self, task):
        await self.repo.save(task)

    async def get_all(self) -> list:
        return await self.repo.get_all()