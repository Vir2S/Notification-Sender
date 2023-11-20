.PHONY: up \
		run \
		build \
		stop \
		restart \
		down

up: ## Up
	docker-compose up
run: ## Run
	docker-compose up -d
build: ## Build
	docker-compose up --build
stop: ## Stop
	docker-compose stop
restart: ## Restart
	docker-compose restart
down: ## Down
	docker-compose down
