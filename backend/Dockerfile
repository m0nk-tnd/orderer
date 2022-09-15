# pull official base image
FROM python:3.7.9-slim-buster

# set work directory
ENV APP_DIR /usr/src/app
WORKDIR $APP_DIR

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Options: api, grabber
ARG ENV_NAME

# install dependencies
RUN pip install --upgrade pip

COPY ./$ENV_NAME/requirements.txt $APP_DIR/
RUN pip install -r requirements.txt

# copy project
COPY ./ $APP_DIR/
ENV SCRIPT_PATH $ENV_NAME.main

ENTRYPOINT python -m $SCRIPT_PATH
