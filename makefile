up:
	docker-compose up -d
	docker-compose logs -f

build:
	docker-compose build --no-cache


test:
	docker-compose run --rm node pytest