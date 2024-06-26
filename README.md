# BeerBrain - Back-end

BeerBrain back-end server uses Django with the Django REST framework.

## Quickstart

### Set pipenv virtual environment

Minimal support version of Python is 3.11.

```shell
pipenv sync
pipenv shell
```

### Setting database

Project uses PostgreSQL

```shell
sudo -u postgres psql
```

```postgresql
CREATE DATABASE beer_brain;
CREATE USER beer_brain WITH ENCRYPTED PASSWORD 'YOUR_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE beer_brain TO beer_brain;
ALTER ROLE beer_brain CREATEDB; -- for testing
```

You need to create `.env` file:

```dotenv
POSTGRES_DB=beer_brain
POSTGRES_USER=beer_brain
POSTGRES_PASSWORD=YOUR_PASSWORD
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### Migrations and superuser

```shell
./manage.py migrate
./manage.py createsuperuser
```

### Running

```shell
./manage.py runserver --noreload 
```

Then you can run [front-end application](https://github.com/FalseR20/beer-brain-front).

### Deploy

You need to create `.env.prod` file:

```dotenv
POSTGRES_DB=beer_brain
POSTGRES_USER=beer_brain
POSTGRES_PASSWORD=YOUR_PASSWORD
POSTGRES_HOST=postgres
```

and `.env` file:
```dotenv
VITE_DJANGO_URL=YOUR_VITE_URL
```

Then use docker compose (remember to migrate)
