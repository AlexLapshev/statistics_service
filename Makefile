test:
	@echo "Running pylint tests"
	@echo "===================="
	@echo "Starting docker containers"
	@docker-compose down
	@docker-compose up -d --remove-orphans
	@sleep 1
	@echo "===================="
	@echo "Running alembic migrations"
	@sleep 1
	@alembic upgrade head
	@echo "===================="
	@echo "Filling db"
	@python -m etc.fill_db
	@echo "===================="
	@echo "Running tests"
	@pytest tests
	@docker-compose down