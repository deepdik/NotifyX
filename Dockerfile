FROM python:3.11

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN apt-get update && \
    apt-get install -y libgdal-dev cron vim nano

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# Add cron job (optional, you handle it separately)
RUN echo "* * * * * root python /app/manage.py runcrons --force >> /var/log/cron.log 2>&1" >> /etc/crontab

CMD service cron start && \
    python manage.py migrate && \
    python manage.py runserver 0.0.0.0:8010
#     gunicorn config.wsgi:application --bind 0.0.0.0:8010 --workers 4 --threads 4 --timeout 60 --reload