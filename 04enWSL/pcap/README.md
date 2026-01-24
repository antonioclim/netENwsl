# Packet Capture Files — Week 4

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

This directory contains network packet captures for educational analysis.

---

## Pre-generated Sample Files

These files are synthetic captures generated for educational demonstration. They can be opened in Wireshark to examine protocol structures without requiring a live lab environment.

| File | Size | Packets | LO | Protocol | Wireshark Filter |
|------|------|---------|-----|----------|------------------|
| `week04_lo3_text_commands.pcap` | ~1.5KB | 25+ | LO3 | TEXT/TCP | `tcp.port == 5400` |
| `week04_lo4_binary_header.pcap` | ~0.9KB | 18+ | LO4 | BINARY/TCP | `tcp.port == 5401` |
| `week04_lo5_tcp_handshake.pcap` | ~0.7KB | 12+ | LO5 | TCP | `tcp.flags.syn == 1` |
| `week04_lo5_udp_sensor.pcap` | ~0.9KB | 11+ | LO5 | UDP Sensor | `udp.port == 5402` |

---

## Opening in Wireshark

### Windows (Recommended)

1. Open Wireshark from Start Menu
2. File → Open
3. Navigate to `D:\NETWORKING\WEEK4\04enWSL\pcap\`
4. Select desired `.pcap` file

### WSL Command Line

```bash
# Copy to Windows-accessible location and open
cp pcap/*.pcap /mnt/c/Users/$USER/Desktop/

# Or use Windows Wireshark directly
"/mnt/c/Program Files/Wireshark/Wireshark.exe" pcap/week04_lo3_text_commands.pcap
```

---

## Sample Analysis Exercises

### Exercise 1: TEXT Protocol Analysis (LO3)

Open `week04_lo3_text_commands.pcap`:

1. **Filter:** `tcp.port == 5400`
2. **Observe:** TCP 3-way handshake (packets 1-3)
3. **Follow:** Right-click any packet → Follow → TCP Stream
4. **Questions:**
   - What is the framing format used? (length-prefix)
   - How many SET commands were issued?
   - What was the response to `GET key1`?

### Exercise 2: BINARY Protocol Analysis (LO4)

Open `week04_lo4_binary_header.pcap`:

1. **Filter:** `tcp.port == 5401 && tcp.len > 0`
2. **Select:** Any data packet
3. **View:** Click on packet → View → Bytes
4. **Identify Header Fields:**
   ```
   Offset | Bytes | Field
   -------|-------|------
   0-1    | 4E 50 | Magic "NP"
   2      | 01    | Version
   3      | 01    | Message Type (ECHO_REQ)
   4-5    | 00 0D | Payload Length (13)
   6-9    | ...   | Sequence Number
   10-13  | ...   | CRC32
   14+    | ...   | Payload
   ```
5. **Verify:** Calculate CRC32 manually:
   ```python
   import zlib
   header = bytes.fromhex('4E5001010D0D00000001')  # Without CRC
   payload = b'Hello Binary!'
   print(f'CRC32: {zlib.crc32(header + payload) & 0xFFFFFFFF:08X}')
   ```

### Exercise 3: TCP Handshake Analysis (LO5)

Open `week04_lo5_tcp_handshake.pcap`:

1. **Filter:** `tcp.flags.syn == 1` (shows SYN packets only)
2. **Examine Handshake:**
   - Packet 1: SYN (seq=1000)
   - Packet 2: SYN-ACK (seq=2000, ack=1001)
   - Packet 3: ACK (seq=1001, ack=2001)
3. **Questions:**
   - Why is the ACK number seq+1?
   - What is the initial window size?
   - How does the 4-way close differ from the 3-way open?

### Exercise 4: UDP Sensor Protocol (LO5)

Open `week04_lo5_udp_sensor.pcap`:

1. **Filter:** `udp.port == 5402`
2. **Select:** Any UDP packet
3. **View Bytes:** Identify the 23-byte structure:
   ```
   Offset | Size | Field
   -------|------|------
   0      | 1    | Version (0x01)
   1-4    | 4    | Sensor ID (big-endian)
   5-8    | 4    | Temperature (float32, big-endian)
   9-18   | 10   | Location (padded string)
   19-22  | 4    | CRC32
   ```
4. **Find Corrupted Packet:** Filter for CRC errors:
   - The last packet has intentionally corrupted CRC (`DEADBEEF`)
   - How would you detect this programmatically?

---

## Generating Your Own Captures

### Using the Lab Environment

```bash
# Start lab services
make docker-up

# In another terminal, start capture
python scripts/capture_traffic.py --interface any --port 5400 --output pcap/my_capture.pcap

# In another terminal, generate traffic
python src/apps/text_proto_client.py

# Stop capture with Ctrl+C
```

### Using tcpdump

```bash
# Capture TEXT protocol traffic
sudo tcpdump -i any port 5400 -w pcap/text_capture.pcap

# Capture BINARY protocol traffic
sudo tcpdump -i any port 5401 -w pcap/binary_capture.pcap

# Capture UDP sensor traffic
sudo tcpdump -i any udp port 5402 -w pcap/udp_capture.pcap
```

### Using Wireshark in WSL

```bash
# Install tshark (command-line Wireshark)
sudo apt install tshark

# Capture
sudo tshark -i any -f "port 5400" -w pcap/capture.pcap
```

---

## Regenerating Sample Files

If samples are missing or corrupted:

```bash
python scripts/generate_pcap_samples.py
```

This creates synthetic captures without requiring live servers.

---

## File Naming Convention

```
week04_lo{N}_{protocol}_{scenario}.pcap

Examples:
- week04_lo3_text_commands.pcap
- week04_lo4_binary_header.pcap
- week04_lo5_tcp_handshake.pcap
- week04_lo5_udp_sensor.pcap
```

---

## Troubleshooting

### "File not recognized" in Wireshark

- Verify file is not corrupted: `file pcap/*.pcap`
- Regenerate: `python scripts/generate_pcap_samples.py`

### No packets visible

- Check filter is not too restrictive
- Clear display filter to see all packets
- Verify capture file is not empty: `ls -la pcap/`

### Can't open from WSL path

- Copy to Windows path first
- Or use Windows path format: `//wsl$/Ubuntu/home/user/...`

---

## See Also

- `scripts/capture_traffic.py` — Automated capture script
- `scripts/generate_pcap_samples.py` — Sample generation script
- `docs/commands_cheatsheet.md` — tcpdump and tshark commands
- `README.md` § Wireshark Setup — Interface selection guide

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Week 4: Physical Layer, Data Link Layer & Custom Protocols*
