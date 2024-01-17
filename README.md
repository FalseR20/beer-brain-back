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

Run backend server:

```shell
./manage.py runserver --noreload 
```

Or for visibility on the network:

```shell
./manage.py runserver --noreload 192.168.100.5:8000
```

Then you can run [front-end application](../front/).
