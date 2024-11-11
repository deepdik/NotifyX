# syntax=docker/dockerfile:1

FROM python:3.11

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

ENV ENV=DEV
RUN apt-get install -y libgdal-dev
RUN apt-get install -y cron
RUN apt-get install -y vim nano

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# Add cron job
RUN echo "* * * * * root python /app/manage.py runcrons --force >> /var/log/cron.log 2>&1" >> /etc/crontab

# Start the cron service and Django
CMD service cron start && python manage.py runserver 0.0.0.0:8010
