build:
	docker-compose -p restaurantselection up -d --build --remove-orphans

container:
	docker exec -it restaurantselection bash

test:
	DJANGO_SETTINGS_MODULE=settings.test_settings pytest -v api/tests

shell:
	./manage.py shell_plus

run:
	./manage.py runserver 0:8000

makemigrations:
	./manage.py makemigrations

migrate:
	./manage.py migrate

createsuperuser:
	./manage.py createsuperuser