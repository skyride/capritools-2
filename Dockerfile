FROM python:2.7

WORKDIR /app

RUN apt-get update && \
    apt-get install gcc
RUN pip install --no-cache-dir gunicorn

COPY requirements.txt /app
RUN pip install -r requirements.txt

# Copy files
COPY . .
COPY capritools/docker_settings.py capritools/local_settings.py

# Ops Parameters
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV WORKERS=2
ENV THREADS=1

CMD gunicorn -w ${WORKERS} -t ${THREADS} -b 0.0.0.0:${PORT} capritools.wsgi:application
