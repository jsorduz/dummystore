FROM python:3.10.8-alpine
LABEL maintainer="jorduz"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements_runtime.txt /tmp/requirements_runtime.txt


RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    /py/bin/pip install -r /tmp/requirements_runtime.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol

COPY . /app/
WORKDIR /app
RUN chmod -R +x /app/scripts
ENV PATH="/app/scripts:/py/bin:$PATH"

USER django-user

CMD ["run.sh"]
