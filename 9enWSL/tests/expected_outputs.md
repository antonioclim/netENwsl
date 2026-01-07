# Expected Outputs for Week 9 Laboratory

> NETWORKING class - ASE, Informatics | by Revolvix

This document describes the expected outputs for each exercise and demonstration
in the Week 9 laboratory.

## Exercise 1: Endianness and Binary Framing

### Expected Console Output

```
═══════════════════════════════════════════════════════════════════════════════
  DEMO: Endianness and Binary Framing (Presentation Layer - L6)
═══════════════════════════════════════════════════════════════════════════════

▶ Original payload:
  Text: 'Hello, S9 – UTF‑8 ✓ Romania'
  Bytes (32): b'Hello, S9 \xe2\x80\x93 UTF\xe2\x80\x918 \xe2\x9c\x93 Romania'

▶ Header length: 12 bytes
  Total message length: 44 bytes

──────────────────────────────────────────────────────────────────────────────
  HEADER COMPARISON: Big-Endian vs Little-Endian
──────────────────────────────────────────────────────────────────────────────

  Big-Endian (Network Order):
  53 39  | 02 a5  | 00 00 00 20  | xx xx xx xx
  ↑↑         ↑  ↑   ↑──────────↑   ↑──────────────────↑
  magic    type flags  length          crc32

  Little-Endian:
  53 39  | 02 a5  | 20 00 00 00  | xx xx xx xx
```

### Key Observations

- Big-endian stores most significant byte first (0x00000020)
- Little-endian stores least significant byte first (0x20000000)
- Network byte order is always big-endian

---

## Exercise 2: Pseudo-FTP Server

### Server Startup Output

```
╔══════════════════════════════════════════════════════════════╗
║             PSEUDO-FTP SERVER v1.0                           ║
╚══════════════════════════════════════════════════════════════╝

[2026-01-07 10:00:00] [INFO] Server configuration:
  - Host: 0.0.0.0
  - Port: 3333
  - Files directory: ./server-files
  - Max connections: 10

[2026-01-07 10:00:00] [INFO] Server started, listening on 0.0.0.0:3333
```

### Client Session Output

```
pseudo-ftp> AUTH admin:password123
[OK] Authentication successful. Welcome, admin!

pseudo-ftp> PWD
[OK] Current directory: /

pseudo-ftp> LIST
[OK] Directory listing:
  hello.txt       42 bytes    2026-01-07 10:00
  sample.bin    1024 bytes    2026-01-07 10:00

pseudo-ftp> GET hello.txt
[OK] Transfer complete: 42 bytes
    CRC-32: 0xA1B2C3D4
    Saved to: ./client-files/hello.txt

pseudo-ftp> QUIT
[OK] Session closed. Goodbye!
```

---

## Docker Multi-Client Test

### Expected Docker Compose Output

```
[+] Running 3/3
 ✔ Container s9_ftp_server  Started
 ✔ Container s9_client1     Started
 ✔ Container s9_client2     Started

s9_ftp_server  | === FTP Server Starting ===
s9_ftp_server  | [INFO] Server started on 0.0.0.0:2121
s9_client1     | === Client 1: Executing LIST ===
s9_client2     | === Client 2: Executing GET ===
s9_ftp_server  | [INFO] Client connected from 172.29.9.3
s9_ftp_server  | [INFO] Client connected from 172.29.9.4
s9_client1     | hello.txt
s9_client1     | sample.bin
s9_client1     | === Client 1: Complete ===
s9_client2     | [OK] Downloaded: hello.txt (42 bytes)
s9_client2     | === Client 2: Complete ===
```

---

## Wireshark Capture Analysis

### Expected Packet Sequence

| No. | Time     | Source        | Destination   | Protocol | Info                    |
|-----|----------|---------------|---------------|----------|-------------------------|
| 1   | 0.000000 | 172.29.9.3    | 172.29.9.2    | TCP      | [SYN] Seq=0             |
| 2   | 0.000012 | 172.29.9.2    | 172.29.9.3    | TCP      | [SYN, ACK] Seq=0 Ack=1  |
| 3   | 0.000018 | 172.29.9.3    | 172.29.9.2    | TCP      | [ACK] Seq=1 Ack=1       |
| 4   | 0.001234 | 172.29.9.2    | 172.29.9.3    | TCP      | [PSH, ACK] Len=35       |
| 5   | 0.002456 | 172.29.9.3    | 172.29.9.2    | TCP      | [PSH, ACK] Len=16       |

### Expected Header Bytes

```
46 54 50 43 00 00 00 20 ab cd 12 34 00 00 00 00
│           │           │           │
│           │           │           └── Flags: 0 (uncompressed)
│           │           └── CRC-32: 0xABCD1234
│           └── Length: 32 bytes
└── Magic: "FTPC"
```

---

## Verification Commands

### Verify Exercise 1

```bash
python src/exercises/ex_9_01_endianness.py --selftest
```

Expected:
```
  [OK] All tests passed!
```

### Verify Docker Environment

```bash
python scripts/start_lab.py --status
```

Expected:
```
Container Status
============================================================
  s9_ftp_server                 running
  s9_client1                    exited (0)
  s9_client2                    exited (0)
```

### Verify File Transfer

```bash
ls -la docker/client2-files/
```

Expected:
```
total 8
drwxr-xr-x 2 user user 4096 Jan  7 10:00 .
drwxr-xr-x 5 user user 4096 Jan  7 10:00 ..
-rw-r--r-- 1 user user   42 Jan  7 10:01 hello.txt
```

---

## Common Issues and Expected Behaviour

### Port Already in Use

If port 2121 is busy:
```
ERROR: Port 2121 is already in use
```

Solution: Stop existing services or use a different port.

### Docker Not Running

```
ERROR: Cannot connect to Docker daemon
```

Solution: Start Docker Desktop.

### Authentication Failed

```
[ERROR] 530 Login incorrect
```

Solution: Use correct credentials (test/12345).

---

*NETWORKING class - ASE, Informatics | by Revolvix*
