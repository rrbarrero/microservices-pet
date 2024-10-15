from typing import Optional
from fastapi import Depends, FastAPI
from domain.task import Task
from repos.in_memory_repo import TaskInMemoryRepository
from service.task_service import TaskService
from pydantic import BaseModel


app = FastAPI()

def get_api_url_with_prefix(subfix: str) -> str:
    return f"/api/v1{subfix}"


class TaskPayload(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


def create_task_service() -> TaskService:
    return TaskService(repo=TaskInMemoryRepository())


@app.post(get_api_url_with_prefix("/tasks"), status_code=201)
async def create_task(payload: TaskPayload, service: TaskService = Depends(create_task_service)):
    new_task = Task.create(id=None, **payload.model_dump())

    await service.save(new_task)

    return {"message": "Task created successfully"}