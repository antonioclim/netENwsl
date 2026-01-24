# 📖 API Quick Reference — Week 13

> Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## Exercise 1: Port Scanner

**File:** `src/exercises/ex_13_01_port_scanner.py`

```bash
python3 src/exercises/ex_13_01_port_scanner.py [OPTIONS]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--target` | Required | IP, range (192.168.1.1-10) or CIDR |
| `--ports` | `1-1024` | Port spec: 80, 1-1024, or 22,80,443 |
| `--mode` | `scan` | `scan` or `discovery` |
| `--timeout` | `0.5` | Connection timeout (seconds) |
| `--workers` | `100` | Parallel threads |
| `--json-out` | None | Export to JSON |

---

## Exercise 2: MQTT Client

**File:** `src/exercises/ex_13_02_mqtt_client.py`

```bash
python3 src/exercises/ex_13_02_mqtt_client.py [OPTIONS]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--broker` | `localhost` | MQTT broker address |
| `--port` | `1883` | Broker port |
| `--mode` | Required | `publish` or `subscribe` |
| `--topic` | Required | MQTT topic |
| `--tls` | False | Enable TLS |
| `--qos` | `0` | QoS level (0, 1, 2) |

---

## Exercise 3: Packet Sniffer

**File:** `src/exercises/ex_13_03_packet_sniffer.py`  
**Requires:** sudo/root privileges

```bash
sudo python3 src/exercises/ex_13_03_packet_sniffer.py [OPTIONS]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--iface` | `any` | Network interface |
| `--filter` | None | BPF filter expression |
| `--count` | `10` | Packets to capture |
| `--output` | None | Save to PCAP file |

---

## Exercise 4: Vulnerability Checker

**File:** `src/exercises/ex_13_04_vuln_checker.py`

```bash
python3 src/exercises/ex_13_04_vuln_checker.py [OPTIONS]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--target` | Required | Target IP/hostname |
| `--port` | Required | Target port |
| `--service` | Required | `http`, `ftp` or `mqtt` |
| `--output` | None | Report output file |

---

## Quick Reference Card

| Task | Command |
|------|---------|
| Start lab | `make start` |
| Stop lab | `make stop` |
| Run quiz | `make quiz` |
| Run tests | `make test` |
| Lint code | `make lint` |
| Validate | `make validate` |

---

*Computer Networks — Week 13: IoT and Security*
