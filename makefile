.PHONY: e2e

up:
	docker-compose up --build --scale node_service=4 etcd gateway node_service

build:
	docker-compose build --no-cache

test:
	docker-compose run --rm node_service pytest
	docker-compose run --rm gateway pytest

post:
	@curl -X POST "http://localhost:8000/api/v1/tasks" \
		-H "Content-Type: application/json" \
		-d "{\"title\": \"Test Task\", \"description\": \"This is a test task\", \"completed\": false}"

e2e:
	docker-compose up -d --build --scale node_service=2 etcd gateway node_service
	sleep 20
	docker-compose run --rm e2e
	docker-compose down