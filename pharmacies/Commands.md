# COMMANDS

Command Prompt

Pip:
$ python -m pip install --upgrade pip

Virtual Environment:
$ pip3 install virtualenvwrapper-win
$ mkvirtualenv my_django_environment
$ workon my_django_environment
$ rmvirtualenv  my_django_environment

Requirements:
$ pip freeze > requirements.txt
$ pip install -r requirements.txt

Dump data:
Cancellare il file db.sqlite3 per evitare conflitti; a terminale eseguire migrate e creare il proprio superuser admin e rieseguire migrate; successivamente importare il db.json con il comandi sottostanti ed avviare il server nuovamente.
$ python manage.py dumpdata > db.json
$ python manage.py loaddata db.json

Generale:
$ python manage.py createsuperuser
$ python manage.py migrate
$ python manage.py migrate --run-syncdb
$ python manage.py makemigrations
$ python manage.py runserver

API
Swagger:
$ pip install django-rest-swagger

ANALISI STATICA
Pyreverse:
$ pyreverse -o png -A -s 0 -a 0 -k authentication  shop timetable transfer --ignore=migrations,tests,tests.py
$ pyreverse -o png -A -s 0 -a 0 -k  shop --ignore=migrations,tests,tests.py

GraphViz:
Install GraphViz (Visit the site) and add the the path for bin\\gvedit.exe in path (Environment variables)
$ python manage.py graph_models -a -o myapp_models.png
$ python manage.py graph_models authentication shop timetable transfer -o apps.png

Plyint:
$ pylint --rcfile=./.pylintrc  ./shop
$ pylint --rcfile=./.pylintrc --errors-only ./shop
$ pylint --rcfile=./.pylintrc --load-plugins pylint_django --load-plugins pylint_django.checkers.db_performance ./shop

ANALISI DINAMICA
Testing (Unit Test)

Coverage:
$ coverage run manage.py test -v 2
$ coverage html
$ coverage erase

Selenium: (Firefox necessario e geckodriver.exe)
$ pip install selenium
$ pip install lxml
$ pip install defusedxml
