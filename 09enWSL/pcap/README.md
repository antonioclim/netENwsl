# 📦 Packet Captures — Week 9

> Session Layer (L5) and Presentation Layer (L6)
> NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

This directory contains packet capture (PCAP) files and instructions for
traffic analysis exercises.

---

## Directory Structure

```
pcap/
├── README.md                    # This file
├── .gitkeep                     # Keeps directory in git
└── [your captures here]         # Student-generated captures
```

---

## Generating Your Own Captures

### Method 1: Using the Capture Script

```bash
# From the project root
cd /mnt/d/NETWORKING/WEEK9/09enWSL

# Capture 30 seconds of traffic
python scripts/capture_traffic.py --duration 30 --output pcap/my_capture.pcap

# Capture with specific filter
python scripts/capture_traffic.py --filter "tcp port 2121" --output pcap/ftp_control.pcap
```

### Method 2: Using Wireshark (Recommended)

1. **Start Wireshark** from Windows Start Menu
2. **Select interface:** `vEthernet (WSL)`
3. **Apply capture filter:** `tcp port 2121 or tcp portrange 60000-60010`
4. **Start capture** (blue shark fin button)
5. **Generate traffic** in a separate terminal:
   ```bash
   make start
   python scripts/run_demo.py --demo ftp_session
   ```
6. **Stop capture** (red square button)
7. **Save as:** `D:\NETWORKING\WEEK9\09enWSL\pcap\ftp_session.pcap`

### Method 3: Using tcpdump in Container

```bash
# Start capture inside FTP server container
docker exec s9_ftp_server tcpdump -c 100 -w /tmp/capture.pcap -i eth0

# Copy capture to host
docker cp s9_ftp_server:/tmp/capture.pcap ./pcap/container_capture.pcap
```

---

## Recommended Capture Exercises

### Capture 1: FTP Authentication (LO1, LO4)

**Objective:** Capture USER/PASS sequence on control channel

**Steps:**
1. Start Wireshark with filter: `tcp.port == 2121`
2. Start FTP server: `make start`
3. Connect with client: `python src/exercises/ex_9_03_ftp_client_demo.py`
4. Observe packets: 220 banner → USER → 331 → PASS → 230
5. Save as: `pcap/ftp_auth_sequence.pcap`

**What to look for:**
- TCP three-way handshake (SYN, SYN-ACK, ACK)
- FTP server banner (220 response)
- USER and PASS commands in clear text
- 230 "Login successful" response

### Capture 2: FTP Passive Mode (LO4, LO5)

**Objective:** Capture PASV negotiation and data channel establishment

**Steps:**
1. Start Wireshark with filter: `tcp.port == 2121 || tcp.port >= 60000`
2. Initiate file listing or transfer
3. Observe PASV response with port numbers
4. Observe data channel connection
5. Save as: `pcap/ftp_passive_mode.pcap`

**What to look for:**
- PASV command on control channel
- 227 response with IP and port numbers
- New TCP connection to passive port
- Data transfer on passive port
- 226 "Transfer complete" on control channel

### Capture 3: Binary Protocol Framing (LO2, LO3)

**Objective:** Capture custom binary protocol messages

**Steps:**
1. Start pseudo-FTP server and client
2. Capture on port 60100
3. Observe binary headers in hex view
4. Save as: `pcap/binary_framing.pcap`

**What to look for:**
- Magic bytes at start of each message
- Length field indicating payload size
- CRC-32 checksum at header end
- Payload data following header

---

## Analysis Tips

### Wireshark Display Filters

| Filter | Purpose |
|--------|---------|
| `tcp.port == 2121` | FTP control channel |
| `tcp.port >= 60000 && tcp.port <= 60010` | FTP passive data |
| `ftp.request.command == "USER"` | Authentication requests |
| `ftp.response.code == 230` | Successful logins |
| `ftp.request.command == "PASV"` | Passive mode requests |
| `tcp.flags.syn == 1` | Connection establishments |

### Following TCP Streams

1. Right-click any packet in the stream
2. Select "Follow" → "TCP Stream"
3. View complete conversation in text or hex
4. Use stream index to switch between streams

### Identifying Control vs Data Channels

- **Control channel (2121):** ASCII text, FTP commands (USER, PASS, LIST, RETR)
- **Data channel (60000-60010):** Binary or text data, file contents

---

## Sample Expected Outputs

### FTP Control Channel Conversation

```
220 FTP Server Ready
USER test
331 Username ok, send password
PASS 12345
230 Login successful
PWD
257 "/" is the current directory
PASV
227 Entering Passive Mode (172,29,9,2,234,96)
LIST
150 Opening data connection
226 Transfer complete
QUIT
221 Goodbye
```

### Binary Message Header (Hex View)

```
53 39 50 4b    Magic: "S9PK"
01             Type: 1 (DATA)
00             Flags: 0
00 00 00 0d    Length: 13 bytes
a3 b2 c1 d0    CRC-32: 0xa3b2c1d0
48 65 6c 6c    Payload: "Hell"
6f 2c 20 57    Payload: "o, W"
6f 72 6c 64    Payload: "orld"
21             Payload: "!"
```

---

## Troubleshooting

### No Packets Captured

- Verify correct interface selected (vEthernet WSL)
- Ensure traffic is being generated DURING capture
- Check that containers are running: `docker ps`
- Try without display filter to see all traffic

### Permission Denied

- Run Wireshark as Administrator
- Reinstall Npcap with "WinPcap API-compatible Mode"

### Cannot Decode FTP

- Right-click packets → "Decode As" → "FTP"
- Ensure port 2121 is recognised as FTP

---

## Submitting Captures

For assignments requiring packet captures:

1. Name files clearly: `[netid]_[exercise]_[description].pcap`
2. Keep file size reasonable (< 5MB)
3. Include only relevant packets (use capture filters)
4. Document what the capture demonstrates

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Week 9: Session Layer and Presentation Layer*
