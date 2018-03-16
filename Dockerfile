FROM python:2

MAINTAINER Schemen <me@schemen.me>

EXPOSE 8000

ENV DEBUG=False
ENV IMPORT=False
ENV AUTH_KEY=None
ENV AUTH_SECRET=None

WORKDIR /usr/src/app

COPY ./docker-entrypoint.sh /

ENTRYPOINT ["/docker-entrypoint.sh"]

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    wget https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2 && \
    bunzip2 sqlite-latest.sqlite.bz2 && mv sqlite-latest.sqlite evesde.db && \
    mkdir data/

COPY . .

VOLUME /usr/src/app/data

CMD [ "uwsgi", "--ini", "app.ini" ]
