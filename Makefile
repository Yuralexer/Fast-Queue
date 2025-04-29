.PHONY: fix
fix:
	isort .
	ruff check --fix

.PHONY: lint
lint:
	ruff check
	isort -qc .

.PHONY: test
test:
	python manage.py test

.PHONY: testapp
testapp:
	python manage.py test $(app)

.PHONY: check
check: lint test

.PHONY: runserver
runserver:
	python manage.py runserver

.PHONY: startapp
startapp:
	python manage.py startapp $(app)

.PHONY: makemigrations
makemigrations:
	python manage.py makemigrations

.PHONY: migrate
migrate:
	python manage.py migrate

.PHONY: shell
shell:
	python manage.py shell

.PHONY: createadmin
createadmin:
	python manage.py createsuperuser