FROM python:3.9-alpine3.13
LABEL maintainer="Tonny-Bright Sogli"

ENV PYTHONUNBUFFERED 1

WORKDIR /opt/slightlytech

COPY ./requirements.txt /tmp/requirements.txt
COPY . /opt/slightlytech/

# COPY .env /opt/slightlytech/.env

# copy entrypoint.sh
COPY ./entrypoint.sh /opt/slightlytech/entrypoint.sh
RUN sed -i 's/\r$//g' /opt/slightlytech/entrypoint.sh
RUN chmod +x /opt/slightlytech/entrypoint.sh

EXPOSE 8041

ENV DATABASE=postgres

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
    then /py/bin/pip install -r /tmp/requirements.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
    --disabled-password \
    --no-create-home \
    django-user

ENV PATH="/py/bin:$PATH"

USER django-user

ENTRYPOINT ["/opt/slightlytech/entrypoint.sh"]
