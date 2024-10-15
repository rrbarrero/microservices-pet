from dataclasses import dataclass
import datetime
from typing import Optional


@dataclass
class Task:
    id: int | None
    title: str
    created_at: float
    description: Optional[str] = None
    completed: bool = False

    @classmethod
    def create(cls, id: int | None, title: str, description: Optional[str], completed: bool):
        created_at = datetime.datetime.now().timestamp()
        return cls(id, title,created_at, description, completed)

