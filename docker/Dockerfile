FROM python:3.7-alpine3.11

RUN apk update && \
    apk upgrade

RUN apk add postgresql-dev \
            python-dev \
            py-pip \
            build-base \
            libffi-dev \
            openssl-dev \
            libgcc \
            gcc \
            libc-dev \
            libxml2-dev \
            libxslt-dev \
            wkhtmltopdf \
            xvfb-run

WORKDIR /app

#ADD requirements.txt /app
#RUN pip install -r requirements.txt

ADD . /app

EXPOSE 5000

# Vestige from DKS
#CMD [ "python", "./manage.py", "run"]