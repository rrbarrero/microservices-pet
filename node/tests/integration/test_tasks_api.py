import pytest
from fastapi.testclient import TestClient
from domain.task import Task
from repos.in_memory_repo import TaskInMemoryRepository
from service.task_service import TaskService
from main import app, create_task_service


class TestTaskApi:

    @classmethod
    def setup_class(cls):
        cls.client = TestClient(app)

    @pytest.mark.asyncio
    async def test_health_check(self):
        response = self.client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    @pytest.mark.asyncio
    async def test_create_task(self):
        def act(spy: TaskService):
            task_data = {
                "title": "Test Task",
                "description": "This is a test task",
                "completed": "false",
            }
            response = self.client.post("/api/v1/tasks", json=task_data)
            assert response.status_code == 201
            assert response.json() == {"message": "Task created successfully"}
            assert spy.repo.tasks[0] == Task(
                id=1,
                title="Test Task",
                created_at=spy.repo.tasks[0].created_at,
                description="This is a test task",
                completed=False,
            )

        return setup_test(act)
    
    @pytest.mark.asyncio
    async def test_get_tasks(self):
        def act(_: TaskService):
            response = self.client.get("/api/v1/tasks")
            assert response.status_code == 200
            assert response.json() == [
                {
                    "id": 1,
                    "title": "Test Task",
                    "created_at": 1729006358.355708,
                    "description": "This is a test task",
                    "completed": False,
                }
            ]

        initial_data = [Task(id=1, title="Test Task", 
                             created_at=1729006358.355708, 
                             description="This is a test task", 
                             completed=False)]
        return setup_test(act, initial_data)



def setup_test(act, initial_data: list[Task] = []):
    spy = TaskService(repo=TaskInMemoryRepository(initial_data))

    app.dependency_overrides[create_task_service] = lambda: spy

    act(spy)

    del app.dependency_overrides[create_task_service]
