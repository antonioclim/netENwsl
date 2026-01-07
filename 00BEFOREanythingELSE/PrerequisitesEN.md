# 🖧 Computer Networks Laboratory — Environment Setup Guide

> **Complete Prerequisites Documentation**  
> Academy of Economic Studies, Bucharest — Faculty of Economic Cybernetics, Statistics and Informatics  
> *Economic Informatics & AI in Economics and Business Programmes*

---

## 📋 Table of Contents

1. [Introduction](#1-introduction)
2. [Architecture Overview](#2-architecture-overview)
3. [Standard Credentials](#3-standard-credentials)
4. [Step 1: Enable WSL2](#4-step-1-enable-wsl2)
5. [Step 2: Install Ubuntu 22.04](#5-step-2-install-ubuntu-2204)
6. [Step 3: Install Docker in WSL](#6-step-3-install-docker-in-wsl)
7. [Step 4: Deploy Portainer CE](#7-step-4-deploy-portainer-ce)
8. [Step 5: Install Wireshark](#8-step-5-install-wireshark)
9. [Step 6: Python Packages](#9-step-6-python-packages)
10. [Step 7: Configure Auto-start](#10-step-7-configure-auto-start-optional)
11. [Final Verification](#11-final-verification)
12. [Troubleshooting](#12-troubleshooting)
13. [Quick Reference Card](#13-quick-reference-card)

---

## 1. Introduction

### 1.1 Purpose of This Guide

This comprehensive guide walks you through setting up a complete network laboratory environment on Windows. By the end, you will have a fully functional containerised environment capable of:

- **Running isolated network experiments** using Docker containers
- **Capturing and analysing network traffic** with Wireshark
- **Managing containers visually** through Portainer's web interface
- **Scripting network interactions** using Python

### 1.2 Why This Architecture?

We use **WSL2 + Docker inside Ubuntu** rather than Docker Desktop for several compelling reasons:

| Aspect | WSL2 + Docker | Docker Desktop |
|--------|---------------|----------------|
| **Performance** | Native Linux kernel, faster I/O | Virtualisation overhead |
| **Resource Usage** | Lighter memory footprint | Higher RAM consumption |
| **Network Access** | Full Linux networking stack | Abstracted networking |
| **Learning Value** | Real Linux environment | Windows abstraction |
| **Cost** | Completely free | Licensing for enterprises |

### 1.3 What You Will Install

| Component | Version | Purpose |
|-----------|---------|---------|
| WSL2 | 2.x | Windows Subsystem for Linux |
| Ubuntu | 22.04 LTS | Linux distribution |
| Docker | 28.2.2 | Container runtime |
| Docker Compose | 1.29.x | Multi-container orchestration |
| Portainer CE | 2.33.6 LTS | Web-based container management |
| Wireshark | 4.4.x | Network protocol analyser |
| Python packages | Latest | docker, scapy, dpkt |

### 1.4 Time Estimate

- **Total installation time:** 30-45 minutes
- **Requires restart:** Yes (after WSL2 installation)
- **Internet connection:** Required for downloads

---

## 2. Architecture Overview

### 2.1 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         WINDOWS 11                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Wireshark     │  │    Browser      │  │   PowerShell    │  │
│  │   (Capture)     │  │  (Portainer)    │  │   (Commands)    │  │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘  │
│           │                    │                    │           │
│           ▼                    ▼                    ▼           │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              vEthernet (WSL) - Virtual Network              ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│  ┌───────────────────────────┴───────────────────────────────┐  │
│  │                        WSL2                                │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │                  Ubuntu 22.04 LTS                    │  │  │
│  │  │  ┌─────────────────────────────────────────────┐    │  │  │
│  │  │  │              Docker Engine                   │    │  │  │
│  │  │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐       │    │  │  │
│  │  │  │  │Container│ │Container│ │Portainer│       │    │  │  │
│  │  │  │  │   A     │ │   B     │ │  :9000  │       │    │  │  │
│  │  │  │  └─────────┘ └─────────┘ └─────────┘       │    │  │  │
│  │  │  │         Docker Network (bridge)             │    │  │  │
│  │  │  └─────────────────────────────────────────────┘    │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Network Flow

1. **Docker containers** communicate through Docker's internal bridge network
2. **Traffic exits** through the WSL2 virtual network interface
3. **Wireshark on Windows** captures traffic on `vEthernet (WSL)`
4. **Portainer** is accessible via `localhost:9000` from Windows browser

### 2.3 Port Mapping

| Service | Container Port | Host Port | Access URL |
|---------|---------------|-----------|------------|
| Portainer | 9000 | 9000 | http://localhost:9000 |
| Portainer HTTPS | 9443 | 9443 | https://localhost:9443 |
| Portainer Edge | 8000 | 8000 | (Agent communication) |

---

## 3. Standard Credentials

> ⚠️ **Important:** Use these exact credentials for all laboratory exercises to ensure consistency.

### 3.1 Ubuntu WSL User

| Field | Value |
|-------|-------|
| **Username** | `stud` |
| **Password** | `stud` |

This user is created during Ubuntu installation and has `sudo` privileges.

### 3.2 Portainer Administrator

| Field | Value |
|-------|-------|
| **Username** | `stud` |
| **Password** | `studstudstud` |
| **Access URL** | http://localhost:9000 |

> 📝 **Note:** Portainer requires a minimum 12-character password, hence `studstudstud`.

---

## 4. Step 1: Enable WSL2

### 4.1 What is WSL2?

**Windows Subsystem for Linux 2 (WSL2)** is a compatibility layer that allows running a genuine Linux kernel directly on Windows. Unlike WSL1, which translated Linux system calls, WSL2 runs a full Linux kernel in a lightweight virtual machine, providing:

- Complete system call compatibility
- Dramatically improved file system performance
- Full Docker support without emulation
- Native Linux networking capabilities

### 4.2 System Requirements

- **Operating System:** Windows 10 version 2004+ or Windows 11
- **Architecture:** 64-bit processor with virtualisation support
- **RAM:** Minimum 4GB (8GB+ recommended)
- **BIOS:** Virtualisation enabled (VT-x/AMD-V)

### 4.3 Installation Steps

#### Step 1: Open PowerShell as Administrator

1. Press `Win + X` or right-click the Start button
2. Select **"Windows Terminal (Admin)"** or **"PowerShell (Admin)"**
3. Click **"Yes"** on the User Account Control prompt

#### Step 2: Install WSL2

Execute the following command:

```powershell
wsl --install
```

**What this command does:**
- Enables the WSL optional feature
- Enables the Virtual Machine Platform feature
- Downloads and installs the Linux kernel
- Sets WSL2 as the default version

#### Step 3: Restart Your Computer

> 🔄 **A restart is required.** Save all your work before proceeding.

```powershell
Restart-Computer
```

Or manually restart through the Start menu.

#### Step 4: Verify Installation

After restart, open PowerShell and verify:

```powershell
wsl --status
```

**Expected output:**
```
Default Distribution: Ubuntu
Default Version: 2

Windows Subsystem for Linux was last updated on [date]
WSL automatic updates are on.

Kernel version: 5.15.x.x-microsoft-standard-WSL2
```

### 4.4 Verification Checklist

- [ ] `wsl --status` shows "Default Version: 2"
- [ ] No error messages about virtualisation
- [ ] WSL service is running

---

## 5. Step 2: Install Ubuntu 22.04

### 5.1 Why Ubuntu 22.04 LTS?

**Ubuntu 22.04 LTS (Jammy Jellyfish)** is our chosen distribution because:

- **Long Term Support (LTS):** Security updates until April 2027
- **Stability:** Thoroughly tested, production-ready packages
- **Compatibility:** Excellent Docker support and documentation
- **Community:** Largest Linux community for troubleshooting

### 5.2 Installation Steps

#### Step 1: Install Ubuntu from PowerShell

Open PowerShell as Administrator and execute:

```powershell
wsl --install -d Ubuntu-22.04 --web-download
```

**Command breakdown:**
- `wsl --install`: Invokes the WSL installer
- `-d Ubuntu-22.04`: Specifies the distribution
- `--web-download`: Downloads from Microsoft servers (more reliable)

#### Step 2: Initial Setup

After download completes, Ubuntu will launch automatically. You'll see:

```
Installing, this may take a few minutes...
Please create a default UNIX user account. The username does not need to match your Windows username.
For more information visit: https://aka.ms/wslusers
Enter new UNIX username:
```

#### Step 3: Create User Account

> ⚠️ **Critical:** Use the standard credentials!

```
Enter new UNIX username: stud
New password: stud
Retype new password: stud
```

**Note:** The password won't display as you type—this is normal Linux behaviour.

#### Step 4: Verify Installation

```powershell
wsl -l -v
```

**Expected output:**
```
  NAME            STATE           VERSION
* Ubuntu-22.04    Running         2
```

### 5.3 Understanding the Ubuntu Environment

When you open Ubuntu, you're in a full Linux environment:

```
stud@HOSTNAME:~$
```

- `stud` — Your username
- `HOSTNAME` — Your computer's name
- `~` — Current directory (home folder: `/home/stud`)
- `$` — Regular user prompt (vs `#` for root)

### 5.4 Verification Checklist

- [ ] Ubuntu appears in `wsl -l -v` with VERSION 2
- [ ] Can log in as user `stud`
- [ ] Home directory is `/home/stud`

---

## 6. Step 3: Install Docker in WSL

### 6.1 What is Docker?

**Docker** is a platform for developing, shipping, and running applications in containers. A container is a lightweight, standalone, executable package that includes everything needed to run software:

- Application code
- Runtime environment
- System tools and libraries
- Configuration settings

### 6.2 Why Docker Inside WSL (Not Docker Desktop)?

| Aspect | Docker in WSL | Docker Desktop |
|--------|---------------|----------------|
| **Licensing** | Free for all uses | Paid for large companies |
| **Performance** | Native Linux performance | Additional abstraction layer |
| **Learning** | Real Linux Docker environment | Windows-specific behaviour |
| **Networking** | Standard Linux networking | Custom networking stack |

### 6.3 Installation Steps

#### Step 1: Open Ubuntu Terminal

Either:
- Click "Ubuntu" in the Start menu, or
- Type `wsl` in PowerShell

#### Step 2: Update System Packages

```bash
sudo apt update && sudo apt upgrade -y
```

**What this does:**
- `sudo`: Execute as superuser (administrator)
- `apt update`: Refresh the package list
- `apt upgrade -y`: Install all available updates (`-y` = yes to all)

**Expected duration:** 2-5 minutes depending on internet speed.

#### Step 3: Install Docker and Docker Compose

```bash
sudo apt install -y docker.io docker-compose
```

**Packages installed:**
- `docker.io`: The Docker container runtime
- `docker-compose`: Tool for defining multi-container applications

#### Step 4: Add User to Docker Group

By default, Docker requires `sudo`. To run Docker commands without `sudo`:

```bash
sudo usermod -aG docker $USER
```

**Command breakdown:**
- `usermod`: Modify user account
- `-aG docker`: Append to the `docker` group
- `$USER`: Current username (expands to `stud`)

#### Step 5: Start Docker Service

```bash
sudo service docker start
```

**Note:** In WSL2, services don't auto-start by default. We'll configure this later.

#### Step 6: Apply Group Changes

For the group change to take effect:

```bash
newgrp docker
```

Or log out and log back in:
```bash
exit
wsl
```

#### Step 7: Verify Installation

```bash
# Check Docker version
docker --version

# Check Docker Compose version
docker-compose --version

# Test Docker functionality
docker run hello-world
```

**Expected Docker version output:**
```
Docker version 28.2.2, build e6534b4
```

**Expected hello-world output:**
```
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

### 6.4 Understanding Docker Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Architecture                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐                                            │
│  │ Docker CLI  │ ◄── Commands you type (docker run, etc.)  │
│  └──────┬──────┘                                            │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────┐                                            │
│  │Docker Daemon│ ◄── Background service (dockerd)          │
│  │  (dockerd)  │                                            │
│  └──────┬──────┘                                            │
│         │                                                    │
│    ┌────┴────┬─────────────┐                                │
│    ▼         ▼             ▼                                │
│ ┌──────┐ ┌──────┐    ┌──────────┐                          │
│ │Images│ │Contai│    │ Networks │                          │
│ │      │ │-ners │    │          │                          │
│ └──────┘ └──────┘    └──────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

### 6.5 Verification Checklist

- [ ] `docker --version` shows version 28.x or higher
- [ ] `docker run hello-world` succeeds without `sudo`
- [ ] `docker ps` runs without permission errors

---

## 7. Step 4: Deploy Portainer CE

### 7.1 What is Portainer?

**Portainer Community Edition** is a lightweight management UI that allows you to easily manage your Docker environments. Features include:

- Visual container management
- Image and volume management
- Network configuration
- Log viewing
- Container console access
- Stack deployment with docker-compose

### 7.2 Why Portainer?

For learning purposes, Portainer provides:
- **Visual feedback** on container states
- **Easy debugging** through built-in console
- **Log access** without command-line complexity
- **Network visualisation** for understanding container communication

### 7.3 Installation Steps

#### Step 1: Create Persistent Volume

Docker volumes persist data beyond container lifecycle:

```bash
docker volume create portainer_data
```

**What this does:** Creates a named volume called `portainer_data` that will store Portainer's configuration, users, and settings.

#### Step 2: Deploy Portainer Container

```bash
docker run -d \
  -p 9000:9000 \
  --name portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest
```

**Command breakdown:**

| Flag | Purpose |
|------|---------|
| `-d` | Run in detached mode (background) |
| `-p 9000:9000` | Map port 9000 from container to host |
| `--name portainer` | Name the container "portainer" |
| `--restart=always` | Restart container if it stops or system reboots |
| `-v /var/run/docker.sock:...` | Give Portainer access to Docker daemon |
| `-v portainer_data:/data` | Persist Portainer data |
| `portainer/portainer-ce:latest` | Use latest Portainer CE image |

#### Step 3: Verify Deployment

```bash
docker ps
```

**Expected output:**
```
CONTAINER ID   IMAGE                           COMMAND        CREATED          STATUS          PORTS                                        NAMES
44b61d00ab18   portainer/portainer-ce:latest   "/portainer"   10 seconds ago   Up 9 seconds    8000/tcp, 9443/tcp, 0.0.0.0:9000->9000/tcp   portainer
```

### 7.4 Initial Portainer Setup

> ⏱️ **Important:** You must complete initial setup within 5 minutes of deployment!

#### Step 1: Access Portainer

Open your Windows browser and navigate to:

```
http://localhost:9000
```

#### Step 2: Create Administrator Account

On the initial setup screen:

| Field | Value |
|-------|-------|
| Username | `stud` |
| Password | `studstudstud` |
| Confirm password | `studstudstud` |

Click **"Create user"**

#### Step 3: Connect to Local Docker

On the "Environment Wizard" screen:
1. Click **"Get Started"** to use the local environment
2. Or select **"Docker"** → **"Connect"** if shown

#### Step 4: Explore the Dashboard

You should now see the Portainer dashboard with your local Docker environment connected.

### 7.5 Portainer Interface Overview

```
┌─────────────────────────────────────────────────────────────┐
│  PORTAINER.io                    [Notifications] [stud ▼]  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────────────────────────────┐  │
│  │ Home        │  │  Environment: local                 │  │
│  │ Environments│  │  ┌─────────────────────────────────┐│  │
│  │             │  │  │ Containers: 1    Running: 1    ││  │
│  │ ─────────── │  │  │ Images: 2        Volumes: 1    ││  │
│  │ Containers  │  │  │ Networks: 3                     ││  │
│  │ Images      │  │  └─────────────────────────────────┘│  │
│  │ Networks    │  │                                     │  │
│  │ Volumes     │  │                                     │  │
│  │ Stacks      │  │                                     │  │
│  └─────────────┘  └─────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 7.6 Verification Checklist

- [ ] `docker ps` shows portainer container running
- [ ] http://localhost:9000 loads in Windows browser
- [ ] Can log in with stud/studstudstud
- [ ] Dashboard shows "local" Docker environment

---

## 8. Step 5: Install Wireshark

### 8.1 What is Wireshark?

**Wireshark** is the world's foremost and widely-used network protocol analyser. It allows you to:

- **Capture** live network traffic in real-time
- **Inspect** packets at multiple protocol layers
- **Filter** traffic by various criteria
- **Analyse** network behaviour and troubleshoot issues
- **Export** captures for later analysis

### 8.2 Why Wireshark on Windows?

We install Wireshark on Windows (not in WSL) because:

1. **GUI Performance:** Native Windows application with better graphics
2. **Interface Access:** Direct access to Windows network interfaces
3. **WSL Traffic:** The `vEthernet (WSL)` interface captures all WSL traffic
4. **Integration:** Easy file saving and sharing on Windows

### 8.3 Installation Steps

#### Step 1: Download Wireshark

1. Visit: https://www.wireshark.org/download.html
2. Click **"Windows x64 Installer"**
3. Save the installer file

#### Step 2: Run the Installer

1. Double-click the downloaded `.exe` file
2. Click **"Yes"** on User Account Control prompt
3. Follow the installation wizard with default options

#### Step 3: Install Npcap

> ⚠️ **Critical:** Npcap is required for packet capture!

During Wireshark installation, you'll be prompted to install Npcap:

1. Click **"Install"** when prompted for Npcap
2. In Npcap installer, ensure these options are checked:
   - ✅ **Install Npcap in WinPcap API-compatible Mode**
   - ✅ **Support raw 802.11 traffic (for wireless packet capture)**
3. Complete Npcap installation
4. Continue with Wireshark installation

#### Step 4: Complete Installation

1. Finish the Wireshark installer
2. Optionally, restart your computer if prompted

### 8.4 Wireshark Interface Selection

When you open Wireshark, you'll see a list of network interfaces. For capturing Docker/WSL traffic:

| Interface | Description | Use For |
|-----------|-------------|---------|
| **vEthernet (WSL)** | WSL2 virtual network | Docker container traffic |
| **vEthernet (WSL) (Hyper-V firewall)** | Same, with firewall | Docker container traffic |
| Ethernet | Physical network card | External traffic |
| Wi-Fi | Wireless adapter | External wireless traffic |

### 8.5 Basic Wireshark Usage

#### Starting a Capture

1. Open Wireshark from Start menu
2. Double-click on **"vEthernet (WSL)"** interface
3. Capture begins immediately

#### Useful Display Filters

| Filter | Purpose |
|--------|---------|
| `icmp` | Show only ping (ICMP) packets |
| `tcp` | Show only TCP packets |
| `http` | Show only HTTP traffic |
| `dns` | Show only DNS queries |
| `ip.addr == 172.17.0.2` | Filter by IP address |
| `tcp.port == 80` | Filter by port |

#### Stopping a Capture

- Click the red **Stop** button in toolbar
- Or press `Ctrl + E`

### 8.6 Verification Checklist

- [ ] Wireshark launches from Start menu
- [ ] Network interfaces are visible
- [ ] "vEthernet (WSL)" interface is present
- [ ] Can start and stop a capture

---

## 9. Step 6: Python Packages

### 9.1 Why Python for Networking?

Python is widely used for network automation and analysis:

- **docker**: Programmatic container management
- **scapy**: Packet manipulation and creation
- **dpkt**: Fast packet parsing

### 9.2 Prerequisites

Ensure Python 3.11+ is installed on Windows:

```powershell
python --version
```

If not installed, download from: https://www.python.org/downloads/

### 9.3 Installation Steps

Open PowerShell or Command Prompt:

```powershell
# Install Docker SDK
pip install docker

# Install network analysis packages
pip install scapy dpkt

# Verify installation
python -c "import docker; print('Docker SDK: OK')"
python -c "import scapy; print('Scapy: OK')"
python -c "import dpkt; print('dpkt: OK')"
```

### 9.4 Package Overview

#### docker (Python Docker SDK)

```python
import docker
client = docker.from_env()

# List containers
for container in client.containers.list():
    print(container.name, container.status)

# Run a container
container = client.containers.run("alpine", "echo hello", detach=True)
```

#### scapy (Packet Manipulation)

```python
from scapy.all import *

# Create and send a ping packet
packet = IP(dst="8.8.8.8")/ICMP()
response = sr1(packet, timeout=2)
print(response.summary())
```

#### dpkt (Packet Parsing)

```python
import dpkt

# Parse a pcap file
with open('capture.pcap', 'rb') as f:
    pcap = dpkt.pcap.Reader(f)
    for timestamp, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        print(eth)
```

### 9.5 Verification Checklist

- [ ] `pip show docker` displays package information
- [ ] `pip show scapy` displays package information
- [ ] `pip show dpkt` displays package information
- [ ] Import statements work without errors

---

## 10. Step 7: Configure Auto-start (Optional)

### 10.1 Why Auto-start?

By default, WSL2 doesn't start services automatically. Every time you open Ubuntu, you'd need to:

```bash
sudo service docker start
```

Auto-start configuration eliminates this manual step.

### 10.2 Configuration Steps

#### Step 1: Add Auto-start to Bash Profile

Open Ubuntu terminal and execute:

```bash
cat >> ~/.bashrc << 'EOF'

# Auto-start Docker service
if ! pgrep -x "dockerd" > /dev/null; then
    sudo service docker start > /dev/null 2>&1
fi
EOF
```

**What this does:**
- Appends code to `~/.bashrc` (executed on every terminal open)
- Checks if `dockerd` is running (`pgrep`)
- If not running, starts Docker service

#### Step 2: Allow Passwordless Docker Start

Create a sudoers exception:

```bash
echo 'stud ALL=(ALL) NOPASSWD: /usr/sbin/service docker start' | sudo tee /etc/sudoers.d/docker-start
sudo chmod 440 /etc/sudoers.d/docker-start
```

**What this does:**
- Creates file `/etc/sudoers.d/docker-start`
- Allows user `stud` to run `service docker start` without password
- Sets secure permissions (read-only for root and sudoers)

#### Step 3: Test Auto-start

```powershell
# In PowerShell, shutdown WSL completely
wsl --shutdown

# Reopen Ubuntu
wsl

# Docker should start automatically
docker ps
```

### 10.3 Verification Checklist

- [ ] Docker starts automatically when opening Ubuntu
- [ ] No password prompt for Docker service
- [ ] `docker ps` works immediately after opening Ubuntu

---

## 11. Final Verification

### 11.1 Complete System Test

#### Test 1: Docker and Portainer

```bash
# In Ubuntu terminal
docker ps
```

**Expected:** Portainer container running.

#### Test 2: Wireshark Capture

1. Open Wireshark on Windows
2. Start capture on **vEthernet (WSL)**
3. In Ubuntu, run:

```bash
docker run --rm alpine ping -c 5 8.8.8.8
```

4. In Wireshark, apply filter: `icmp`
5. Verify you see ICMP Echo Request and Reply packets

**Expected Wireshark Output:**

| No. | Time | Source | Destination | Protocol | Info |
|-----|------|--------|-------------|----------|------|
| 1 | 0.000 | 172.27.159.165 | 8.8.8.8 | ICMP | Echo request |
| 2 | 0.087 | 8.8.8.8 | 172.27.159.165 | ICMP | Echo reply |

#### Test 3: Python Integration

```powershell
# In PowerShell
python -c "import docker; c = docker.from_env(); print(f'Containers: {len(c.containers.list())}')"
```

**Expected:** `Containers: 1` (or more)

### 11.2 Component Summary

| Component | Version | Status Check |
|-----------|---------|--------------|
| WSL2 | 2.x | `wsl --status` |
| Ubuntu | 22.04 LTS | `lsb_release -a` |
| Docker | 28.2.2 | `docker --version` |
| Docker Compose | 1.29.x | `docker-compose --version` |
| Portainer | 2.33.6 LTS | http://localhost:9000 |
| Wireshark | 4.4.x | Application launch |
| Python docker | 7.1.0 | `pip show docker` |
| Python scapy | 2.7.0 | `pip show scapy` |
| Python dpkt | 1.9.8 | `pip show dpkt` |

### 11.3 Quick Verification Script

Create and run this verification script:

```bash
#!/bin/bash
echo "=== WSL Status ==="
wsl.exe --status 2>/dev/null || echo "Run from Windows"

echo ""
echo "=== Ubuntu Version ==="
lsb_release -d

echo ""
echo "=== Docker Version ==="
docker --version

echo ""
echo "=== Docker Compose Version ==="
docker-compose --version

echo ""
echo "=== Running Containers ==="
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "=== Portainer Status ==="
docker ps --filter name=portainer --format "{{.Status}}"

echo ""
echo "=== Docker Networks ==="
docker network ls

echo ""
echo "✅ All checks complete!"
```

---

## 12. Troubleshooting

### 12.1 WSL Issues

#### "WSL 2 requires an update to its kernel component"

```powershell
wsl --update
```

#### "Please enable the Virtual Machine Platform Windows feature"

```powershell
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```
Restart computer after.

#### WSL won't start

```powershell
# Reset WSL
wsl --shutdown
wsl
```

### 12.2 Docker Issues

#### "Cannot connect to the Docker daemon"

```bash
# Start Docker service
sudo service docker start

# Check if dockerd is running
ps aux | grep dockerd
```

#### "Permission denied while trying to connect to Docker daemon socket"

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Apply changes
newgrp docker
# Or log out and back in
```

#### "docker: command not found" in PowerShell

This is expected. Docker is installed in WSL, not Windows. Use:

```powershell
wsl docker ps
```

### 12.3 Portainer Issues

#### Can't access http://localhost:9000

1. Check if container is running:
```bash
docker ps | grep portainer
```

2. If not running, check logs:
```bash
docker logs portainer
```

3. Restart Portainer:
```bash
docker restart portainer
```

#### "Portainer has been initialized already"

If you missed the 5-minute window:

```bash
# Remove Portainer and volume
docker stop portainer
docker rm portainer
docker volume rm portainer_data

# Redeploy
docker volume create portainer_data
docker run -d -p 9000:9000 --name portainer --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest
```

### 12.4 Wireshark Issues

#### No interfaces visible

- Ensure Npcap is installed
- Run Wireshark as Administrator
- Reinstall Npcap from https://npcap.com/

#### "vEthernet (WSL)" not showing

- WSL must be running
- Try: `wsl` in PowerShell, then restart Wireshark

#### No traffic captured

- Ensure capture is on correct interface
- Generate traffic: `docker run --rm alpine ping -c 3 8.8.8.8`
- Check display filter isn't too restrictive

---

## 13. Quick Reference Card

### Essential Commands

```bash
# WSL Management (PowerShell)
wsl --status           # Check WSL status
wsl --shutdown         # Stop all WSL instances
wsl                    # Open default distribution
wsl -l -v              # List distributions

# Docker (Ubuntu Terminal)
docker ps              # List running containers
docker ps -a           # List all containers
docker images          # List images
docker logs <name>     # View container logs
docker exec -it <name> sh  # Shell into container
docker stop <name>     # Stop container
docker rm <name>       # Remove container

# Service Management (Ubuntu Terminal)
sudo service docker start   # Start Docker
sudo service docker status  # Check Docker status
sudo service docker stop    # Stop Docker
```

### Important URLs

| Service | URL |
|---------|-----|
| Portainer | http://localhost:9000 |
| Docker Docs | https://docs.docker.com/ |
| Wireshark Docs | https://www.wireshark.org/docs/ |
| WSL Docs | https://learn.microsoft.com/en-us/windows/wsl/ |

### Credentials

| Service | Username | Password |
|---------|----------|----------|
| Ubuntu WSL | stud | stud |
| Portainer | stud | studstudstud |

---

## 🎉 Setup Complete!

Your laboratory environment is fully configured. You can now:

- ✅ Run isolated network experiments with Docker containers
- ✅ Capture and analyse traffic with Wireshark
- ✅ Manage containers through Portainer's web interface
- ✅ Automate network tasks with Python

**Next Steps:**
- Explore Portainer's interface
- Try creating custom Docker networks
- Practice Wireshark filtering
- Run your first laboratory exercise

---

*Computer Networks Laboratory — ASE Bucharest, CSIE*  
*Documentation version: January 2026*
