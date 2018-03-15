FROM python:2

MAINTAINER Schemen <me@schemen.me>

WORKDIR /usr/src/app

COPY ./docker-entrypoint.sh /

ENTRYPOINT ["/docker-entrypoint.sh"]

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    wget https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2 && \
    bunzip2 sqlite-latest.sqlite.bz2 && mv sqlite-latest.sqlite evesda.db && \
    mkdir data/

VOLUME /usr/src/app/data

COPY . .

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
