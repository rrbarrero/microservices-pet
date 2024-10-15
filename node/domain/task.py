from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    id: int | None
    title: str
    description: Optional[str] = None
    completed: bool = False

    @classmethod
    def create(cls, id: int | None, title: str, description: Optional[str], completed: bool):
        return cls(id, title, description, completed)

