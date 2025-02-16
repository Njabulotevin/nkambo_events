start:
	flask --app run app --debug --port=8080

start-production:
	gunicorn app:app

setup:
	bash setup.sh

uninstall:
	bash uninstall.sh

activate:
	source venv/bin/activate

venv:
	python3 -m venv ./venv