# Parsons Problems — Week 1

> Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Parsons problems are code arrangement exercises. Each problem contains **two distractor blocks**: they look plausible but should not be used.

**How to use in class**
- Give students the scrambled blocks first.
- Ask for a predicted output.
- Let pairs agree on an order then run the code.
- Compare outputs and explain why each distractor is wrong.

---

## P1: Ping RTT summary (LO1)

**Task:** Arrange blocks to ping a host 4 times and extract the average RTT from the summary line.

### Scrambled blocks

```python
# Block A
import re
import subprocess

# Block B
cmd = ["ping", "-c", "4", "8.8.8.8"]

# Block C
out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout

# Block D
m = re.search(r"rtt .* = .*?/.*?/(.*?)/", out)

# Block E
print(float(m.group(1)))

# Block F (DISTRACTOR 1)
cmd = ["ping", "8.8.8.8", "-n", "4"]  # Windows flag, not WSL

# Block G (DISTRACTOR 2)
m = re.search(r"time=(\d+)", out)  # Only gets first packet, not average
```

### Correct order
<details>
<summary>Reveal</summary>

```python
import re
import subprocess

cmd = ["ping", "-c", "4", "8.8.8.8"]
out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
m = re.search(r"rtt .* = .*?/.*?/(.*?)/", out)
print(float(m.group(1)))
```

**Why the distractors are wrong:**
- **Block F:** `-n` is the Windows syntax. In WSL you need `-c`.
- **Block G:** This regex only extracts the first packet's RTT, not the average from the summary line.
</details>

---

## P2: Identify your active interface (LO1)

**Task:** Parse `ip a` output and print the first non-loopback interface that has an IPv4 address.

### Scrambled blocks

```python
# Block A
import re
import subprocess

# Block B
out = subprocess.run(["ip", "a"], capture_output=True, text=True, check=True).stdout

# Block C
blocks = out.split("\n\n")

# Block D
for blk in blocks:
    if " lo:" in blk:
        continue
    if re.search(r"\binet\s+\d+\.\d+\.\d+\.\d+/", blk):
        name = re.search(r"^\d+:\s+([^:]+):", blk).group(1)
        print(name)
        break

# Block E (DISTRACTOR 1)
print("eth0")  # Assumes a fixed name

# Block F (DISTRACTOR 2)
out = subprocess.run(["ifconfig"], capture_output=True, text=True, check=True).stdout
```

### Correct order
<details>
<summary>Reveal</summary>

```python
import re
import subprocess

out = subprocess.run(["ip", "a"], capture_output=True, text=True, check=True).stdout
blocks = out.split("\n\n")
for blk in blocks:
    if " lo:" in blk:
        continue
    if re.search(r"\binet\s+\d+\.\d+\.\d+\.\d+/", blk):
        name = re.search(r"^\d+:\s+([^:]+):", blk).group(1)
        print(name)
        break
```

**Why the distractors are wrong:**
- **Block E:** Interface names vary. In containers you may see `eth0`, in WSL you might see something else entirely.
- **Block F:** `ifconfig` is deprecated and may not be installed. The modern tool is `ip`.
</details>

---

## P3: Listening sockets count (LO4)

**Task:** Count listening TCP sockets using `ss -tulpn` output.

### Scrambled blocks

```python
# Block A
import subprocess

# Block B
out = subprocess.run(["ss", "-tulpn"], capture_output=True, text=True, check=True).stdout

# Block C
lines = [ln for ln in out.splitlines() if ln.strip().startswith("tcp")]

# Block D
listen = [ln for ln in lines if "LISTEN" in ln]

# Block E
print(len(listen))

# Block F (DISTRACTOR 1)
out = subprocess.run(["netstat", "-an"], capture_output=True, text=True, check=True).stdout

# Block G (DISTRACTOR 2)
lines = out.split(",")  # Wrong delimiter for line splitting
```

### Correct order
<details>
<summary>Reveal</summary>

```python
import subprocess

out = subprocess.run(["ss", "-tulpn"], capture_output=True, text=True, check=True).stdout
lines = [ln for ln in out.splitlines() if ln.strip().startswith("tcp")]
listen = [ln for ln in lines if "LISTEN" in ln]
print(len(listen))
```

**Why the distractors are wrong:**
- **Block F:** `netstat` may not be installed and it produces different output format. Also drops the process mapping which is the point of `-p`.
- **Block G:** Using `split(",")` is wrong — output is line-based, not comma-separated.
</details>

---

## P4: Traceroute hop extraction (LO3)

**Task:** Extract the hop numbers from `traceroute` output.

### Scrambled blocks

```python
# Block A
import subprocess

# Block B
out = subprocess.run(["traceroute", "-n", "8.8.8.8"], capture_output=True, text=True, check=True).stdout

# Block C
hops = []
for ln in out.splitlines():
    if ln and ln[0].isdigit():
        hops.append(int(ln.split()[0]))

# Block D
print(hops[:5])

# Block E (DISTRACTOR 1)
out = subprocess.run(["tracert", "8.8.8.8"], capture_output=True, text=True, check=True).stdout

# Block F (DISTRACTOR 2)
hops = out.count("\n")  # Counts all lines, not just hops
```

### Correct order
<details>
<summary>Reveal</summary>

```python
import subprocess

out = subprocess.run(["traceroute", "-n", "8.8.8.8"], capture_output=True, text=True, check=True).stdout
hops = []
for ln in out.splitlines():
    if ln and ln[0].isdigit():
        hops.append(int(ln.split()[0]))
print(hops[:5])
```

**Why the distractors are wrong:**
- **Block E:** `tracert` is the Windows tool, not available in WSL by default.
- **Block F:** Counting newlines includes the header line and blank lines, not just hop entries.
</details>

---

## P5: Loopback sanity check (LO1)

**Task:** Verify that `127.0.0.1` resolves to loopback by reading `ip route get 127.0.0.1`.

### Scrambled blocks

```python
# Block A
import subprocess

# Block B
out = subprocess.run(["ip", "route", "get", "127.0.0.1"], capture_output=True, text=True, check=True).stdout

# Block C
print("lo" in out)

# Block D (DISTRACTOR 1)
out = subprocess.run(["ipconfig"], capture_output=True, text=True, check=True).stdout

# Block E (DISTRACTOR 2)
out = subprocess.run(["route", "print"], capture_output=True, text=True, check=True).stdout
```

### Correct order
<details>
<summary>Reveal</summary>

```python
import subprocess

out = subprocess.run(["ip", "route", "get", "127.0.0.1"], capture_output=True, text=True, check=True).stdout
print("lo" in out)
```

**Why the distractors are wrong:**
- **Block D:** `ipconfig` is a Windows command and does not exist in WSL Linux.
- **Block E:** `route print` is Windows syntax. Linux uses `ip route` or the deprecated `route` without `print`.
</details>

---

## Summary

| Problem | Topic | LO | Key Learning |
|---------|-------|----|-|
| P1 | Ping RTT | LO1 | Linux vs Windows flags, regex for summary |
| P2 | Interface discovery | LO1 | Modern `ip` vs deprecated `ifconfig` |
| P3 | Socket listing | LO4 | `ss` vs `netstat`, line parsing |
| P4 | Traceroute | LO3 | Linux vs Windows tools, hop extraction |
| P5 | Loopback routing | LO1 | `ip route` vs Windows commands |

---

*NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim*
*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*
