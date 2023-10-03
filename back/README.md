# BeerBrain - Back-end

BeerBrain back-end server uses Django with Django REST framework.
Minimal support version of Python is 3.11.

## Quickstart

Go to `back` directory:

```shell
cd back
```

Set virtual environment:

```shell
python3.11 -m virtualenv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Make Django migrations and run server:

```shell
cd src
python manage.py migrate
python manage.py runserver
```

Then you can run front-end application.
