FROM alpine:3.19

LABEL maintainer="NETWORKING class - ASE, Informatics"
LABEL description="Week 10 SSH Server (OpenSSH)"

# Install OpenSSH server
RUN apk add --no-cache openssh-server

# Create user for laboratory
RUN adduser -D -s /bin/sh labuser && \
    echo "labuser:labpass" | chpasswd

# Configure SSH
RUN ssh-keygen -A && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config

# Create storage directory
RUN mkdir -p /home/labuser/storage && \
    chown labuser:labuser /home/labuser/storage

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D", "-e"]
