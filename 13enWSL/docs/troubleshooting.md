# 🔧 Troubleshooting Guide

> Week 13: IoT and Security  
> by ing. dr. Antonio Clim

---

## 🆘 Beginner Errors (Start Here!)

### "I do not know which command to run first"

```bash
cd /mnt/d/NETWORKING/WEEK13/13enWSL
make help
```

### "I get weird Python errors"

```bash
python3 --version
# Should show: Python 3.11.x or higher
```

### "Permission denied" on anything

```bash
sudo usermod -aG docker $USER
# Then log out and back in!
```

### "Nothing happens when I run a command"

```bash
# Check if lab is running
docker ps

# If empty, start the lab:
make start
```

---

## Docker Issues

### Docker Not Running

```bash
sudo service docker start
docker info
```

### Port Already in Use

```bash
sudo netstat -tlnp | grep <PORT>
# Stop conflicting process or change port in docker-compose.yml
```

### Containers Not Starting

```bash
docker logs week13_mosquitto
docker logs week13_dvwa
docker logs week13_vsftpd
```

---

## Certificate Issues

### TLS Connection Refused

```bash
# Regenerate certificates
python3 setup/configure_docker.py

# Verify certificates exist
ls -la docker/configs/certs/
```

---

## MQTT Issues

### Cannot Connect to Broker

```bash
# Verify container is running
docker ps | grep mosquitto

# Test with netcat
nc -zv localhost 1883
```

---

## Python Issues

### Module Not Found

```bash
pip install -r setup/requirements.txt
```

### Scapy Permission Errors

```bash
sudo python3 src/exercises/ex_13_03_packet_sniffer.py
```

---

## Quick Fixes Table

| Problem | Solution |
|---------|----------|
| Docker not running | `sudo service docker start` |
| Permission denied | `sudo usermod -aG docker $USER && newgrp docker` |
| Wrong directory | `cd /mnt/d/NETWORKING/WEEK13/13enWSL` |
| Missing packages | `pip install -r setup/requirements.txt` |
| Port in use | Check with `netstat -tlnp` |

---

## Getting Help

1. Run: `python3 setup/verify_environment.py`
2. Check logs: `docker logs week13_<service>`
3. Open an issue in the GitHub repository

---

*Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim*
