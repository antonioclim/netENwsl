# 🎯 Concept Analogies — Week 0
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> **CPA Method:** Concrete → Pictorial → Abstract  
> We understand new concepts more easily when we connect them to familiar things.

---

## Overview: Lab Architecture

### 🏠 Complete Analogy: The Apartment Building

Imagine a **modern apartment building** with centralised management:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          THE BUILDING (Windows 11)                          │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                    THE LINUX FLOOR (WSL2)                             │ │
│  │                                                                       │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │ │
│  │  │              MANAGEMENT COMPANY (Docker)                        │ │ │
│  │  │                                                                 │ │ │
│  │  │   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐          │ │ │
│  │  │   │  Flat 1 │  │  Flat 2 │  │  Flat 3 │  │Reception│          │ │ │
│  │  │   │ (nginx) │  │ (mysql) │  │ (redis) │  │(Portain)│          │ │ │
│  │  │   │  :80    │  │ :3306   │  │ :6379   │  │ :9000   │          │ │ │
│  │  │   └─────────┘  └─────────┘  └─────────┘  └─────────┘          │ │ │
│  │  │                                                                 │ │ │
│  │  └─────────────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                        │
│  │  Wireshark  │  │   Browser   │  │ PowerShell  │                        │
│  │  (Security  │  │  (Visit     │  │ (Intercom)  │                        │
│  │   camera)   │  │ reception)  │  │             │                        │
│  └─────────────┘  └─────────────┘  └─────────────┘                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

| Real Element | Building Analogy | Explanation |
|--------------|------------------|-------------|
| Windows 11 | The entire building | Main structure that houses everything |
| WSL2 | A dedicated floor | Separate space with its own rules (Linux) |
| Docker | Management company | Manages the flats (containers) |
| Container | Flat | Isolated unit with its own utilities |
| Portainer | Reception desk | Central point for information and control |
| Wireshark | Security camera | Monitors all traffic |
| Port mapping | Flat number | How you reach the desired flat |

---

## WSL2: The Linux Subsystem

### 🏠 Analogy: The Floor with Different Rules

In a building, imagine a floor that operates under completely different rules — it has its own adminilayerion and utilities but uses the building's infrastructure (electricity, water).

### 🖼️ Visual Representation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              WINDOWS 11                                     │
│                                                                             │
│    C:\Users\stud\Desktop\     ←── Windows filesystem                       │
│         │                                                                   │
│         │ (access via /mnt/c/)                                             │
│         ▼                                                                   │
│    ┌─────────────────────────────────────────────────────────────────────┐ │
│    │                           WSL2 (Ubuntu)                             │ │
│    │                                                                     │ │
│    │    /home/stud/          ←── Linux filesystem                       │ │
│    │    /mnt/c/Users/stud/   ←── Access to Windows                      │ │
│    │                                                                     │ │
│    │    Linux Kernel 5.15.x                                             │ │
│    │    Commands: ls, cd, grep, apt, docker                             │ │
│    │                                                                     │ │
│    └─────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│    Access from Windows:  \\wsl$\Ubuntu\home\stud\                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### ⚠️ Where the Analogy Breaks Down

- A real floor cannot run different programmes from the rest of the building
- Real floors don't have their own internal addressing system
- WSL2 is actually a lightweight virtual machine, not just a different floor

---

## Docker: Containers vs Images

### 🏠 Analogy: Flat Blueprint vs Actual Flat

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   DOCKER IMAGE                            DOCKER CONTAINERS                 │
│   (Flat blueprint)                        (Built flats)                     │
│                                                                             │
│   ┌─────────────────────┐                 ┌───────┐ ┌───────┐ ┌───────┐   │
│   │  ┌───┐ ┌───┐       │                 │ Flat  │ │ Flat  │ │ Flat  │   │
│   │  │ 🛋 │ │ 🛏 │       │    you build   │ 101   │ │ 102   │ │ 103   │   │
│   │  └───┘ └───┘       │ ──────────────► │ web1  │ │ web2  │ │ web3  │   │
│   │  Standard blueprint │   from plan    │       │ │       │ │       │   │
│   │  nginx:latest      │                 │ Own   │ │ Own   │ │ Own   │   │
│   │  (read-only)       │                 │tenant │ │tenant │ │tenant │   │
│   └─────────────────────┘                 └───────┘ └───────┘ └───────┘   │
│                                                                             │
│   • One blueprint                         • Multiple flats                 │
│   • Doesn't change                        • Each with own modifications    │
│   • Template                              • Real instances                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### ⚠️ Where the Analogy Breaks Down

