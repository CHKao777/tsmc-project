FROM python:3.10-slim as crawler-controller
WORKDIR /tsmc-project/crawler
COPY ./crawler/requirements.txt requirements.txt 
RUN pip install -r requirements.txt
COPY ./crawler/. .
CMD ["python", "GoogleCrawlerController.py"]

FROM python:3.10-slim as crawler
WORKDIR /tsmc-project/crawler
COPY ./crawler/requirements.txt requirements.txt 
RUN pip install -r requirements.txt
COPY ./crawler/. .
CMD ["python", "GoogleCrawler.py"]

FROM python:3.10-slim as worker
WORKDIR /tsmc-project/crawler
COPY ./crawler/requirements-worker.txt requirements-worker.txt
RUN pip install -r requirements-worker.txt
COPY ./crawler/. .
CMD ["python", "worker.py"]

FROM python:3.10-slim as web
WORKDIR /tsmc-project
ENV FLASK_APP=./frontend/app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY ./frontend/requirements.txt ./frontend/requirements.txt
RUN pip install -r ./frontend/requirements.txt
EXPOSE 500
COPY ./frontend/. ./frontend/.
CMD ["flask", "run"]

FROM node:16.15.0 as nodeserver
WORKDIR /tsmc-project/nodeserver
COPY ./nodeserver/. .
RUN npm install
EXPOSE 3000
CMD npm start