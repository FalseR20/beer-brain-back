FROM python:3.11.9-slim

WORKDIR /usr/src/

ENV PIPENV_VENV_IN_PROJECT=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get install -y build-essential \
  && apt-get install -y python3-dev libpq-dev \
  && apt-get install -y pipenv \
  && rm -rf /var/lib/apt/lists/*

ADD Pipfile Pipfile.lock /usr/src/
RUN pipenv sync

COPY . .

EXPOSE 8000
CMD ["pipenv", "run", "gunicorn", "beer_brain.wsgi", "-b", "0.0.0.0:8000"]
