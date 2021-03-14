# https://github.com/tiangolo/uvicorn-gunicorn-docker
FROM python:3.7

RUN apt-get update -y
RUN apt-get install python3-pip -y

COPY ./dependencies/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./scripts .
RUN chmod +x /start.sh /start-reload.sh

COPY ./configs/gunicorn_conf.py /gunicorn_conf.py

COPY ./app /app
WORKDIR /app/

ENV PYTHONPATH=/app

EXPOSE 80

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/start.sh"]