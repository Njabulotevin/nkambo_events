start:
	flask --app run run --debug --port=8080

start-production:
	gunicorn app:run

setup:
	bash setup.sh

uninstall:
	bash uninstall.sh

activate:
	source venv/bin/activate

venv:
	python3 -m venv ./venv