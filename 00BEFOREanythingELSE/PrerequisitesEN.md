# 🖧 Computer Networks Laboratory — Complete Environment Setup Guide

> **Complete Prerequisites Documentation**  
> Academy of Economic Studies, Bucharest — Faculty of Economic Cybernetics, Statistics and Informatics  
> *Economic Informatics & AI in Economics and Business Programmes*

---

## 📋 Table of Contents

1. [Introduction](#1-introduction)
2. [⚠️ Important Clarification: Docker Desktop is NOT Required](#2-️-important-clarification-docker-desktop-is-not-required)
3. [Architecture Overview](#3-architecture-overview)
4. [Standard Credentials](#4-standard-credentials)
5. [Step 1: Enable WSL2](#5-step-1-enable-wsl2)
6. [Step 2: Install Ubuntu 22.04](#6-step-2-install-ubuntu-2204)
7. [Step 3: Install Docker in WSL](#7-step-3-install-docker-in-wsl)
8. [Step 4: Deploy Portainer CE](#8-step-4-deploy-portainer-ce)
9. [Step 5: Install Wireshark](#9-step-5-install-wireshark)
10. [Step 6: Python Packages](#10-step-6-python-packages)
11. [Step 7: Configure Auto-start](#11-step-7-configure-auto-start-optional)
12. [Final Verification](#12-final-verification)
13. [Complete Portainer Usage Guide](#13-complete-portainer-usage-guide)
14. [Complete Wireshark Usage Guide](#14-complete-wireshark-usage-guide)
15. [Troubleshooting](#15-troubleshooting)
16. [Quick Reference Card](#16-quick-reference-card)

---

## 1. Introduction

### 1.1 Purpose of This Guide

This comprehensive guide walks you through setting up a complete network laboratory environment on Windows. By the end, you will have a fully functional containerised environment capable of:

- **Running isolated network experiments** using Docker containers
- **Capturing and analysing network traffic** with Wireshark
- **Managing containers visually** through Portainer's web interface
- **Scripting network interactions** using Python

### 1.2 What You Will Learn

Beyond environment setup, this guide provides:

- **Deep understanding** of WSL2 and Docker architecture
- **Practical knowledge** about containerisation and networking
- **Troubleshooting skills** for common issues
- **Solid foundation** for all semester laboratories

### 1.3 What You Will Install

| Component | Version | Purpose | Where Installed |
|-----------|---------|---------|-----------------|
| WSL2 | 2.x | Windows Subsystem for Linux | Windows (built-in feature) |
| Ubuntu | 22.04 LTS | Linux distribution | Inside WSL2 |
| Docker Engine | 28.2.2 | Container runtime | Inside Ubuntu (WSL) |
| Docker Compose | 1.29.x | Multi-container orchestration | Inside Ubuntu (WSL) |
| Portainer CE | 2.33.6 LTS | Web-based container management | Docker container (in WSL) |
| Wireshark | 4.4.x | Network protocol analyser | Windows (native application) |
| Python packages | Latest | docker, scapy, dpkt | Windows (optionally also in WSL) |

### 1.4 Time Estimate

- **Total installation time:** 30-45 minutes
- **Requires restart:** Yes (after WSL2 installation)
- **Internet connection:** Required for downloads
- **Difficulty level:** Beginner-Intermediate

---

## 2. ⚠️ Important Clarification: Docker Desktop is NOT Required

### 2.1 The Architectural Decision

> **🚫 DO NOT INSTALL Docker Desktop!**
>
> In this laboratory we use **Docker Engine installed directly inside Ubuntu (WSL)**, not Docker Desktop for Windows.

This decision is intentional and brings multiple educational and practical benefits.

### 2.2 What is Docker Desktop and Why We DON'T Use It

**Docker Desktop** is a Windows application that:
- Installs a GUI for managing Docker
- Creates its own virtualisation environment
- Costs money for companies (commercial licence)
- Adds an extra abstraction layer

**Instead**, we install **Docker Engine** directly in Ubuntu (running in WSL2):
- It's the exact same Docker used on real Linux servers
- It's completely free for any use
- It provides direct access to all Docker features
- It teaches you to work with Docker as it's used in industry

### 2.3 Detailed Comparison: Docker in WSL vs Docker Desktop

| Aspect | Docker in WSL (What We Use) | Docker Desktop (NOT Used) |
|--------|----------------------------|---------------------------|
| **Licensing** | ✅ 100% free, open source | ⚠️ Free personal, paid for companies >250 employees |
| **Performance** | ✅ Native Linux kernel, fast I/O | ⚠️ Additional virtualisation layer |
| **Memory Usage** | ✅ ~500MB-1GB | ⚠️ 2-4GB minimum |
| **Startup Time** | ✅ Instant (Linux service) | ⚠️ 30-60 seconds |
| **Network Access** | ✅ Full Linux networking stack | ⚠️ Abstracted networking, complex NAT |
| **Educational Value** | ✅ Real Linux environment, learn real commands | ⚠️ Abstraction, hides details |
| **Compatibility** | ✅ Identical to production servers | ⚠️ Sometimes different behaviour |
| **Debugging** | ✅ Direct access to logs, processes | ⚠️ Limited GUI interface |
| **Updates** | ✅ `apt update && apt upgrade` | ⚠️ Automatic updates that can cause issues |

### 2.4 Our Architecture (Correct)

```
┌─────────────────────────────────────────────────────────────────┐
│                         WINDOWS 11                               │
│                                                                  │
│   ❌ Docker Desktop - NOT INSTALLED, NOT REQUIRED               │
│                                                                  │
│   ✅ Native Windows Applications:                               │
│      • Wireshark (traffic capture)                              │
│      • Browser (Portainer access)                               │
│      • PowerShell (WSL commands)                                │
│      • VS Code (optional, code editing)                         │
│                                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                        WSL2                              │   │
│   │   ┌─────────────────────────────────────────────────┐   │   │
│   │   │              Ubuntu 22.04 LTS                    │   │   │
│   │   │                                                  │   │   │
│   │   │   ✅ Docker Engine (docker.io)                  │   │   │
│   │   │      └── Portainer CE (container, port 9000)    │   │   │
│   │   │      └── Laboratory containers                  │   │   │
│   │   │      └── Docker networks (bridge)               │   │   │
│   │   │                                                  │   │   │
│   │   │   ✅ Docker Compose (docker-compose)            │   │   │
│   │   │   ✅ Python packages (optional)                 │   │   │
│   │   └─────────────────────────────────────────────────┘   │   │
│   └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 2.5 What To Do If You Have Docker Desktop Installed

If you have already installed Docker Desktop, you have two options:

**Option A: Uninstall Docker Desktop (Recommended)**
1. Open **Settings → Apps → Installed Apps**
2. Find **Docker Desktop**
3. Click **Uninstall**
4. Restart your computer
5. Continue with this guide

**Option B: Keep Docker Desktop but Configure Correctly**

If you need Docker Desktop for other projects:
1. Open Docker Desktop → Settings → Resources → WSL Integration
2. **Disable** integration with Ubuntu-22.04
3. This allows you to have Docker separately in WSL

> ⚠️ **Recommendation:** For this laboratory, uninstalling Docker Desktop simplifies things and avoids confusion.

### 2.6 The Correct Workflow

Here's what a typical laboratory session looks like:

```
1. Start Windows
   └── WSL2 and Ubuntu are already installed (nothing to do)

2. Open Ubuntu
   └── From Start Menu: click "Ubuntu"
   └── Or from PowerShell: type "wsl"

3. Start Docker (if not already running)
   └── stud@PC:~$ sudo service docker start
   └── Password: stud

4. Verify Portainer is running
   └── stud@PC:~$ docker ps
   └── You should see the "portainer" container

5. Access Portainer from Windows browser
   └── http://localhost:9000
   └── Login: stud / studstudstud

6. Navigate to laboratory directory
   └── stud@PC:~$ cd /mnt/d/NETWORKING/WEEK7

7. Start laboratory containers
   └── stud@PC:/mnt/d/NETWORKING/WEEK7$ python scripts/start_lab.py

8. Work on exercises...

9. At the end, stop laboratory containers
   └── stud@PC:/mnt/d/NETWORKING/WEEK7$ python scripts/stop_lab.py
   └── Portainer stays active for future sessions!
```

---

## 3. Architecture Overview

### 3.1 Complete System Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            WINDOWS 11                                    │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  │
│  │  Wireshark   │  │   Browser    │  │  PowerShell  │  │   VS Code   │  │
│  │  (Traffic    │  │ (Portainer   │  │  (WSL        │  │  (Code      │  │
│  │   capture)   │  │  GUI)        │  │   commands)  │  │   editor)   │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬──────┘  │
│         │                 │                 │                 │         │
│         │           localhost:9000          │                 │         │
│         │                 │                 │                 │         │
│         ▼                 ▼                 ▼                 ▼         │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │              vEthernet (WSL) - Virtual Network Adapter           │   │
│  │                     (Visible in Wireshark)                        │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                    │                                     │
│                                    │ Network traffic                    │
│                                    ▼                                     │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                           WSL2                                    │   │
│  │                  (Real Linux kernel in lightweight VM)            │   │
│  │                                                                   │   │
│  │  ┌────────────────────────────────────────────────────────────┐  │   │
│  │  │                    Ubuntu 22.04 LTS                         │  │   │
│  │  │                (Default WSL distribution)                   │  │   │
│  │  │                                                             │  │   │
│  │  │  User: stud    Home: /home/stud    Password: stud          │  │   │
│  │  │                                                             │  │   │
│  │  │  ┌──────────────────────────────────────────────────────┐  │  │   │
│  │  │  │               Docker Engine (docker.io)               │  │  │   │
│  │  │  │                   Service: dockerd                    │  │  │   │
│  │  │  │                                                       │  │  │   │
│  │  │  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐ │  │  │   │
│  │  │  │  │  Portainer  │ │ week7_lab   │ │ Other lab       │ │  │  │   │
│  │  │  │  │   :9000     │ │   :9090     │ │ containers      │ │  │  │   │
│  │  │  │  │  (global)   │ │   :9091     │ │                 │ │  │  │   │
│  │  │  │  └─────────────┘ └─────────────┘ └─────────────────┘ │  │  │   │
│  │  │  │                                                       │  │  │   │
│  │  │  │  ┌─────────────────────────────────────────────────┐ │  │  │   │
│  │  │  │  │         Docker Networks (bridge networks)        │ │  │  │   │
│  │  │  │  │   • bridge (default)                            │ │  │  │   │
│  │  │  │  │   • week7_network (172.20.7.0/24)               │ │  │  │   │
│  │  │  │  │   • other lab networks...                       │ │  │  │   │
│  │  │  │  └─────────────────────────────────────────────────┘ │  │  │   │
│  │  │  └──────────────────────────────────────────────────────┘  │  │   │
│  │  └────────────────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Network Data Flow

Understanding data flow is essential for troubleshooting and analysis:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Network Traffic Flow                          │
└─────────────────────────────────────────────────────────────────┘

Container A (172.20.7.2)              Container B (172.20.7.3)
     │                                       │
     │ Packet: "Hello"                       │
     └──────────────────┬────────────────────┘
                        │
                        ▼
              ┌─────────────────┐
              │  Docker Bridge   │
              │ (week7_network)  │
              │  172.20.7.0/24   │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Docker Engine   │
              │    (dockerd)     │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   Ubuntu eth0    │
              │  (WSL interface) │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ vEthernet (WSL)  │  ◄── Wireshark captures HERE
              │ (Windows virtual)│
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Windows Network │
              │     Stack        │
              └─────────────────┘
```

### 3.3 Port Mapping

Ports are essential for accessing services from containers:

| Service | Container Port | Host Port (Windows) | Access URL | Notes |
|---------|----------------|---------------------|------------|-------|
| **Portainer** | 9000 | **9000** | http://localhost:9000 | ⚠️ PERMANENTLY RESERVED |
| Portainer HTTPS | 9443 | 9443 | https://localhost:9443 | Optional, with certificate |
| Portainer Edge | 8000 | 8000 | - | For agents |
| Lab TCP | 9090 | 9090 | localhost:9090 | Varies per laboratory |
| Lab UDP | 9091 | 9091 | localhost:9091 | Varies per laboratory |

> ⚠️ **Important Rule:** Port 9000 is ALWAYS reserved for Portainer. No laboratory should use this port.

### 3.4 File Access Between Windows and WSL

WSL automatically mounts Windows drives under `/mnt/`:

| Windows Path | WSL Path |
|--------------|----------|
| `C:\Users\` | `/mnt/c/Users/` |
| `D:\NETWORKING\` | `/mnt/d/NETWORKING/` |
| `E:\Projects\` | `/mnt/e/Projects/` |

**Practical example:**
```bash
# In Ubuntu, access files from D:\NETWORKING\WEEK7
cd /mnt/d/NETWORKING/WEEK7

# List contents
ls -la

# Edit a file with nano
nano README.md
```

---

## 4. Standard Credentials

> ⚠️ **Important:** Use these exact credentials for all laboratory exercises to ensure consistency.

### 4.1 Ubuntu WSL User

| Field | Value | Explanation |
|-------|-------|-------------|
| **Username** | `stud` | Main laboratory account |
| **Password** | `stud` | Simple, easy to remember |
| **Rights** | `sudo` | Can execute administrative commands |
| **Home directory** | `/home/stud` | Personal directory |

This user is created during Ubuntu installation and has `sudo` privileges.

### 4.2 Portainer Administrator

| Field | Value | Explanation |
|-------|-------|-------------|
| **Username** | `stud` | Consistent with Ubuntu user |
| **Password** | `studstudstud` | 12 characters (Portainer minimum requirement) |
| **Access URL** | http://localhost:9000 | From any Windows browser |
| **Session timeout** | 8 hours | Re-authentication required after |

> 📝 **Why `studstudstud`?** Portainer requires a minimum 12-character password for security. We chose to repeat `stud` three times to make it easy to remember.

### 4.3 Credentials Summary Table

```
┌─────────────────────────────────────────────────────────────┐
│              STANDARD LABORATORY CREDENTIALS                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Ubuntu WSL                                                  │
│  ──────────                                                  │
│  Username: stud                                              │
│  Password: stud                                              │
│                                                              │
│  Portainer                                                   │
│  ─────────                                                   │
│  URL:      http://localhost:9000                             │
│  Username: stud                                              │
│  Password: studstudstud                                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Step 1: Enable WSL2

### 5.1 What is WSL2?

**Windows Subsystem for Linux 2 (WSL2)** is a compatibility layer that allows running a genuine Linux kernel directly on Windows.

#### Differences Between WSL1 and WSL2

| Aspect | WSL1 | WSL2 |
|--------|------|------|
| Kernel | System call translation | Real Linux kernel |
| File Performance | Fast on /mnt/c | Fast on Linux filesystem |
| Compatibility | Limited | Complete |
| Docker | Doesn't work | Works natively |
| Networking | Shared with Windows | Own virtual network |

#### Benefits of WSL2 for Laboratory:
- ✅ Complete Linux system call compatibility
- ✅ Dramatically improved performance
- ✅ Full Docker support, no emulation
- ✅ Native Linux networking capabilities
- ✅ You can run the same commands as on a real Linux server

### 5.2 System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **Operating System** | Windows 10 v2004+ | Windows 11 |
| **Architecture** | 64-bit | 64-bit |
| **RAM** | 4 GB | 8 GB+ |
| **Processor** | With virtualisation (VT-x/AMD-V) | Intel Core i5+ / AMD Ryzen 5+ |
| **Disk Space** | 10 GB free | 20 GB+ free |
| **BIOS** | Virtualisation enabled | Virtualisation enabled |

#### Checking Virtualisation Support

1. Press `Ctrl + Shift + Esc` for Task Manager
2. Go to **Performance** tab
3. Click on **CPU**
4. Look for **Virtualization: Enabled**

If it says "Disabled", you need to enable virtualisation in BIOS.

### 5.3 Installation Steps

#### Step 1: Open PowerShell as Administrator

1. Press `Win + X` or right-click the Start button
2. Select **"Windows Terminal (Admin)"** or **"PowerShell (Admin)"**
3. Click **"Yes"** at the User Account Control prompt

> 💡 **Visual indicator:** The window title will contain "Administrator"

#### Step 2: Install WSL2

Execute the following command:

```powershell
wsl --install
```

**What this command does:**
- ✅ Enables the optional WSL feature
- ✅ Enables the Virtual Machine Platform feature
- ✅ Downloads and installs the Linux kernel for WSL2
- ✅ Sets WSL2 as the default version
- ✅ Downloads Ubuntu (default distribution)

**Expected output:**
```
Installing: Virtual Machine Platform
Virtual Machine Platform has been installed.
Installing: Windows Subsystem for Linux
Windows Subsystem for Linux has been installed.
Installing: Ubuntu
Ubuntu has been installed.
The requested operation is successful. Changes will not be effective until the system is rebooted.
```

#### Step 3: Restart Computer

> 🔄 **A restart is required.** Save all work before continuing.

```powershell
Restart-Computer
```

Or restart manually: Start → Power → Restart

#### Step 4: Verify Installation

After restart, open PowerShell (Administrator not required) and verify:

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

#### Step 5: Update WSL (Optional but Recommended)

```powershell
wsl --update
```

### 5.4 Verifying WSL Version

```powershell
wsl -l -v
```

**Expected output:**
```
  NAME            STATE           VERSION
* Ubuntu          Running         2
```

> ⚠️ **Important:** Make sure VERSION is **2**, not 1!

### 5.5 Checklist

- [ ] `wsl --status` shows "Default Version: 2"
- [ ] `wsl -l -v` shows Ubuntu with VERSION 2
- [ ] No errors about virtualisation
- [ ] Computer has been restarted after installation

---

## 6. Step 2: Install Ubuntu 22.04

### 6.1 Why Ubuntu 22.04 LTS?

**Ubuntu 22.04 LTS (Jammy Jellyfish)** is our chosen distribution because:

| Reason | Explanation |
|--------|-------------|
| **LTS (Long Term Support)** | Security updates until April 2027 |
| **Stability** | Thoroughly tested packages, production-ready |
| **Docker Compatibility** | Excellent support, vast documentation |
| **Community** | Largest Linux community, help available |
| **Consistency** | Same environment as industry servers |

### 6.2 Installation Steps

#### Step 1: Install Ubuntu from PowerShell

Open PowerShell as Administrator and execute:

```powershell
wsl --install -d Ubuntu-22.04 --web-download
```

**Command explanation:**
| Parameter | Purpose |
|-----------|---------|
| `wsl --install` | Invokes WSL installer |
| `-d Ubuntu-22.04` | Specifies Ubuntu 22.04 distribution |
| `--web-download` | Downloads from Microsoft servers (more reliable) |

**Expected duration:** 5-15 minutes depending on internet speed.

#### Step 2: Initial Configuration

After download completes, Ubuntu will start automatically. You will see:

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

**Important note:** The password will not display while typing - this is normal Linux behaviour for security reasons. Type confidently and press Enter.

**Success output:**
```
passwd: password updated successfully
Installation successful!
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

Welcome to Ubuntu 22.04 LTS (GNU/Linux 5.15.x.x-microsoft-standard-WSL2 x86_64)

stud@HOSTNAME:~$
```

#### Step 4: Verify Installation

```powershell
wsl -l -v
```

**Expected output:**
```
  NAME            STATE           VERSION
* Ubuntu-22.04    Running         2
```

### 6.3 Set Ubuntu 22.04 as Default Distribution

If you have multiple WSL distributions, set Ubuntu 22.04 as default:

```powershell
wsl --set-default Ubuntu-22.04
```

### 6.4 Understanding the Ubuntu Environment

When you open Ubuntu, you're in a complete Linux environment:

```
stud@HOSTNAME:~$
```

| Element | Meaning |
|---------|---------|
| `stud` | Your username |
| `@` | Separator |
| `HOSTNAME` | Your Windows computer name |
| `:` | Separator |
| `~` | Current directory (home: `/home/stud`) |
| `$` | Regular user prompt (vs `#` for root) |

### 6.5 Basic Linux Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `pwd` | Print working directory | `pwd` → `/home/stud` |
| `ls` | List files | `ls -la` |
| `cd` | Change directory | `cd /mnt/d/NETWORKING` |
| `mkdir` | Create directory | `mkdir project` |
| `cat` | Display file contents | `cat file.txt` |
| `sudo` | Execute as administrator | `sudo apt update` |

### 6.6 Checklist

- [ ] Ubuntu-22.04 appears in `wsl -l -v` with VERSION 2
- [ ] It's marked with `*` (default distribution)
- [ ] You can log in as user `stud`
- [ ] Home directory is `/home/stud`
- [ ] Command `pwd` shows `/home/stud`

---

## 7. Step 3: Install Docker in WSL

### 7.1 What is Docker?

**Docker** is a platform for developing, shipping, and running applications in containers.

#### What is a Container?

A container is a lightweight, standalone, executable package that includes:
- Application code
- Runtime environment
- Libraries and dependencies
- Configuration settings

#### Analogy: Container vs Virtual Machine

```
┌─────────────────────────────────────────────────────────────────┐
│                    Virtual Machine (VM)                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   App A      │  │   App B      │  │   App C      │          │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤          │
│  │  Libraries   │  │  Libraries   │  │  Libraries   │          │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤          │
│  │  Guest OS    │  │  Guest OS    │  │  Guest OS    │  ← Heavy!│
│  │  (GB)        │  │  (GB)        │  │  (GB)        │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Hypervisor                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Host OS                               │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       Docker Containers                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   App A      │  │   App B      │  │   App C      │          │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤          │
│  │  Libraries   │  │  Libraries   │  │  Libraries   │  ← Light!│
│  │  (MB)        │  │  (MB)        │  │  (MB)        │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Docker Engine                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Host OS (Linux)                       │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 Why Docker in WSL (Not Docker Desktop)?

We discussed this topic in detail in Section 2. Summary:

| Aspect | Docker in WSL ✅ | Docker Desktop ❌ |
|--------|------------------|-------------------|
| Cost | Free | Paid for companies |
| Performance | Native Linux | Virtualisation overhead |
| Learning | Real Linux commands | Abstraction |
| Compatibility | Identical to servers | Sometimes different |

### 7.3 Installation Steps

#### Step 1: Open Ubuntu Terminal

Two methods:
- **Method 1:** Click "Ubuntu" in Windows Start menu
- **Method 2:** In PowerShell, type `wsl` and press Enter

#### Step 2: Update System Packages

```bash
sudo apt update && sudo apt upgrade -y
```

**What this does:**
| Command | Purpose |
|---------|---------|
| `sudo` | Execute as superuser (administrator) |
| `apt update` | Refresh available package list |
| `&&` | Execute next command only if first succeeds |
| `apt upgrade -y` | Install all updates (`-y` = yes to all) |

**Expected duration:** 2-5 minutes depending on internet speed.

When asked for password, enter: `stud`

#### Step 3: Install Docker and Docker Compose

```bash
sudo apt install -y docker.io docker-compose
```

**Packages installed:**
| Package | Description |
|---------|-------------|
| `docker.io` | Docker container runtime |
| `docker-compose` | Tool for defining multi-container applications |

#### Step 4: Add User to Docker Group

By default, Docker requires `sudo` for every command. To run Docker commands without `sudo`:

```bash
sudo usermod -aG docker $USER
```

**Command explanation:**
| Element | Purpose |
|---------|---------|
| `usermod` | Modify user account |
| `-a` | Append (add, don't replace) |
| `-G docker` | To the `docker` group |
| `$USER` | Variable containing current username (`stud`) |

#### Step 5: Start Docker Service

```bash
sudo service docker start
```

**What happens:** Starts the Docker daemon (`dockerd`) which listens for commands.

#### Step 6: Apply Group Changes

For the group change to take effect, you have two options:

**Option A: newgrp (quick, temporary)**
```bash
newgrp docker
```

**Option B: Logout/Login (permanent)**
```bash
exit
```
Then open Ubuntu again.

#### Step 7: Verify Installation

```bash
# Check Docker version
docker --version

# Check Docker Compose version
docker-compose --version

# Test Docker functionality (without sudo!)
docker run hello-world
```

**Expected output for `docker --version`:**
```
Docker version 28.2.2, build e6534b4
```

**Expected output for `docker run hello-world`:**
```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
...
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

### 7.4 Docker Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Docker Architecture                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│    User                                                          │
│        │                                                         │
│        │  Commands: docker run, docker ps, docker stop, etc.    │
│        ▼                                                         │
│   ┌─────────────────┐                                           │
│   │   Docker CLI    │  ◄── Command line interface               │
│   └────────┬────────┘                                           │
│            │                                                     │
│            │  Communicates via Unix socket                       │
│            │  (/var/run/docker.sock)                            │
│            ▼                                                     │
│   ┌─────────────────┐                                           │
│   │  Docker Daemon  │  ◄── Service that does all the work      │
│   │    (dockerd)    │                                           │
│   └────────┬────────┘                                           │
│            │                                                     │
│       ┌────┴────┬───────────────┬─────────────┐                 │
│       ▼         ▼               ▼             ▼                 │
│   ┌───────┐ ┌───────┐    ┌───────────┐ ┌───────────┐           │
│   │Images │ │Contai-│    │ Networks  │ │  Volumes  │           │
│   │       │ │ners   │    │           │ │           │           │
│   └───────┘ └───────┘    └───────────┘ └───────────┘           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 7.5 Essential Docker Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `docker ps` | List running containers | `docker ps` |
| `docker ps -a` | List all containers | `docker ps -a` |
| `docker images` | List downloaded images | `docker images` |
| `docker run` | Create and start container | `docker run -d nginx` |
| `docker stop` | Stop a container | `docker stop portainer` |
| `docker start` | Start a stopped container | `docker start portainer` |
| `docker logs` | View logs | `docker logs portainer` |
| `docker exec` | Execute command in container | `docker exec -it portainer sh` |

### 7.6 Checklist

- [ ] `docker --version` shows version 28.x or higher
- [ ] `docker-compose --version` shows version 1.29.x
- [ ] `docker run hello-world` succeeds **without sudo**
- [ ] `docker ps` runs without permission errors
- [ ] Docker service is running (`sudo service docker status`)

---

## 8. Step 4: Deploy Portainer CE

### 8.1 What is Portainer?

**Portainer Community Edition** is a web management interface that allows you to easily manage Docker environments.

#### Main Features:
- 🖥️ **Visual dashboard** - See all containers, images, networks
- 📊 **Monitoring** - Real-time CPU, memory, network statistics
- 📝 **Logs** - Easy viewing of container logs
- 🖱️ **Console** - Direct terminal access to containers
- 🔧 **Configuration** - Modify container settings through UI
- 📦 **Stacks** - Deploy multi-container applications with docker-compose

### 8.2 Why Portainer for Laboratory?

| Benefit | Explanation |
|---------|-------------|
| **Visual feedback** | See container states without commands |
| **Easy debugging** | Quick access to logs and console |
| **Network understanding** | Visual representation of communication |
| **Learning curve** | Less intimidating than CLI |

### 8.3 Installation Steps

#### Step 1: Ensure Docker is Running

```bash
sudo service docker start
docker ps
```

#### Step 2: Create Persistent Volume

Docker volumes persist data beyond container lifecycle:

```bash
docker volume create portainer_data
```

**What this does:** Creates a volume named `portainer_data` that will store:
- Portainer configuration
- User accounts
- Settings and preferences

#### Step 3: Deploy Portainer Container

```bash
docker run -d \
  -p 9000:9000 \
  --name portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest
```

**Detailed explanation of each parameter:**

| Flag | Value | Purpose |
|------|-------|---------|
| `-d` | - | Run in detached mode (background) |
| `-p` | `9000:9000` | Map container port 9000 to Windows port 9000 |
| `--name` | `portainer` | Name the container for easy reference |
| `--restart` | `always` | Automatically restart container if it stops |
| `-v` | `/var/run/docker.sock:...` | Give Portainer access to Docker daemon |
| `-v` | `portainer_data:/data` | Persist data between restarts |
| image | `portainer/portainer-ce:latest` | Use latest Portainer CE version |

#### Step 4: Verify Deployment

```bash
docker ps
```

**Expected output:**
```
CONTAINER ID   IMAGE                           COMMAND        CREATED          STATUS          PORTS                                        NAMES
44b61d00ab18   portainer/portainer-ce:latest   "/portainer"   10 seconds ago   Up 9 seconds    8000/tcp, 9443/tcp, 0.0.0.0:9000->9000/tcp   portainer
```

### 8.4 Initial Portainer Configuration

> ⏱️ **IMPORTANT:** You must complete initial configuration within **5 minutes** of deployment! After that, Portainer locks for security reasons.

#### Step 1: Access Portainer

Open your Windows browser (Chrome, Firefox, Edge) and navigate to:

```
http://localhost:9000
```

#### Step 2: Create Administrator Account

On the initial setup screen, fill in:

| Field | Value |
|-------|-------|
| **Username** | `stud` |
| **Password** | `studstudstud` |
| **Confirm password** | `studstudstud` |

Click **"Create user"**

#### Step 3: Connect to Local Docker

On the "Environment Wizard" screen:
1. You'll see the **"Get Started"** option - click it
2. Portainer will automatically detect local Docker

#### Step 4: Explore the Dashboard

After connection, you'll see the main dashboard with:
- Number of containers (running/stopped)
- Number of images
- Number of volumes
- Number of networks

### 8.5 What To Do If You Missed the 5-Minute Window

If you see "Portainer instance timed out for security purposes":

```bash
# Delete Portainer and data volume
docker stop portainer
docker rm portainer
docker volume rm portainer_data

# Recreate volume and container
docker volume create portainer_data
docker run -d \
  -p 9000:9000 \
  --name portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest
```

Then immediately access http://localhost:9000 and configure.

### 8.6 Checklist

- [ ] `docker ps` shows portainer container in "Up" state
- [ ] http://localhost:9000 loads in browser
- [ ] You can log in with stud/studstudstud
- [ ] Dashboard shows "local" Docker environment
- [ ] You see at least 1 container (portainer itself)

---

## 9. Step 5: Install Wireshark

### 9.1 What is Wireshark?

**Wireshark** is the world's foremost and most widely used network protocol analyser. Created in 1998 (as Ethereal), it's the standard tool for:

- 🔍 **Capturing** network traffic in real-time
- 📊 **Inspecting** packets at all OSI layers
- 🎯 **Filtering** traffic by hundreds of criteria
- 🔧 **Troubleshooting** network issues
- 📈 **Analysing** network performance
- 🎓 **Learning** network protocols

### 9.2 Why Wireshark on Windows (Not in WSL)?

| Reason | Explanation |
|--------|-------------|
| **Native GUI** | Optimal graphical performance on Windows |
| **Interface Access** | Sees all Windows network adapters |
| **vEthernet (WSL)** | Can capture all WSL/Docker traffic |
| **Integration** | Easy file saving, screenshots |
| **Stability** | More stable than X11 forwarding from WSL |

### 9.3 Installation Steps

#### Step 1: Download Wireshark

1. Open your browser
2. Navigate to: https://www.wireshark.org/download.html
3. Click **"Windows x64 Installer"** (or Windows Arm64 for ARM)
4. Save the installer file (approximately 80 MB)

#### Step 2: Run the Installer

1. Double-click the downloaded `.exe` file
2. Click **"Yes"** at User Account Control prompt
3. On the welcome screen, click **"Next"**
4. Accept the licence (GPL), click **"Noted"**
5. Select components (leave defaults), click **"Next"**

#### Step 3: Install Npcap

> ⚠️ **CRITICAL:** Npcap is **absolutely required** for packet capture!

During installation, you'll be prompted to install Npcap:

1. Click **"Install"** when Npcap prompt appears
2. In Npcap installer, **ensure** these options are checked:
   - ✅ **Install Npcap in WinPcap API-compatible Mode**
   - ✅ **Support raw 802.11 traffic (and target monitor mode)**
3. Click **"Install"** in Npcap installer
4. Wait for completion
5. Click **"Finish"** in Npcap installer
6. Continue with Wireshark installation

#### Step 4: Complete Installation

1. Choose whether you want shortcuts (recommended: Yes)
2. Click **"Install"**
3. Wait for completion
4. Click **"Finish"**

### 9.4 Capture Interface Selection

When you open Wireshark, you'll see a list of interfaces. For Docker/WSL traffic:

| Interface | Description | When to Use |
|-----------|-------------|-------------|
| **vEthernet (WSL)** | WSL2 virtual adapter | ✅ Docker container traffic |
| **vEthernet (WSL) (Hyper-V)** | Variant with firewall | ✅ Alternative |
| **Ethernet** | Physical network card | External real traffic |
| **Wi-Fi** | Wireless adapter | Wireless traffic |
| **Loopback Adapter** | Localhost interface | Localhost traffic only |

> 💡 **Simple rule:** For Docker laboratories, always use **vEthernet (WSL)**.

### 9.5 First Test Capture

1. **Open Wireshark** from Start Menu
2. **Double-click** on "vEthernet (WSL)"
3. **Capture starts** (you'll see packets appearing)
4. **In Ubuntu**, run:
   ```bash
   docker run --rm alpine ping -c 5 8.8.8.8
   ```
5. **In Wireshark**, apply filter: `icmp`
6. **Stop capture** (red Stop button)
7. **Verify** you see ICMP packets

### 9.6 Checklist

- [ ] Wireshark starts from Start Menu without errors
- [ ] Interface list is visible
- [ ] "vEthernet (WSL)" interface is present
- [ ] You can start a capture on vEthernet (WSL)
- [ ] You see packets when generating traffic from Docker

---

## 10. Step 6: Python Packages

### 10.1 Why Python for Networking?

Python is the preferred language for network automation and analysis due to:

- 📚 **Rich libraries** for networking
- 🚀 **Easy to learn** and read
- 🔧 **Ideal for scripting** and automation
- 📊 **Data processing** - pandas, matplotlib
- 🔬 **Packet analysis** - scapy, dpkt

### 10.2 Required Packages

| Package | Purpose | Laboratory Use |
|---------|---------|----------------|
| `docker` | Programmatic container management | Automate container start/stop |
| `scapy` | Packet creation and manipulation | Build custom packets, sniffing |
| `dpkt` | Fast PCAP parsing | Analyse capture files |
| `requests` | HTTP client | API testing, web scraping |
| `pyyaml` | YAML parsing | Read docker-compose files |

### 10.3 Installation on Windows

#### Step 1: Verify Python

Open PowerShell:

```powershell
python --version
```

**Expected output:** `Python 3.11.x` or newer

If not installed, download from: https://www.python.org/downloads/

> ⚠️ **During installation**, check "Add Python to PATH"!

#### Step 2: Install Packages

```powershell
pip install docker scapy dpkt requests pyyaml
```

#### Step 3: Verify Installation

```powershell
python -c "import docker; print(docker.__version__)"
python -c "import scapy; print(scapy.__version__)"
python -c "import dpkt; print(dpkt.__version__)"
```

### 10.4 Installation in Ubuntu WSL (Optional)

If you prefer running Python scripts from Ubuntu:

```bash
# In Ubuntu terminal
sudo apt install -y python3-pip
pip3 install docker scapy dpkt requests pyyaml
```

### 10.5 Checklist

- [ ] `python --version` shows Python 3.11+
- [ ] `pip show docker` shows package info
- [ ] `pip show scapy` shows package info
- [ ] `pip show dpkt` shows package info

---

## 11. Step 7: Configure Auto-start (Optional)

### 11.1 The Problem

In WSL2, services don't start automatically at boot. This means after every Windows restart, you need to manually run:

```bash
sudo service docker start
```

### 11.2 The Solution: Docker Auto-start

#### Method 1: .bashrc Script (Recommended)

Add to your `~/.bashrc` file:

```bash
# Start Docker automatically when terminal opens
if service docker status 2>&1 | grep -q "is not running"; then
    echo "Starting Docker..."
    sudo service docker start
fi
```

To edit:
```bash
nano ~/.bashrc
# Add the lines above at the end of file
# Ctrl+O to save, Ctrl+X to exit
```

#### Method 2: sudoers Configuration (For No Password)

To avoid entering password:

```bash
sudo visudo
```

Add at the end of the file:
```
stud ALL=(ALL) NOPASSWD: /usr/sbin/service docker start
```

### 11.3 Verification

1. Close all Ubuntu terminals
2. Stop WSL: `wsl --shutdown` in PowerShell
3. Open Ubuntu again
4. Verify: `docker ps` - should work immediately

### 11.4 Checklist

- [ ] Docker starts automatically when you open Ubuntu
- [ ] No password prompt (if sudoers configured)
- [ ] `docker ps` works immediately after opening Ubuntu

---

## 12. Final Verification

### 12.1 Complete System Test

Run these checks to confirm everything works:

#### Test 1: Verify WSL and Ubuntu

```powershell
# In PowerShell
wsl --status
wsl -l -v
```

**Expected:** Ubuntu-22.04 with VERSION 2, marked as default.

#### Test 2: Verify Docker

```bash
# In Ubuntu
docker --version
docker-compose --version
docker ps
```

**Expected:** Versions displayed, Portainer in container list.

#### Test 3: Verify Portainer

1. Open http://localhost:9000 in browser
2. Log in with stud/studstudstud
3. Verify you see the dashboard

#### Test 4: Wireshark Capture

1. Open Wireshark
2. Select vEthernet (WSL)
3. Start capture
4. In Ubuntu, run:
   ```bash
   docker run --rm alpine ping -c 5 8.8.8.8
   ```
5. In Wireshark, apply filter: `icmp`
6. Verify ICMP packets visible

#### Test 5: Python

```powershell
python -c "import docker; c = docker.from_env(); print(f'Containers: {len(c.containers.list())}')"
```

**Expected:** Displays container count.

### 12.2 Complete Verification Script

Save this as `verify_environment.sh` and run in Ubuntu:

```bash
#!/bin/bash
echo "╔════════════════════════════════════════════════════════════╗"
echo "║       NETWORKING LABORATORY ENVIRONMENT CHECK              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo "=== 1. Ubuntu Version ==="
lsb_release -d
echo ""

echo "=== 2. Docker Version ==="
docker --version
docker-compose --version
echo ""

echo "=== 3. Docker Service Status ==="
sudo service docker status | head -3
echo ""

echo "=== 4. Running Containers ==="
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""

echo "=== 5. Portainer Status ==="
if docker ps | grep -q portainer; then
    echo "✅ Portainer is running"
    echo "   URL: http://localhost:9000"
else
    echo "❌ Portainer is NOT running!"
fi
echo ""

echo "=== 6. Docker Networks ==="
docker network ls
echo ""

echo "=== 7. Docker Volumes ==="
docker volume ls
echo ""

echo "════════════════════════════════════════════════════════════"
echo "✅ Verification complete!"
echo "════════════════════════════════════════════════════════════"
```

### 12.3 Component Summary Table

| Component | Verification Command | Expected Output |
|-----------|---------------------|-----------------|
| WSL2 | `wsl --status` | Default Version: 2 |
| Ubuntu | `lsb_release -a` | Ubuntu 22.04 LTS |
| Docker | `docker --version` | Docker version 28.x |
| Docker Compose | `docker-compose --version` | version 1.29.x |
| Portainer | http://localhost:9000 | Login page |
| Wireshark | Launch application | Interface list |
| Python docker | `pip show docker` | Version: 7.x |

---

## 13. Complete Portainer Usage Guide

### 13.1 Access and Authentication

1. **URL:** http://localhost:9000
2. **Username:** stud
3. **Password:** studstudstud

### 13.2 Interface Navigation

```
┌─────────────────────────────────────────────────────────────────┐
│  PORTAINER                                    [🔔] [stud ▼]     │
├──────────────────┬──────────────────────────────────────────────┤
│                  │                                              │
│  🏠 Home         │  Environment: local                         │
│                  │  ┌────────────────────────────────────────┐  │
│  📦 Containers   │  │                                        │  │
│  🖼️ Images       │  │  Containers: 1    Running: 1           │  │
│  🌐 Networks     │  │  Images: 2        Volumes: 1           │  │
│  💾 Volumes      │  │  Networks: 3      Stacks: 0            │  │
│  📚 Stacks       │  │                                        │  │
│                  │  └────────────────────────────────────────┘  │
│  ⚙️ Settings     │                                              │
│                  │                                              │
└──────────────────┴──────────────────────────────────────────────┘
```

### 13.3 Container Management

#### Viewing Containers
1. Click **Containers** in left menu
2. See list of all containers
3. Columns: Name, State, Image, Created, IP Address, Ports

#### Container Actions

| Action | How | Purpose |
|--------|-----|---------|
| **Start** | Check container → Click "Start" | Start stopped container |
| **Stop** | Check container → Click "Stop" | Stop running container |
| **Restart** | Check container → Click "Restart" | Restart container |
| **Remove** | Check container → Click "Remove" | Delete container |
| **Logs** | Click name → "Logs" tab | View output/errors |
| **Console** | Click name → "Console" tab | Terminal in container |
| **Inspect** | Click name → "Inspect" tab | JSON configuration |
| **Stats** | Click name → "Stats" tab | CPU/Memory/Network |

### 13.4 Viewing Logs

1. Click on container name
2. Select **Logs** tab
3. Available options:
   - **Auto-refresh**: Automatic update
   - **Timestamps**: Show timestamp
   - **Lines**: Number of lines displayed
   - **Download**: Download logs

### 13.5 Container Console Access

1. Click on container name
2. Select **Console** tab
3. Click **Connect**
4. Choose shell: `/bin/sh` or `/bin/bash`
5. Now you have terminal in container!

### 13.6 Modifying Networks and IP Addresses

#### Viewing Networks
1. Click **Networks** in menu
2. See all Docker networks
3. Click a network for details

#### Changing Container IP Address

To change a container's IP address:

1. **Stop the container** to be modified
2. **Edit `docker-compose.yml`**:
   ```yaml
   services:
     lab:
       networks:
         week7_network:
           ipv4_address: 172.20.7.50  # New IP address
   
   networks:
     week7_network:
       ipam:
         config:
           - subnet: 172.20.7.0/24
             gateway: 172.20.7.1
   ```
3. **Recreate containers**:
   ```bash
   docker-compose down
   docker-compose up -d
   ```
4. **Verify in Portainer**: Networks → See new configuration

### 13.7 Modifying Ports

1. **Stop the container**
2. **Edit `docker-compose.yml`**:
   ```yaml
   services:
     lab:
       ports:
         - "9095:9090"  # Host:Container
         - "9096:9091"
   ```
3. **Recreate**:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

> ⚠️ **IMPORTANT:** Never use port 9000 - it's reserved for Portainer!

---

## 14. Complete Wireshark Usage Guide

### 14.1 Starting a Capture

1. **Open Wireshark** from Start Menu
2. **Identify the interface** - for Docker, look for "vEthernet (WSL)"
3. **Double-click** on interface to start capture
4. **Alternative**: Select interface and click 🦈 (blue shark fin)

### 14.2 Correct Interface Selection

| You See | Choose | When |
|---------|--------|------|
| vEthernet (WSL) | ✅ YES | Docker/WSL traffic |
| vEthernet (WSL) (Hyper-V) | ✅ YES | Alternative |
| Ethernet | ⚠️ Sometimes | External traffic |
| Wi-Fi | ⚠️ Sometimes | Wireless traffic |
| Loopback | ❌ Rarely | Localhost only |

### 14.3 Display Filters

Filters are entered in the top bar. When valid, the bar turns green.

#### Basic Filters

| Filter | Description |
|--------|-------------|
| `tcp` | All TCP traffic |
| `udp` | All UDP traffic |
| `icmp` | Ping packets (ICMP) |
| `http` | HTTP traffic |
| `dns` | DNS queries |
| `arp` | ARP packets |

#### Address Filters

| Filter | Description |
|--------|-------------|
| `ip.addr == 172.20.7.2` | Traffic to/from IP |
| `ip.src == 172.20.7.2` | Only from this IP |
| `ip.dst == 8.8.8.8` | Only to this IP |
| `eth.addr == aa:bb:cc:dd:ee:ff` | By MAC address |

#### Port Filters

| Filter | Description |
|--------|-------------|
| `tcp.port == 80` | TCP on port 80 |
| `udp.port == 53` | UDP on port 53 (DNS) |
| `tcp.dstport == 443` | TCP to port 443 |
| `tcp.srcport == 9090` | TCP from port 9090 |

#### Specific TCP Filters

| Filter | Description |
|--------|-------------|
| `tcp.flags.syn == 1` | SYN packets |
| `tcp.flags.syn == 1 && tcp.flags.ack == 0` | Initial SYN only |
| `tcp.flags.fin == 1` | FIN packets |
| `tcp.flags.rst == 1` | RST (reset) packets |
| `tcp.analysis.retransmission` | Retransmissions |
| `tcp.stream eq 0` | First TCP conversation |

#### Combining Filters

| Operator | Example |
|----------|---------|
| AND | `tcp.port == 80 && ip.addr == 172.20.7.2` |
| OR | `tcp.port == 80 \|\| tcp.port == 443` |
| NOT | `!arp && !dns` |
| Parentheses | `(tcp.port == 80 \|\| tcp.port == 443) && ip.src == 172.20.7.2` |

### 14.4 Understanding Columns

| Column | Contents | Example |
|--------|----------|---------|
| **No.** | Packet number in capture | 1, 2, 3... |
| **Time** | Seconds from start | 0.000000, 0.000234 |
| **Source** | Source IP address | 172.20.7.2 |
| **Destination** | Destination IP address | 8.8.8.8 |
| **Protocol** | Detected protocol | TCP, UDP, HTTP, DNS |
| **Length** | Packet size (bytes) | 74, 1500 |
| **Info** | Specific details | 80 → 54321 [SYN] |

### 14.5 Colour Coding

| Colour | Meaning |
|--------|---------|
| **Light purple** | Normal TCP traffic |
| **Light blue** | UDP traffic |
| **Light green** | HTTP traffic |
| **Yellow** | Warnings (retransmissions) |
| **Red** | Errors (RST, problems) |
| **Grey** | Connection events (SYN, FIN) |
| **Black on red** | Severe errors |

### 14.6 Following a TCP Conversation

1. **Find a packet** from the desired conversation
2. **Right-click** on packet
3. Select **Follow → TCP Stream**
4. See complete conversation:
   - **Red**: Data sent by client
   - **Blue**: Data sent by server
5. **Dropdown**: Switch between ASCII/Hex/Raw
6. **Close**: Return to packet list

### 14.7 TCP Three-Way Handshake Analysis

The three-way handshake:

```
Client                              Server
  │                                   │
  │ ────── SYN (seq=100) ──────────► │  Step 1
  │                                   │
  │ ◄──── SYN-ACK (seq=300, ack=101) │  Step 2
  │                                   │
  │ ────── ACK (seq=101, ack=301) ──► │  Step 3
  │                                   │
  │         CONNECTION ESTABLISHED    │
```

**Filter to see handshakes:** `tcp.flags.syn == 1`

### 14.8 Saving and Exporting

#### Save Capture
1. **File → Save As**
2. Navigate to desired location
3. Format: `.pcapng` (default, recommended)

#### Export CSV for Python Analysis
1. **File → Export Packet Dissections → As CSV**
2. Select desired fields
3. Save as `.csv`

### 14.9 Useful Statistics

| Menu | Function |
|------|----------|
| Statistics → Capture File Properties | Capture information |
| Statistics → Protocol Hierarchy | Protocol distribution |
| Statistics → Conversations | Conversation list |
| Statistics → Endpoints | Endpoint list |
| Statistics → I/O Graphs | Traffic graphs over time |

---

## 15. Troubleshooting

### 15.1 WSL Issues

#### "WSL 2 requires an update to its kernel component"

```powershell
wsl --update
```

#### "Please enable the Virtual Machine Platform Windows feature"

```powershell
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```
Restart computer.

#### WSL won't start

```powershell
wsl --shutdown
wsl
```

#### Ubuntu doesn't appear in `wsl -l -v`

```powershell
wsl --install -d Ubuntu-22.04 --web-download
```

### 15.2 Docker Issues

#### "Cannot connect to the Docker daemon"

```bash
# Start Docker service
sudo service docker start

# Verify
ps aux | grep dockerd
```

#### "Permission denied connecting to Docker socket"

```bash
# Add user to group
sudo usermod -aG docker $USER

# Apply changes
newgrp docker
# Or logout/login
```

#### "docker: command not found" in PowerShell

Normal! Docker is in WSL, not Windows. Use:

```powershell
wsl docker ps
```

### 15.3 Portainer Issues

#### Cannot access http://localhost:9000

1. Check container is running:
   ```bash
   docker ps | grep portainer
   ```

2. If not running:
   ```bash
   docker start portainer
   ```

3. Check logs:
   ```bash
   docker logs portainer
   ```

#### "Portainer instance timed out"

```bash
docker stop portainer
docker rm portainer
docker volume rm portainer_data
docker volume create portainer_data
docker run -d -p 9000:9000 --name portainer --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data portainer/portainer-ce:latest
```

### 15.4 Wireshark Issues

#### No interfaces visible

- Ensure Npcap is installed
- Run Wireshark as Administrator
- Reinstall Npcap from https://npcap.com/

#### "vEthernet (WSL)" doesn't appear

- WSL must be running. In PowerShell: `wsl`
- Restart Wireshark

#### No traffic captured

- Check interface (vEthernet WSL)
- Generate active traffic
- Check display filter

---

## 16. Quick Reference Card

### Essential WSL Commands (PowerShell)

```powershell
wsl --status           # WSL status
wsl --shutdown         # Stop all instances
wsl                    # Open default distribution
wsl -l -v              # List distributions
wsl --set-default Ubuntu-22.04  # Set default
```

### Essential Docker Commands (Ubuntu)

```bash
# Service
sudo service docker start
sudo service docker status

# Containers
docker ps              # Running
docker ps -a           # All
docker start <n>       # Start
docker stop <n>        # Stop
docker logs <n>        # Logs
docker exec -it <n> sh # Shell in container

# Images and cleanup
docker images
docker image prune -f
docker system prune -f
```

### Important URLs

| Service | URL |
|---------|-----|
| **Portainer** | http://localhost:9000 |
| Docker Docs | https://docs.docker.com/ |
| Wireshark Docs | https://www.wireshark.org/docs/ |
| WSL Docs | https://learn.microsoft.com/windows/wsl/ |

### Credentials

```
┌─────────────────────────────────────┐
│  Ubuntu WSL: stud / stud           │
│  Portainer:  stud / studstudstud   │
└─────────────────────────────────────┘
```

### File Paths

| Windows | Ubuntu (WSL) |
|---------|--------------|
| D:\NETWORKING\WEEK7 | /mnt/d/NETWORKING/WEEK7 |
| C:\Users\stud | /mnt/c/Users/stud |

### Common Wireshark Filters

```
tcp                     # All TCP
udp                     # All UDP
icmp                    # Ping
tcp.port == 9090        # Specific port
ip.addr == 172.20.7.2   # Specific IP
tcp.flags.syn == 1      # Handshakes
```

---

## 🎉 Setup Complete!

Your laboratory environment is fully configured. You can now:

- ✅ Run isolated network experiments with Docker containers
- ✅ Capture and analyse traffic with Wireshark
- ✅ Manage containers through Portainer web interface
- ✅ Automate network tasks with Python
- ✅ Learn Linux and Docker at the same time

**Reminder:** Docker Desktop is **NOT** required and should **NOT** be installed!

**Next Steps:**
1. Explore Portainer interface
2. Try creating custom Docker networks
3. Practice Wireshark filtering
4. Run your first laboratory exercise

---

*Computer Networks Laboratory — ASE Bucharest, CSIE*  
*Documentation version: January 2026 v2.0*  
*Updated with Docker Desktop clarifications and extended Portainer/Wireshark guides*
