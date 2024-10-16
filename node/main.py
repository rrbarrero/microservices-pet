from typing import Optional
from fastapi import Depends, FastAPI
from domain.task import Task
from repos.in_memory_repo import TaskInMemoryRepository
from service.gateway_service import GatewayService
from service.task_service import TaskService
from pydantic import BaseModel


app = FastAPI()

#TODO: put in tear up and tear down methods
GatewayService().register()

def get_api_url_with_prefix(subfix: str) -> str:
    return f"/api/v1{subfix}"


class TaskPayload(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


def create_task_service() -> TaskService:
    return TaskService(repo=TaskInMemoryRepository())


@app.get(get_api_url_with_prefix("/health"))
async def health_check():
    return {"status": "ok"}


@app.post(get_api_url_with_prefix("/tasks"), status_code=201)
async def create_task(payload: TaskPayload, service: TaskService = Depends(create_task_service)):
    new_task = Task.create(id=None, **payload.model_dump())

    await service.save(new_task)

    return {"message": "Task created successfully"}


@app.get(get_api_url_with_prefix("/tasks"))
async def get_tasks(service: TaskService = Depends(create_task_service)) -> list[Task]:
    return await service.get_all()