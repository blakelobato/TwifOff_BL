# TwifOff_BL
A web application for comparing twitter users and which user is more likely to tweet a given string of text.

```sh
pipenv install --python 3.7

pipenv install Flask Flask-SQLAlchemy Flask-Migrate

pipenv shell
```

```sh
cd TwifOff_BL
FLASK_APP=app.py flask db init #generates app/migrations dir

FLASK_APP=app.py flask db migrate #creates the db (with "alembic_version" table)
FLASK_APP=app.py flask db upgrade #creates the "users" table

FLASK_APP=app.py flask run 
```

## RUN

```sh
FLASK_APP=app.py flask run 
```
