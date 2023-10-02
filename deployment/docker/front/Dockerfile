FROM python:3.8-slim-buster
WORKDIR /worker   

COPY ["src/deployment/docker/front/requirements.txt", "/worker/"]
RUN pip install -r requirements.txt

COPY ["src/logic/", "/worker/"]

CMD python front.py
EXPOSE 5000