- Real blueprints aren't "downloaded" from the internet
- Real flats don't start up in milliseconds
- You can't create 100 identical flats instantly
- Layers have no equivaslow in real construction

---

## Port Mapping: -p 8080:80

### 🏠 Analogy: Hotel Reception

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  OUTSIDE WORLD                            THE HOTEL (Docker Host)           │
│                                                                             │
│     👤 Visitor                            ┌───────────────────────────────┐ │
│        │                                  │         RECEPTION              │ │
│        │ "I want room 8080"               │                               │ │
│        ▼                                  │   8080 ──► Room 80 (nginx)    │ │
│   ┌─────────┐                             │   8081 ──► Room 80 (apache)   │ │
│   │  :8080  │────────────────────────────►│   9000 ──► Room 9000 (port.)  │ │
│   └─────────┘                             │                               │ │
│                                           │   "8080" is the public number │ │
│   Public address                          │   "80" is the actual room     │ │
│   localhost:8080                          │                               │ │
│                                           └───────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### ⚠️ Where the Analogy Breaks Down

- At a hotel, room 80 and 8080 would be different physical rooms
- A hotel can't have two guests in the same physical room
- Docker can map the same container port to multiple host ports

---

## Sockets: Network Communication

### 🏠 Analogy: The Landline Telephone

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   SOCKET OPERATION           TELEPHONE EQUIVALENT                          │
│                                                                             │
│   socket()          ──────►    🛒 Buy a new telephone                      │
│                                                                             │
│   bind(port)        ──────►    📞 Get assigned a phone number              │
│                                   (e.g., 0722-123-456)                     │
│                                                                             │
│   listen()          ──────►    🔌 Plug the phone in and wait for           │
│                                   calls                                    │
│                                                                             │
│   accept()          ──────►    📱 Pick up the receiver when it rings       │
│                                                                             │
│   connect()         ──────►    📲 Dial someone's number                    │
│                                                                             │
│   send() / recv()   ──────►    🗣️ Talk / Listen                            │
│                                                                             │
│   close()           ──────►    📵 Hang up the phone                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### ⚠️ Where the Analogy Breaks Down

- Telephones don't have "buffer size"
- You can't send raw bytes through a telephone
- TCP guarantees delivery, telephones don't
- A telephone can't have 65535 different numbers (ports)

---

## Bytes vs Strings in Python

### 🏠 Analogy: Letter vs Sealed Envelope

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   STRING (str)                            BYTES (bytes)                     │
│   The letter you read                     Sealed envelope for post          │
│                                                                             │
│   ┌─────────────────────────┐            ┌─────────────────────────┐       │
│   │                         │            │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │       │
│   │   "Hello, world!"       │            │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │       │
│   │                         │            │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │       │
│   │   You read directly     │            │   b'Hello, world!'      │       │
│   │   Visible characters    │            │   Bytes for transport   │       │
│   │                         │            │                         │       │
│   └─────────────────────────┘            └─────────────────────────┘       │
│                                                                             │
│         │                                         ▲                         │
│         │ .encode('utf-8')                        │                         │
│         │ (put in envelope)                       │                         │
│         ▼                                         │                         │
│         ─────────────────────────────────────────►│                         │
│                                                   │ .decode('utf-8')        │
│         ◄─────────────────────────────────────────                          │
│                                                   (open the envelope)       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### ⚠️ Where the Analogy Breaks Down

- Real envelopes don't have "encoding"
- You can read a letter without decoding it
- bytes can contain anything (images, executables), not just text

---

## Summary: Quick Reference Table

| Concept | Analogy | Analogy Limitation |
|---------|---------|-------------------|
| Windows 11 | Apartment building | Building doesn't run software |
| WSL2 | Floor with Linux rules | It's actually a VM, not a floor |
| Docker | Management company | Company doesn't create flats from plans |
| Container | Flat | Flats don't start in ms |
| Image | Flat blueprint | Blueprints don't have layers |
| Port mapping | Hotel reception | Hotel doesn't redirect |
| Socket | Landline phone | Phone doesn't have buffer |
| String→Bytes | Letter→Envelope | Envelope doesn't have encoding |
| Portainer | Reception with monitor | Reception doesn't control building |
| Wireshark | Security camera | Camera doesn't decode packets |

---

*Concept Analogies — Week 0: Lab Environment Setup*  
*Computer Networks — ASE Bucharest, CSIE*  
*Version: January 2025*
