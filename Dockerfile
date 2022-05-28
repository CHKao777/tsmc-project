FROM python:3.10-slim
WORKDIR /tsmc-project
COPY GoogleCrawler.py /tsmc-project
COPY worker.py /tsmc-project
COPY requirements.txt /tsmc-project
RUN pip install -r requirements.txt
CMD ["python", "GoogleCrawler.py"]

# FROM python:3.10-slim
# WORKDIR /tsmc-project
# COPY worker.py /tsmc-project
# COPY requirements.txt /tsmc-project
# RUN pip install -r requirements.txt
# CMD ["python", "worker.py"]