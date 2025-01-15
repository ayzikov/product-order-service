# Используем официальный образ Python как базовый
FROM python:3.11

# это переменная окружения, которая означает, что Python не будет пытаться создавать файлы .pyc
ENV PYTHONDONTWRITEBYTECODE 1

# выходные данные python, т.е. потоки stdout и stderr, отправляются прямо на терминал
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости проекта в контейнер
COPY requirements.txt ./

# Устанавливаем зависимости проекта
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код проекта в контейнер
COPY . .
