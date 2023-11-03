FROM python:3.11.5

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Встановлення необхідних пакетів, включаючи netcat
RUN apt-get update && \
    apt-get install -y libpq-dev netcat-traditional && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
