FROM python:3.12-alpine

LABEL maintainer="NETWORKING class - ASE, Informatics"
LABEL description="Week 10 SSH Client (Paramiko)"

RUN pip install --no-cache-dir paramiko

WORKDIR /app
COPY paramiko_client.py .

CMD ["python3", "paramiko_client.py"]
