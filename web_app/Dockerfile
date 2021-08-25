# pull official base image
FROM python:3.7.6-alpine

# set work directory
WORKDIR /usr/web_app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY ./requirements.txt /usr/web_app/requirements.txt

# install dependencies
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
        libressl-dev libffi-dev gcc musl-dev python3-dev \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /usr/web_app/requirements.txt \
    && rm -rf /root/.cache/pip

# copy project
COPY . /usr/web_app/

# expose port used by fastapi to the outside world
EXPOSE 8181

# allow permissions for the .sh file
RUN chmod 744 /usr/web_app/run.sh

# actual command that executes the .sh file that runs the python program
CMD ["/usr/web_app/run.sh"]