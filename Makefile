

start: 
	@docker compose up -d

restart: 
	@docker compose stop && docker compose up -d