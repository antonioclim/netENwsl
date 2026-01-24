# 🧩 Parsons Problems — Week 10
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Reorder the code blocks to create a working solution.

---

## Problem P1: Simple HTTPS Client

### Task

Create a function that makes an HTTPS GET request to a URL and returns the response body. The function should handle self-signed certificates by disabling verification.

### Scrambled Blocks

```python
# Block A
    return response.text

# Block B
def https_get(url: str) -> str:

# Block C
    response = requests.get(url, verify=False, timeout=10)

# Block D
import requests
import urllib3

# Block E
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Block F (DISTRACTOR - not needed)
    ssl_context = ssl.create_default_context()

# Block G
    response.raise_for_status()

# Block H (DISTRACTOR - not needed)
import ssl
```

### Correct Order

<details>
<summary>Click to reveal</summary>

```python
# Block D
import requests
import urllib3

# Block B
def https_get(url: str) -> str:

# Block E
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Block C
    response = requests.get(url, verify=False, timeout=10)

# Block G
    response.raise_for_status()

# Block A
    return response.text
```

**Distractor notes:**
- Block F (`ssl.create_default_context()`) is for the `ssl` module, not `requests`
- Block H (`import ssl`) is not needed when using `requests` with `verify=False`

**Key concepts:**
- `verify=False` disables certificate verification
- `urllib3.disable_warnings()` suppresses the InsecureRequestWarning
- `raise_for_status()` raises an exception for 4xx/5xx responses
</details>

---

## Problem P2: DNS Query Function

### Task

Create a function that sends a DNS query using the `socket` module and returns the raw response. The function should query a specific DNS server on a custom port.

### Scrambled Blocks

```python
# Block A
    sock.settimeout(5.0)

# Block B
def dns_query(server: str, port: int, query_data: bytes) -> bytes:

# Block C
    sock.sendto(query_data, (server, port))

# Block D
import socket

# Block E
    response, addr = sock.recvfrom(512)

# Block F
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Block G
    return response

# Block H
    sock.close()

# Block I (DISTRACTOR - not needed)
    sock.connect((server, port))

# Block J (DISTRACTOR - not needed)
    sock.bind(('', 0))
```

### Correct Order

<details>
<summary>Click to reveal</summary>

```python
# Block D
import socket

# Block B
def dns_query(server: str, port: int, query_data: bytes) -> bytes:

# Block F
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Block A
    sock.settimeout(5.0)

# Block C
    sock.sendto(query_data, (server, port))

# Block E
    response, addr = sock.recvfrom(512)

# Block H
    sock.close()

# Block G
    return response
```

**Distractor notes:**
- Block I (`sock.connect()`) is not needed for UDP; `sendto()` specifies the destination
- Block J (`sock.bind()`) is for servers, not clients

**Key concepts:**
- DNS uses UDP (`SOCK_DGRAM`)
- `sendto()` sends to a specific address without `connect()`
- `recvfrom()` receives data and the sender's address
- Always close sockets when done
</details>

---

## Problem P3: REST API Resource Handler

### Task

Create a Flask route that handles GET and POST requests for a `/api/items` endpoint. GET should return all items, POST should create a new item.

### Scrambled Blocks

```python
# Block A
        return jsonify({"items": items}), 200

# Block B
@app.route("/api/items", methods=["GET", "POST"])

# Block C
    if request.method == "GET":

# Block D
def handle_items():

# Block E
from flask import Flask, request, jsonify

# Block F
    elif request.method == "POST":

# Block G
        data = request.get_json()

# Block H
        items.append(new_item)

# Block I
        new_item = {"id": len(items) + 1, "name": data["name"]}

# Block J
        return jsonify(new_item), 201

# Block K
app = Flask(__name__)
items = []

# Block L (DISTRACTOR - not needed)
    return jsonify({"error": "Method not allowed"}), 405

# Block M (DISTRACTOR - not needed)
@app.route("/api/items/<int:item_id>")
```

### Correct Order

<details>
<summary>Click to reveal</summary>

```python
# Block E
from flask import Flask, request, jsonify

# Block K
app = Flask(__name__)
items = []

# Block B
@app.route("/api/items", methods=["GET", "POST"])

# Block D
def handle_items():

# Block C
    if request.method == "GET":

# Block A
        return jsonify({"items": items}), 200

# Block F
    elif request.method == "POST":

# Block G
        data = request.get_json()

# Block I
        new_item = {"id": len(items) + 1, "name": data["name"]}

# Block H
        items.append(new_item)

# Block J
        return jsonify(new_item), 201
```

**Distractor notes:**
- Block L (405 error) is not needed because Flask handles unknown methods automatically
- Block M is a different route decorator for item-specific operations

