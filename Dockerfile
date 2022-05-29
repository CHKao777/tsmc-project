FROM python:3.10-slim as crawler
WORKDIR /tsmc-project
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY GoogleCrawler.py GoogleCrawler.py
CMD ["python", "GoogleCrawler.py"]

FROM python:3.10-slim as worker
WORKDIR /tsmc-project
COPY requirements-worker.txt requirements-worker.txt
RUN pip install -r requirements-worker.txt
COPY worker.py worker.py
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