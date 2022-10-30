include .env

env_file = --env-file .env

help:
	@echo "Makefile commands:"
	@echo "stop"
	@echo "restart"
	@echo "destroy"
build:
	docker-compose --profile notifications -f docker-compose.yml build -d $(c)
	docker-compose --profile notifications -f docker-compose.yml up -d $(c)
stop:
	docker-compose -f docker-compose.yml stop $(c)
restart:
	docker-compose -f docker-compose.yml stop $(c)
	docker-compose -f docker-compose.yml up -d $(c)
destroy:
	docker system prune -f --volumes $(c)
admin_build:
	docker-compose exec admin python manage.py migrate
	docker-compose exec admin python manage.py collectstatic
admin_superuser:
	docker-compose exec admin python manage.py createsuperuser
