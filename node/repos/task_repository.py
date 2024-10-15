from typing import Protocol

from domain.task import Task


class TaskRepository(Protocol):

    async def save(self, task: Task):
        ...

    async def get_all(self) -> list[Task]:
        ...