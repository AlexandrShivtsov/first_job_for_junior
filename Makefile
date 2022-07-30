cdSHELL := /bin/bash

manage_py := python app/manage.py

runserver:
	$(manage_py) runserver

worker:
	cd app && celery -A settings worker -l info --autoscale=5,1
	#cd app && celery -A settings worker -l info --concurrency 10

beat:
	cd app && celery -A settings beat -l info

shell:
	$(manage_py) shell_plus

show_urls:
	$(manage_py) show_urls

makemigrations:
	$(manage_py) makemigrations

migrate:
	$(manage_py) migrate

rabbitmq:
	sudo service rabbitmq-server start

gunicorn:
	 cd app && gunicorn settings.wsgi:application --workers 4 --bind 0.0.0.0:8000 --timeout 5 --max-requests 10000



    	
