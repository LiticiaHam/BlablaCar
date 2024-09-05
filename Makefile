
.PHONY: build up down logs tests web db redis swagger flower


build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f


load_airports_airlines:
	docker compose run --rm loader python -m src.loader.00_get_airports_and_airlines

load_data:
	docker compose run --rm loader python -m src.loader.01_get_all_flights

load_schedule:
	docker compose run --rm loader python -m src.loader.02_get_all_flights_every_hour

hello-world:
	docker compose run --rm loader python -m src.loader.hello_world

jupyter:
	open http://localhost:8888/

hadoop:
	open http://localhost:9870/