#!/bin/bash
# Week 13 - vsftpd Container Entrypoint
# NETWORKING class - ASE, Informatics | by Revolvix
#
# Starts vsftpd and an educational backdoor stub listener.
# The stub does NOT execute commands - it only prints a banner and closes.

set -e

echo "[Week 13] Starting FTP service..."

# Start the backdoor stub listener in background
# This simulates the presence of a backdoor port for detection exercises
echo "[Week 13] Starting educational backdoor stub on port 6200..."
while true; do
    echo -e "220 Week13-Backdoor-Stub\r\n[EDUCATIONAL] This is a simulated backdoor.\r\n[EDUCATIONAL] No commands are executed.\r\nConnection will close.\r\n" | \
        nc -l -p 6200 -q 1 2>/dev/null || sleep 1
done &

# Start vsftpd in foreground
echo "[Week 13] Starting vsftpd on port 21..."
exec /usr/sbin/vsftpd /etc/vsftpd.conf
