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