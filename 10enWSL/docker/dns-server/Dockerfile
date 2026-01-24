FROM python:3.12-alpine

LABEL maintainer="NETWORKING class - ASE, Informatics"
LABEL description="Week 10 Custom DNS Server (dnslib)"

RUN pip install --no-cache-dir dnslib

WORKDIR /app
COPY dns_server.py .

EXPOSE 5353/udp

CMD ["python3", "dns_server.py"]
