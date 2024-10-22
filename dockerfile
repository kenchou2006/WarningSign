FROM python:3.12-slim

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

ENV DJANGO_SETTINGS_MODULE=server.settings

EXPOSE 5000

CMD ["gunicorn", "server.wsgi:application", "--bind", "0.0.0.0:80"]
