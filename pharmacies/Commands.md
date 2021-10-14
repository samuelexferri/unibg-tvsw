# Commands

Path:

```bash
$ cd C:/GitHub/tvsw/pharmacies
```

Virtual Environment:

```bash
$ pip install virtualenvwrapper-win
$ mkvirtualenv -p python3.7.7 venv_pharmacies
$ workon venv_pharmacies
$ rmvirtualenv venv_pharmacies
```

PIP:

```bash
$ python -m pip install --upgrade pip
$ pip install --upgrade setuptools
```

Requirements:

```bash
$ pip freeze > requirements.txt
$ pip install -r requirements.txt
```

Django:

```bash
$ python manage.py createsuperuser
$ python manage.py migrate
$ python manage.py migrate --run-syncdb
$ python manage.py makemigrations
$ python manage.py runserver
```

Data:

Delete the `db.sqlite3` file to avoid conflicts; run migrate and create your own superuser admin and re-run migrate; then import the `db.json` with the commands below and start the server again.

```bash
$ python manage.py dumpdata > db.json
$ python manage.py loaddata db.json
```

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
$ pip install coverage
$ coverage run --source ./ manage.py test -v 2 --exclude-tag=selenium
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

Require to uninstall `pytest` and to comment Selenium test

```bash
$ pip install django-mutpy
$ python manage.py muttest shop
```

Selenium:

Requires `Firefox` and `geckodriver.exe`

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

icontract:

```bash
$ pip install icontract
```

mypy, django-stub:

```bash
$ pip install mypy
$ pip install django-stub
$ mypy -p shop
```

pylint:

```bash
$ pip install pylint
$ pip install pylint-django
$ pylint --rcfile=./.pylintrc ./shop
$ pylint --rcfile=./.pylintrc --errors-only ./shop
$ pylint --rcfile=./.pylintrc --load-plugins pylint_django --load-plugins pylint_django.checkers.db_performance ./shop
$ pylint --rcfile=./.pylintrc ./shop --exit-zero
```

flake8:

```bash
$ pip install flake8
$ flake8 -v --count
$ flake8 -v --count --ignore=E501,F405
```

bandit:

```bash
$ pip install bandit
$ bandit -r -v .
```

pyreverse:

```bash
$ pip install pyreverse
$ pyreverse -o png -A -s 0 -a 0 -k authentication  shop timetable transfer --ignore=migrations,tests,tests.py
$ pyreverse -o png -A -s 0 -a 0 -k  shop --ignore=migrations,tests,tests.py
```

GraphViz:

Install GraphViz (visit the site) and add the the path `bin\gvedit.exe` in the environment variables path

```bash
$ python manage.py graph_models -a -o models.png
$ python manage.py graph_models authentication shop timetable transfer -o apps.png
```

CPD:

Install PMD-CPD

```bash
$ cpd --minimum-tokens 75 --files C:/GitHub/tvsw/pharmacies --language python
```

black:

```bash
$ pip install black
$ black . --line-length 79 --check
$ black . --line-length 79
```

### Users

Account: cliente1 (ginopino), farmacista1 (ginopino), admin (admin)
