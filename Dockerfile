FROM alpine:edge
MAINTAINER Norman Denayer <denayer.norman@gmail.com>

RUN set -x && \
    mkdir /app

COPY requirements.txt /app/    

RUN set -x && apk add --update python3 python3-dev musl-dev gcc ca-certificates

RUN set -x && \
    python3 -m pip install -r /app/requirements.txt && \
    apk del python3-dev musl-dev gcc

COPY . /app

EXPOSE 8180
VOLUME "/app/config"
VOLUME "/var/log/http_redirect"

WORKDIR "/app"
CMD ["/usr/bin/python3", "-m http_redirect.__init__"]
