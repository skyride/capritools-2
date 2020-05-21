FROM python:2.7

WORKDIR /app

RUN apt-get update && \
    apt-get install gcc
RUN pip install --no-cache-dir uWSGI==2.0.18

COPY requirements.txt /app
RUN pip install -r requirements.txt

# Copy files
COPY . .
COPY capritools/docker_settings.py capritools/local_settings.py

# Collectstatic
RUN ./manage.py collectstatic

# Ops Parameters
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV WORKERS=2

CMD uwsgi --http :${PORT} --processes ${WORKERS} --static-map /static=/static --module capritools.wsgi:application
