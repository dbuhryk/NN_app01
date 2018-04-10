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
	gcc

RUN pip3 install --upgrade pip

RUN pip3 install \
	flask \
	markdown

RUN rm -rf /var/cache/apk/*

#####################################
RUN cp /usr/share/zoneinfo/Europe/Prague /etc/localtime && \
    echo "Europe/Prague" > /etc/timezone

#####################################
ADD app01 /app/app01

ADD test /app/test

ADD setup.py /app

RUN cd /app &&\
	python3 /app/setup.py install

RUN rm -rf /app

#####################################
COPY supervisord.conf /etc/supervisor/supervisord.conf

RUN mkdir -p /var/log/flask

COPY supervisord_flask.conf /etc/supervisor/supervisor.d/
#####################################
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf" ]
#####################################

EXPOSE 8080