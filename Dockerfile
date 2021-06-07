FROM python:3.8

ENV PYTHONUNBUFFERED 1

ENV DJANGO_SETTINGS_MODULE=settings.settings_dev
ENV DJANGO_SECRET="dsnjkcdslcndscjkejerbjrebgerhgberincdsnc21e1232"
ENV POSTGRES_DB=app
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=supersecretpassword

RUN mkdir /app
WORKDIR /app

ADD . /app/

RUN pip install --upgrade pip \
&& pip install --no-cache-dir -r requirements.txt

CMD  ["tail", "-f", "/dev/null"]

