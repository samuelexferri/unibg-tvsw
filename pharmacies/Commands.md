# Commands

Code Path:

```bash
$ cd C:\GitHub\tvsw\pharmacies
```

Upgrade pip:

```bash
$ python -m pip install --upgrade pip
```

Virtual Environment:

```bash
$ pip3 install virtualenvwrapper-win
$ mkvirtualenv my_django_environment
$ workon my_django_environment
$ rmvirtualenv  my_django_environment # Delete the envrironment!
```

Requirements:

```bash
$ pip freeze > requirements.txt
$ pip install -r requirements.txt
```

Data:

Delete the `db.sqlite3` file to avoid conflicts; run migrate and create your own superuser admin and re-run migrate; then import the `db.json` with the commands below and start the server again.

```bash
$ python manage.py dumpdata > db.json
$ python manage.py loaddata db.json
```

Commands:

```bash
$ python manage.py createsuperuser
$ python manage.py migrate
$ python manage.py migrate --run-syncdb
$ python manage.py makemigrations
$ python manage.py runserver
```

### REST API

Swagger UI:

```bash
$ pip install django-rest-swagger
```

### Code Testing

unittests:

```bash
$ python manage.py test -v 2 --exclude-tag=selenium
```

parameterized:

```bash
$ pip install parameterized
```

coverage:

```bash
$ coverage run manage.py test -v 2 --exclude-tag=selenium
$ coverage report
$ coverage html
$ coverage xml
$ coverage erase
```

Codecov:

```bash
Site
```

django-mutpy:

```bash
$ pip install django-mutpy
$ python manage.py muttest shop  # Remember to disable Selenium
```

Selenium:

```bash
$ pip install selenium
$ pip install lxml
$ pip install defusedxml
```

mock:

```bash
$ pip install mock
```

### Code Verification

pyreverse:

```bash
$ pyreverse -o png -A -s 0 -a 0 -k authentication  shop timetable transfer --ignore=migrations,tests,tests.py
$ pyreverse -o png -A -s 0 -a 0 -k  shop --ignore=migrations,tests,tests.py
```

GraphViz: install GraphViz (visit the site) and add the the path `bin\\gvedit.exe` in the environment variables path.

```bash
$ python manage.py graph_models -a -o models.png
$ python manage.py graph_models authentication shop timetable transfer -o apps.png
```

pylint:

```bash
$ pylint --rcfile=./.pylintrc  ./shop
$ pylint --rcfile=./.pylintrc --errors-only ./shop
$ pylint --rcfile=./.pylintrc --load-plugins pylint_django --load-plugins pylint_django.checkers.db_performance ./shop
```

black:

```bash
$ black . --check
$ black .
```
