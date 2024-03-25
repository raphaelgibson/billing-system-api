FROM python:3.12.2-slim-bullseye

WORKDIR /usr/src/app
COPY ./requirements.txt ./requirements.txt

RUN python -m pip install -U pip
RUN pip install -r requirements.txt

COPY . .

CMD exec gunicorn -b :8080 app.main.server:app -w 5 -k uvicorn.workers.UvicornWorker
