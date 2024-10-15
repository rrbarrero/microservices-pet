up:
	docker-compose up --build --scale node_service=2

build:
	docker-compose build --no-cache

test:
	docker-compose run --rm node_service pytest

post:
	@curl -X POST "http://localhost:8000/api/v1/tasks" \
		-H "Content-Type: application/json" \
		-d "{\"title\": \"Test Task\", \"description\": \"This is a test task\", \"completed\": false}"

