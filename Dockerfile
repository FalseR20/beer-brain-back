FROM python:3.11.9-slim AS builder

WORKDIR /usr/src/

ENV PIPENV_VENV_IN_PROJECT=1

RUN apt-get update \
  && apt-get install -y build-essential \
  && apt-get install -y python3-dev libpq-dev \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install pipenv

ADD Pipfile Pipfile.lock /usr/src/
RUN python3 -m pipenv sync


FROM python:3.11.9-slim as main

WORKDIR /usr/src/

RUN mkdir -v /usr/src/.venv

COPY --from=builder /usr/src/.venv/ /usr/src/.venv/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

CMD ["./.venv/bin/python", "-m", "gunicorn", "beer_brain.wsgi"]
