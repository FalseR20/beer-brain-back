FROM python:3.11-slim-buster

# Установите рабочую директорию в /app
WORKDIR /app

# Установите переменные окружения, необходимые для Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установите зависимости
RUN apt-get update \
  && apt-get install -y build-essential \
  && apt-get install -y python3-dev libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Установите зависимости проекта
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируйте текущий каталог в рабочую директорию /app
COPY . .

# Запустите команду для запуска вашего приложения
CMD ["gunicorn", "beer_brain.wsgi"]
