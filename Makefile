build:
	@docker compose build

run:
	@docker compose up server

test:
	@docker compose up tests