**Key concepts:**
- `methods=["GET", "POST"]` allows both HTTP methods
- `request.method` determines which operation to perform
- POST returns 201 Created status code
- GET returns 200 OK status code
</details>

---

## Problem P4: FTP File Download

### Task

Create a function that downloads a file from an FTP server using passive mode and returns its contents as bytes.

### Scrambled Blocks

```python
# Block A
    ftp.retrbinary(f"RETR {filename}", buffer.write)

# Block B
def ftp_download(host: str, port: int, user: str, passwd: str, filename: str) -> bytes:

# Block C
    ftp.login(user, passwd)

# Block D
from ftplib import FTP
from io import BytesIO

# Block E
    ftp = FTP()

# Block F
    ftp.connect(host, port)

# Block G
    buffer = BytesIO()

# Block H
    ftp.quit()

# Block I
    return buffer.getvalue()

# Block J (DISTRACTOR - not needed)
    ftp.set_pasv(True)

# Block K (DISTRACTOR - not needed)
    ftp.cwd("/")
```

### Correct Order

<details>
<summary>Click to reveal</summary>

```python
# Block D
from ftplib import FTP
from io import BytesIO

# Block B
def ftp_download(host: str, port: int, user: str, passwd: str, filename: str) -> bytes:

# Block E
    ftp = FTP()

# Block F
    ftp.connect(host, port)

# Block C
    ftp.login(user, passwd)

# Block G
    buffer = BytesIO()

# Block A
    ftp.retrbinary(f"RETR {filename}", buffer.write)

# Block H
    ftp.quit()

# Block I
    return buffer.getvalue()
```

**Distractor notes:**
- Block J (`set_pasv(True)`) is not needed because passive mode is the default in Python's ftplib
- Block K (`cwd("/")`) is not needed if the file path is absolute or we're in the right directory

**Key concepts:**
- `FTP()` creates a connection object (not connected yet)
- `connect()` establishes the control connection
- `login()` authenticates
- `retrbinary()` downloads in binary mode, calling the callback for each chunk
- `BytesIO` provides an in-memory file-like buffer
</details>

---

## Problem P5: Certificate Verification

### Task

Create a function that connects to an HTTPS server, retrieves its certificate and returns the certificate's subject and expiry date.

### Scrambled Blocks

```python
# Block A
    cert = conn.getpeercert()

# Block B
def get_cert_info(hostname: str, port: int = 443) -> dict:

# Block C
    context = ssl.create_default_context()

# Block D
import ssl
import socket
from datetime import datetime

# Block E
    conn = context.wrap_socket(sock, server_hostname=hostname)

# Block F
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Block G
    sock.connect((hostname, port))

# Block H
    expiry = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")

# Block I
    subject = dict(x[0] for x in cert["subject"])

# Block J
    conn.close()

# Block K
    return {"subject": subject, "expires": expiry}

# Block L (DISTRACTOR - not needed)
    context.check_hostname = False

# Block M (DISTRACTOR - not needed)
    context.verify_mode = ssl.CERT_NONE
```

### Correct Order

<details>
<summary>Click to reveal</summary>

```python
# Block D
import ssl
import socket
from datetime import datetime

# Block B
def get_cert_info(hostname: str, port: int = 443) -> dict:

# Block C
    context = ssl.create_default_context()

# Block F
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Block G
    sock.connect((hostname, port))

# Block E
    conn = context.wrap_socket(sock, server_hostname=hostname)

# Block A
    cert = conn.getpeercert()

# Block I
    subject = dict(x[0] for x in cert["subject"])

# Block H
    expiry = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")

# Block J
    conn.close()

# Block K
    return {"subject": subject, "expires": expiry}
```

**Distractor notes:**
- Block L and M disable certificate verification, which defeats the purpose of checking the certificate
- In a real verification scenario, you want the default security settings

**Key concepts:**
- `create_default_context()` creates a secure SSL context
- `wrap_socket()` upgrades a regular socket to TLS
- `server_hostname` enables SNI (Server Name Indication)
- `getpeercert()` retrieves the server's certificate as a dictionary
</details>

---

## Tips for Parsons Problems

1. **Identify imports first** — they always go at the top
2. **Look for function definitions** — `def` lines establish structure
3. **Follow variable dependencies** — a variable must be defined before use
4. **Check indentation clues** — indented blocks belong inside functions
5. **Identify distractors** — some blocks are intentionally wrong or unnecessary
6. **Think about error handling** — cleanup/close statements often come last

---

*Computer Networks — Week 10 | ASE, CSIE Bucharest*
*Parsons problems by ing. dr. Antonio Clim*
