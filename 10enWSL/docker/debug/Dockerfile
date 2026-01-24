FROM alpine:3.19

LABEL maintainer="NETWORKING class - ASE, Informatics"
LABEL description="Week 10 Debug Container with Network Tools"

# Install network debugging tools
RUN apk add --no-cache \
    bash \
    bind-tools \
    curl \
    wget \
    openssh-client \
    lftp \
    tcpdump \
    nmap \
    nmap-scripts \
    iputils \
    iproute2 \
    netcat-openbsd \
    python3 \
    py3-pip

# Install Python packages for scripting
RUN pip3 install --no-cache-dir --break-system-packages \
    requests \
    paramiko

WORKDIR /workspace

# Keep container running
CMD ["tail", "-f", "/dev/null"]
