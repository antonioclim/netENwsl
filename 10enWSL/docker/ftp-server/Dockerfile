FROM python:3.12-alpine

LABEL maintainer="NETWORKING class - ASE, Informatics"
LABEL description="Week 10 FTP Server (pyftpdlib)"

RUN pip install --no-cache-dir pyftpdlib

# Create FTP directories
RUN mkdir -p /home/ftp/uploads /home/ftp/downloads && \
    echo "Welcome to the Week 10 FTP server!" > /home/ftp/welcome.txt

WORKDIR /app
COPY ftp_server.py .

EXPOSE 2121
EXPOSE 30000-30009

CMD ["python3", "ftp_server.py"]
