FROM python:3.7.15-alpine   
WORKDIR /worker 

COPY ["src/deployment/docker/worker/requirements.txt", "/worker/"]

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install -r requirements.txt

COPY ["src", "/worker/"]

CMD cd logic/worker && python worker.py
EXPOSE 4000