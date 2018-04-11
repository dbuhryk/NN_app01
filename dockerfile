FROM alpine:latest

#####################################
RUN apk add --update \
    python3 \
    supervisor \
    tzdata

RUN apk add --update \
	build-base \
	python3-dev \
	g++ \
	gcc \
	ca-certificates \
	git

RUN pip3 install --upgrade pip

RUN pip3 install \
	flask \
	markdown \
	coverage

RUN rm -rf /var/cache/apk/*

#####################################
RUN cp /usr/share/zoneinfo/Europe/Prague /etc/localtime && \
    echo "Europe/Prague" > /etc/timezone

#####################################
ADD . /app

RUN cd /app &&\
	python3 -m coverage run /app/setup.py test &&\
	python3 -m coverage report -m &&\
	python3 /app/setup.py install &&\
	python3 /app/setup.py clean --all

RUN rm -rf /app/*

#####################################
RUN mkdir -p  /app/app01/

RUN cd /app/ && \
    GIT_HASH=$(git rev-parse --short HEAD) && \
    echo "GIT_HASH = '$GIT_HASH'" > /app/app01/config.cfg

RUN head -c 24 /dev/urandom > /app/app01/secret_key

#####################################
COPY supervisord.conf /etc/supervisor/supervisord.conf

RUN mkdir -p /var/log/flask

COPY supervisord_flask.conf /etc/supervisor/supervisor.d/
#####################################
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf" ]
#####################################

EXPOSE 8080