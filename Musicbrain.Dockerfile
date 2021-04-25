# Adapted from https://www.digitalocean.com/community/tutorials/how-to-build-and-deploy-a-flask-application-using-docker-on-ubuntu-18-04
FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine-2020-12-19

RUN apk --update add bash 

ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static

COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt