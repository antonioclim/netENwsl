# Project 09: Multi-Client FTP Server

> **Course:** Computer Networks | **Institution:** ASE Bucharest - CSIE | **Project type:** Main

**Common guides:** [Pair Programming](../docs/common/pair_programming_guide.md) | [Code Quality](../docs/common/code_quality_standards.md) | [Git Workflow](../docs/common/git_workflow_detailed.md)

### 📅 Stage Calendar
| Stage | Week | Deliverables | Score |
|-------|------|--------------|-------|
| **E1** - Design | Week 5 | Specifications + Diagrams | 20% |
| **E2** - Prototype | Week 9 | Partial implementation | 25% |
| **E3** - Final | Week 13 | Complete version | 35% |
| **E4** - Presentation | Week 14 | Live demo | 20% |

**Repository:** `https://github.com/[username]/retele-proiect-09`

---

## 📚 Project Description

Implement a simplified FTP server supporting multiple concurrent clients. Handle basic FTP commands (USER, PASS, LIST, RETR, STOR, QUIT) with proper control and data channel separation.

### 🎯 Learning Objectives
- **Implement** FTP command protocol
- **Handle** control and data channels separately
- **Support** concurrent client connections
- **Manage** file transfers with progress tracking

---

## 🎯 Concept Analogies

### FTP Channels = Phone Call + Fax
🏠 **Analogy:** You call someone (control channel) to discuss what documents to send. Then you use a separate fax line (data channel) to actually transfer the documents. The phone call coordinates, the fax transfers.

💻 **Technical:** Port 21 for commands, port 20 (or dynamic) for data transfer.

### Active vs Passive = Who Calls Back
🏠 **Analogy:** 
- **Active:** "I'll call you back on your fax number" (server connects to client)
- **Passive:** "Use my fax number to send" (client connects to server)

💻 **Technical:** Passive mode works better with firewalls/NAT.

---

## 🗳️ Peer Instruction Questions

### Question 1: Two Channels
**Question:** Why does FTP use separate control and data channels?
- A) Security isolation
- B) Allow commands during transfer and different transfer modes ✓
- C) Historical accident
- D) Protocol limitation

**Explanation:** Separating channels allows sending commands (abort, status) during transfer and using different connection modes for data.

### Question 2: Passive Mode
**Question:** In passive mode, who initiates the data connection?
- A) Server
- B) Client ✓
- C) Both simultaneously
- D) Neither (shared channel)

**Explanation:** Client connects to server's data port. This works better through NAT/firewalls.

---

## ❌ Common Misconceptions

### 🚫 "FTP is secure"
**CORRECT:** Basic FTP sends passwords in plaintext! Use SFTP (SSH) or FTPS (TLS) for security.

### 🚫 "Binary and ASCII modes are the same"
**CORRECT:** ASCII mode converts line endings (CR/LF). Binary transfers exact bytes. Wrong mode corrupts files!

---

## 📖 Glossary
| Term | Definition |
|------|------------|
| **Control Channel** | Port 21, sends commands and responses |
| **Data Channel** | Transfers file content and listings |
| **Active Mode** | Server connects to client for data |
| **Passive Mode** | Client connects to server for data |
| **RETR** | Retrieve (download) file command |
| **STOR** | Store (upload) file command |

---

## 🔨 Implementation Example

```python
#!/usr/bin/env python3
"""FTP Server with Multi-Client Support"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import socket
import threading
import os
from typing import Optional

# ═══════════════════════════════════════════════════════════════════════════════
# FTP_COMMANDS
# ═══════════════════════════════════════════════════════════════════════════════
class FTPSession:
    """Handle single FTP client session."""
    
    def __init__(self, control_socket: socket.socket, root_dir: str):
        self.control = control_socket
        self.root = root_dir
        self.cwd = "/"
        self.authenticated = False
        self.data_socket: Optional[socket.socket] = None
    
    def send_response(self, code: int, message: str) -> None:
        """Send FTP response code and message."""
        response = f"{code} {message}\r\n"
        self.control.send(response.encode())
    
    def handle_LIST(self, args: str) -> None:
        """List directory contents."""
        if not self.data_socket:
            self.send_response(425, "Use PASV first")
            return
        
        # 💭 PREDICTION: What if directory doesn't exist?
        self.send_response(150, "Opening data connection")
        
        path = os.path.join(self.root, self.cwd.lstrip('/'))
        listing = "\r\n".join(os.listdir(path))
        
        conn, _ = self.data_socket.accept()
        conn.send(listing.encode())
        conn.close()
        
        self.send_response(226, "Transfer complete")
    
    def handle_RETR(self, filename: str) -> None:
        """Send file to client."""
        filepath = os.path.join(self.root, self.cwd.lstrip('/'), filename)
        
        if not os.path.exists(filepath):
            self.send_response(550, "File not found")
            return
        
        self.send_response(150, "Opening binary data connection")
        
        conn, _ = self.data_socket.accept()
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                conn.send(chunk)
        conn.close()
        
        self.send_response(226, "Transfer complete")

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 21))
    server.listen(5)
    
    print("FTP Server listening on port 21")
    
    while True:
        client, addr = server.accept()
        session = FTPSession(client, '/srv/ftp')
        thread = threading.Thread(target=session.run)
        thread.start()

if __name__ == "__main__":
    main()
```

---

## ❓ Frequently Asked Questions

**Q: Port 21 requires root**
A: Use port 2121 for testing, or run with sudo.

**Q: Data connection fails through NAT**
A: Implement passive mode (PASV) — client connects to server.

---

## 📚 Laboratory References

Consult these resources from **netENwsl** (https://github.com/antonioclim/netENwsl):

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 2 | `02enWSL/` | Socket programming |
| 3 | `03enWSL/` | Multi-threading, TCP tunneling |
| 9 | `09enWSL/` | FTP implementation (ex_9_02_implement_pseudo_ftp.py) |
| 11 | `11enWSL/` | FTP protocol in Docker context |

---

*Last update: January 2026 — Computer Networks, ASE Bucharest*
