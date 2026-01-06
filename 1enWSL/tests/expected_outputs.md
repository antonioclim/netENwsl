# Expected Outputs

> NETWORKING class - ASE, Informatics | by Revolvix

This document describes the expected outputs for each exercise to help students verify their work.

## Exercise 1: Network Interface Inspection

### Command: `ip addr show`

Expected output pattern:
```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 ...
    inet 172.20.1.X/24 brd 172.20.1.255 scope global eth0
```

**Key observations:**
- `lo` interface with IP 127.0.0.1/8
- At least one other interface (eth0 or similar) with an IP address
- Interface state should be UP

### Command: `ip route show`

Expected output pattern:
```
default via 172.20.1.1 dev eth0
172.20.1.0/24 dev eth0 proto kernel scope link src 172.20.1.X
```

**Key observations:**
- Default route pointing to a gateway
- Local network route

---

## Exercise 2: Ping Connectivity

### Command: `ping -c 4 127.0.0.1`

Expected output:
```
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.025 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.031 ms
64 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.028 ms
64 bytes from 127.0.0.1: icmp_seq=4 ttl=64 time=0.030 ms

--- 127.0.0.1 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3051ms
rtt min/avg/max/mdev = 0.025/0.028/0.031/0.002 ms
```

**Key observations:**
- 0% packet loss
- TTL = 64 (local)
- Very low latency (< 1ms)

### Python Exercise: `ex_1_01_ping_latency.py`

Expected output:
```
PING host=127.0.0.1 tx=5 rx=5 avg_rtt=0.045 ms
```

**Key observations:**
- tx = rx (no packet loss)
- avg_rtt present and reasonable

---

## Exercise 3: TCP Communication

### Netcat Server/Client

Server terminal:
```
$ nc -l -p 9090
Hello from client
```

Client terminal:
```
$ nc localhost 9090
Hello from client
^C
```

Socket state (while connected):
```
$ ss -tnp | grep 9090
ESTAB  0  0  127.0.0.1:9090   127.0.0.1:54321  users:(("nc",pid=1234,fd=3))
ESTAB  0  0  127.0.0.1:54321  127.0.0.1:9090   users:(("nc",pid=1235,fd=3))
```

**Key observations:**
- Two ESTABLISHED connections visible
- Bidirectional data flow
- Ephemeral port on client side

### Python Exercise: `ex_1_02_tcp_server_client.py`

Expected output:
```
TCP host=127.0.0.1 port=9090 rtt_ms=0.85 response=ACK:hello
```

**Key observations:**
- Response contains "ACK:" prefix
- RTT measured in milliseconds
- Connection succeeded

---

## Exercise 4: Traffic Capture

### tcpdump Output

```
$ tcpdump -i lo -c 10 port 9090
tcpdump: verbose output suppressed...
listening on lo, link-type EN10MB (Ethernet), capture size 262144 bytes
12:34:56.789012 IP localhost.54321 > localhost.9090: Flags [S], seq 123456789...
12:34:56.789123 IP localhost.9090 > localhost.54321: Flags [S.], seq 987654321...
12:34:56.789234 IP localhost.54321 > localhost.9090: Flags [.], ack 1, win 512...
```

**Key observations:**
- SYN packet (Flags [S])
- SYN-ACK packet (Flags [S.])
- ACK packet (Flags [.])

### tshark Output

```
$ tshark -r capture.pcap
    1   0.000000    127.0.0.1 → 127.0.0.1    TCP 74 54321 → 9090 [SYN]
    2   0.000012    127.0.0.1 → 127.0.0.1    TCP 74 9090 → 54321 [SYN, ACK]
    3   0.000018    127.0.0.1 → 127.0.0.1    TCP 66 54321 → 9090 [ACK]
```

**Key observations:**
- Three-way handshake visible
- Timestamps in microseconds
- Source and destination ports visible

---

## Exercise 5: PCAP Statistics

### CSV Export Fields

Expected CSV structure:
```csv
frame.number,frame.time_relative,ip.src,ip.dst,tcp.srcport,tcp.dstport,tcp.flags.str,frame.len
1,0.000000,127.0.0.1,127.0.0.1,54321,9090,··········S·,74
2,0.000012,127.0.0.1,127.0.0.1,9090,54321,·······A··S·,74
3,0.000018,127.0.0.1,127.0.0.1,54321,9090,·······A····,66
```

### Python Analysis Output

Expected format:
```
Total packets: 8
First packet: 0.000000
Last packet: 0.015234
Duration: 0.0152 seconds
```

---

## Success Criteria Summary

| Exercise | Success Indicator |
|----------|-------------------|
| 1 | Interfaces and routes displayed correctly |
| 2 | 0% packet loss on loopback ping |
| 3 | Bidirectional TCP communication works |
| 4 | PCAP file contains TCP handshake |
| 5 | Statistics extracted from capture |

---

*NETWORKING class - ASE, Informatics | by Revolvix*
