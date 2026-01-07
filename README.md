# 🖧 Rețele de Calculatoare — Kit-uri Complete de Laborator (Ediția WSL)

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-28.2.2+-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![WSL2](https://img.shields.io/badge/WSL2-Ubuntu_22.04_LTS-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com)
[![Wireshark](https://img.shields.io/badge/Wireshark-4.4.x-1679A7?style=for-the-badge&logo=wireshark&logoColor=white)](https://wireshark.org)
[![Portainer](https://img.shields.io/badge/Portainer-2.33.6_LTS-13BEF9?style=for-the-badge&logo=portainer&logoColor=white)](https://portainer.io)
[![Licență](https://img.shields.io/badge/Licență-MIT-yellow?style=for-the-badge)](LICENSE)

> **by Revolvix**

**Disciplină:** Rețele de Calculatoare (25.0205IF3.2-0003)  
**Program de studiu:** Informatică Economică, Anul III, Semestrul 2  
**Instituție:** Academia de Studii Economice din București (ASE), Facultatea de Cibernetică, Statistică și Informatică Economică (CSIE)  
**An universitar:** 2024–2025

---

## 📋 Cuprins General

### Partea I — Introducere și Prezentare
- [1. Prezentare generală](#1-prezentare-generală)
- [2. Filosofia pedagogică](#2-filosofia-pedagogică)
- [3. Arhitectura sistemului](#3-arhitectura-sistemului)
- [4. Structura repository-ului](#4-structura-repository-ului)

### Partea II — Configurarea Mediului de Lucru
- [5. Cerințe de sistem](#5-cerințe-de-sistem)
- [6. Credențiale standard](#6-credențiale-standard)
- [7. Instalare pas cu pas](#7-instalare-pas-cu-pas)
- [8. Verificarea instalării](#8-verificarea-instalării)

### Partea III — Curricula Săptămânală Detaliată
- [9. Ghid rapid de pornire a laboratoarelor](#9-ghid-rapid-de-pornire-a-laboratoarelor)
- [10. Clonarea individuală a fiecărei săptămâni](#10-clonarea-individuală-a-fiecărei-săptămâni)
- [11. Săptămâna 1: Fundamente ale rețelelor](#11-săptămâna-1-fundamente-ale-rețelelor)
- [12. Săptămâna 2: Modele arhitecturale și programare socket](#12-săptămâna-2-modele-arhitecturale-și-programare-socket)
- [13. Săptămâna 3: Paradigme de programare în rețea](#13-săptămâna-3-paradigme-de-programare-în-rețea)
- [14. Săptămâna 4: Nivelurile fizic și legătură de date](#14-săptămâna-4-nivelurile-fizic-și-legătură-de-date)
- [15. Săptămâna 5: Nivelul rețea și adresare IP](#15-săptămâna-5-nivelul-rețea-și-adresare-ip)
- [16. Săptămâna 6: NAT/PAT, protocoale suport și SDN](#16-săptămâna-6-natpat-protocoale-suport-și-sdn)
- [17. Săptămâna 7: Interceptare pachete, filtrare și securitate](#17-săptămâna-7-interceptare-pachete-filtrare-și-securitate)
- [18. Săptămâna 8: Nivelul transport, HTTP și proxy invers](#18-săptămâna-8-nivelul-transport-http-și-proxy-invers)
- [19. Săptămâna 9: Nivelurile sesiune și prezentare](#19-săptămâna-9-nivelurile-sesiune-și-prezentare)
- [20. Săptămâna 10: Protocoale de nivel aplicație](#20-săptămâna-10-protocoale-de-nivel-aplicație)
- [21. Săptămâna 11: FTP, DNS, SSH și echilibrarea încărcării](#21-săptămâna-11-ftp-dns-ssh-și-echilibrarea-încărcării)
- [22. Săptămâna 12: Protocoale email și RPC](#22-săptămâna-12-protocoale-email-și-rpc)
- [23. Săptămâna 13: IoT și securitatea rețelelor](#23-săptămâna-13-iot-și-securitatea-rețelelor)
- [24. Săptămâna 14: Recapitulare integrată și evaluare](#24-săptămâna-14-recapitulare-integrată-și-evaluare)

### Partea IV — Referințe și Suport
- [25. Structura standard a kit-urilor](#25-structura-standard-a-kit-urilor)
- [26. Planul de adresare IP](#26-planul-de-adresare-ip)
- [27. Tehnologii și instrumente utilizate](#27-tehnologii-și-instrumente-utilizate)
- [28. Ghid complet de depanare](#28-ghid-complet-de-depanare)
- [29. Comenzi esențiale — Fișă de referință rapidă](#29-comenzi-esențiale--fișă-de-referință-rapidă)
- [30. Licență](#30-licență)

---

# PARTEA I — INTRODUCERE ȘI PREZENTARE

---

## 1. Prezentare generală

Acest repository conține **kit-uri complete de laborator** pentru disciplina **Rețele de Calculatoare**, acoperind exhaustiv toate cele **14 săptămâni** ale semestrului universitar. Materialele sunt proiectate și optimizate specific pentru implementare pe sisteme **Windows 10/11** utilizând **WSL2** (Windows Subsystem for Linux) cu containerizare **Docker**, oferind studenților și profesorilor un mediu de laborator portabil, reproductibil, izolat și profesional.

### 1.1 Ce oferă acest repository?

Fiecare kit săptămânal constituie o **unitate educațională autonomă și completă**, cuprinzând:

| Componentă | Descriere |
|------------|-----------|
| **📚 Documentație structurată** | Fundamentele teoretice articulate clar, obiective de învățare explicite, ghiduri pas cu pas |
| **🐍 Exerciții Python** | Progresie graduală de la implementări ghidate la rezolvare independentă de probleme complexe |
| **🐳 Medii Docker Compose** | Topologii de rețea multi-container pre-configurate, gata de utilizare |
| **🧪 Framework-uri de testare** | Validare automată a completării exercițiilor și integrității mediului |
| **📡 Facilități de captură** | Scripturi pentru captură de pachete și analiză forensică a protocoalelor |
| **📋 Fișe de referință** | Comenzi CLI esențiale consolidate pentru acces rapid |
| **📝 Teme pentru acasă** | Exerciții suplimentare cu soluții de referință pentru studiu individual |

### 1.2 Metodologia de învățare

Abordarea pedagogică pune accent pe **învățarea prin observație și experimentare directă**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     CICLUL DE ÎNVĂȚARE EXPERIENȚIALĂ                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    ┌──────────────┐      ┌──────────────┐      ┌──────────────┐            │
│    │  CONSTRUIEȘTE │ ──▶ │   GENEREAZĂ   │ ──▶ │   CAPTEAZĂ   │            │
│    │   servicii    │      │    trafic     │      │   pachete    │            │
│    │   de rețea    │      │    de rețea   │      │   PCAP       │            │
│    └──────────────┘      └──────────────┘      └──────┬───────┘            │
│           ▲                                           │                     │
│           │                                           ▼                     │
│    ┌──────┴───────┐                          ┌──────────────┐              │
│    │   APLICĂ     │ ◀────────────────────── │   ANALIZEAZĂ  │              │
│    │  cunoștințe  │                          │  protocoale   │              │
│    │   noi        │                          │  și comportam.│              │
│    └──────────────┘                          └──────────────┘              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

Această metodologie face punte între **modelele teoretice** și **realitatea operațională**, pregătind studenții pentru cariere în:

- 🌐 Ingineria rețelelor de calculatoare
- 🔒 Analiza și auditul de securitate cibernetică
- 🏗️ Dezvoltarea sistemelor distribuite
- ☁️ Administrarea infrastructurilor cloud
- 🔧 DevOps și Site Reliability Engineering

### 1.3 Pentru cine este acest repository?

| Public țintă | Beneficii |
|--------------|-----------|
| **Studenți** | Materiale complete pentru învățare independentă, exerciții practice, soluții de referință |
| **Profesori/Asistenți** | Kit-uri gata de utilizare pentru laborator, structură consistentă, framework de evaluare |
| **Autodidacți** | Curriculum complet de networking, de la fundamentals la advanced topics |
| **Profesioniști** | Refresh de concepte, sandbox pentru experimentare, referință tehnică |

---

## 2. Filosofia pedagogică

### 2.1 Modelul de progresie în învățare

Cursul urmează o **explorare arhitecturală de jos în sus** aliniată cu modelele de referință OSI/TCP-IP, începând cu concepte fundamentale și instrumente de diagnoză înainte de a urca prin stiva de protocoale:

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    TRAIECTORIA DE ÎNVĂȚARE — SEMESTRUL 2                       ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  Săpt. 14 ─┬─ INTEGRARE    ════════════════════════════════════════════════  ║
║            │                                                                  ║
║  Săpt. 13 ─┤                ┌───────────────────────────────────────────┐    ║
║  Săpt. 12 ─┤  NIVELUL       │  • IoT & MQTT (publish/subscribe)        │    ║
║  Săpt. 11 ─┤  APLICAȚIE     │  • Email (SMTP, POP3, IMAP)              │    ║
║  Săpt. 10 ─┘                │  • RPC (JSON-RPC, XML-RPC, gRPC)         │    ║
║                             │  • HTTP/HTTPS, REST APIs, DNS, SSH       │    ║
║                             │  • FTP, Load Balancing                   │    ║
║                             └───────────────────────────────────────────┘    ║
║                                                                               ║
║  Săpt. 9  ─┬─ SESIUNE &     ┌───────────────────────────────────────────┐    ║
║            │  PREZENTARE    │  • FTP Active/Passive modes               │    ║
║            │                │  • Serializare binară                     │    ║
║            │                │  • Gestionare stare sesiune               │    ║
║            └────────────────└───────────────────────────────────────────┘    ║
║                                                                               ║
║  Săpt. 8  ─── TRANSPORT     ┌───────────────────────────────────────────┐    ║
║                             │  • TCP 3-way handshake                    │    ║
║                             │  • HTTP/1.1 server implementation         │    ║
║                             │  • Nginx reverse proxy & load balancing   │    ║
║                             └───────────────────────────────────────────┘    ║
║                                                                               ║
║  Săpt. 7  ─── SECURITATE    ┌───────────────────────────────────────────┐    ║
║              & FILTRARE     │  • iptables firewall rules                │    ║
║                             │  • Packet filtering (DROP/REJECT)         │    ║
║                             │  • Port scanning & reconnaissance         │    ║
║                             │  • tcpdump, tshark, Wireshark             │    ║
║                             └───────────────────────────────────────────┘    ║
║                                                                               ║
║  Săpt. 5  ─┬─ NIVELUL       ┌───────────────────────────────────────────┐    ║
║  Săpt. 6  ─┘  REȚEA         │  • Adresare IP, CIDR, VLSM                │    ║
║                             │  • NAT/PAT, SNAT, DNAT                    │    ║
║                             │  • ARP, DHCP, ICMP, NDP                   │    ║
║                             │  • Software-Defined Networking (SDN)      │    ║
║                             └───────────────────────────────────────────┘    ║
║                                                                               ║
║  Săpt. 4  ─── LEGĂTURĂ      ┌───────────────────────────────────────────┐    ║
║              DE DATE        │  • Ethernet frames, MAC addressing        │    ║
║                             │  • CRC32 error detection                  │    ║
║                             │  • Binary protocol design                 │    ║
║                             │  • Python struct pack/unpack              │    ║
║                             └───────────────────────────────────────────┘    ║
║                                                                               ║
║  Săpt. 1  ─┬─ FUNDAMENTE    ┌───────────────────────────────────────────┐    ║
║  Săpt. 2  ─┤                │  • CLI diagnostic tools (ip, ss, ping)    │    ║
║  Săpt. 3  ─┘                │  • Socket programming (TCP/UDP)           │    ║
║                             │  • Concurrent servers (threading)         │    ║
║                             │  • Packet capture & analysis              │    ║
║                             └───────────────────────────────────────────┘    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### 2.2 Cadrul de dezvoltare a competențelor (Taxonomia Bloom)

Fiecare sesiune de laborator vizează niveluri cognitive specifice, progresând de la simplu la complex:

| Nivel cognitiv | Verb cheie | Activități tipice | Metode de evaluare |
|----------------|------------|-------------------|-------------------|
| **1. A REȚINE** | Reamintește, Identifică, Listează | Sintaxa comenzilor, câmpurile protocoalelor, definițiile conceptelor | Completarea fișelor de referință, quiz-uri rapide |
| **2. A ÎNȚELEGE** | Explică, Descrie, Compară | Comportamentul protocoalelor, pattern-uri de trafic, fluxuri de date | Analiză scrisă, explicații verbale, diagrame |
| **3. A APLICA** | Demonstrează, Implementează, Utilizează | Folosirea instrumentelor în scenarii noi, adaptarea scripturilor | Implementări funcționale, log-uri, rapoarte |
| **4. A ANALIZA** | Examinează, Diferențiază, Investighează | Capturile de pachete, workflow-uri de depanare, root cause analysis | Adnotări PCAP, rapoarte cauză principală |
| **5. A EVALUA** | Evaluează, Critică, Justifică | Postura de securitate, trade-off-uri de design, alegeri arhitecturale | Recomandări tehnice, audituri, peer review |
| **6. A CREA** | Proiectează, Construiește, Dezvoltă | Implementări de protocoale, instrumente personalizate, soluții originale | Cod original, documentație, prezentări |

---

## 3. Arhitectura sistemului

### 3.1 De ce WSL2 + Docker (și nu Docker Desktop)?

Alegerea arhitecturii **WSL2 + Docker nativ în Ubuntu** (în loc de Docker Desktop) este fundamentată pe mai multe avantaje semnificative pentru mediul educațional:

| Criteriu | WSL2 + Docker nativ | Docker Desktop |
|----------|---------------------|----------------|
| **🚀 Performanță** | Kernel Linux nativ, I/O rapid | Overhead de virtualizare suplimentar |
| **💾 Consum resurse** | ~500MB bază, eficient | ~2GB+ bază, consum RAM ridicat |
| **🌐 Fidelitate rețea** | Stivă de rețea Linux completă | Abstractizare și limitări |
| **📁 Integrare fișiere** | Acces direct la sistemul de fișiere Windows | Montări cu overhead |
| **💰 Licențiere** | Complet gratuit | Restricții pentru întreprinderi (>250 angajați) |
| **🎓 Valoare educativă** | Competențe Linux reale, transferabile | Abstracție care ascunde complexitatea |
| **🔧 Control** | Control complet asupra configurației | Configurație limitată |

### 3.2 Diagrama arhitecturii complete

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              WINDOWS 10/11 HOST                                  │
│                                                                                  │
│  ┌────────────────┐   ┌────────────────┐   ┌────────────────┐   ┌────────────┐ │
│  │   Wireshark    │   │    Browser     │   │  PowerShell/   │   │  VS Code   │ │
│  │  (Analizor     │   │   (Portainer   │   │   Terminal     │   │   (IDE)    │ │
│  │   nativ Win)   │   │    :9000)      │   │   Windows      │   │            │ │
│  └───────┬────────┘   └───────┬────────┘   └───────┬────────┘   └─────┬──────┘ │
│          │                    │                    │                  │         │
│          │     ┌──────────────┴──────────────┬─────┴──────────────────┘         │
│          │     │                             │                                   │
│          ▼     ▼                             ▼                                   │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                    vEthernet (WSL) — Rețea Virtuală                        │  │
│  │              Interfața de bridge între Windows și Linux                    │  │
│  │                     IP dinamic: 172.x.x.x                                  │  │
│  └───────────────────────────────────────────┬───────────────────────────────┘  │
│                                              │                                   │
│  ┌───────────────────────────────────────────┴───────────────────────────────┐  │
│  │                         WSL2 (Mașină Virtuală Lightweight)                 │  │
│  │  ┌─────────────────────────────────────────────────────────────────────┐  │  │
│  │  │                        Ubuntu 22.04 LTS                              │  │  │
│  │  │                   Utilizator: stud | Parolă: stud                    │  │  │
│  │  │  ┌───────────────────────────────────────────────────────────────┐  │  │  │
│  │  │  │                      Docker Engine 28.2.2                      │  │  │  │
│  │  │  │                                                                │  │  │  │
│  │  │  │   ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │  │  │  │
│  │  │  │   │  Container  │  │  Container  │  │     Portainer CE    │  │  │  │  │
│  │  │  │   │   Week N    │  │   Servicii  │  │     2.33.6 LTS      │  │  │  │  │
│  │  │  │   │    Lab      │  │   Backend   │  │  stud/studstudstud  │  │  │  │  │
│  │  │  │   │             │  │             │  │                     │  │  │  │  │
│  │  │  │   │ Porturi:    │  │ Porturi:    │  │ Porturi:            │  │  │  │  │
│  │  │  │   │ 9090-9099   │  │ 8080-8089   │  │ 9000 (HTTP)         │  │  │  │  │
│  │  │  │   │             │  │             │  │ 9443 (HTTPS)        │  │  │  │  │
│  │  │  │   └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │  │  │  │
│  │  │  │          │                │                    │             │  │  │  │
│  │  │  │   ┌──────┴────────────────┴────────────────────┴──────────┐  │  │  │  │
│  │  │  │   │              Docker Bridge Network                     │  │  │  │  │
│  │  │  │   │        weekN_network (subnet dedicat/săptămână)       │  │  │  │  │
│  │  │  │   │              172.20.x.0/24 sau 10.x.x.0/24            │  │  │  │  │
│  │  │  │   └────────────────────────────────────────────────────────┘  │  │  │  │
│  │  │  │                                                                │  │  │  │
│  │  │  └────────────────────────────────────────────────────────────────┘  │  │  │
│  │  │                                                                       │  │  │
│  │  │  ┌─────────────────────────────────────────────────────────────────┐ │  │  │
│  │  │  │  INSTRUMENTE INSTALATE:                                          │ │  │  │
│  │  │  │  Python 3.11+ │ tcpdump │ tshark │ netcat │ nmap │ iperf3       │ │  │  │
│  │  │  │  git │ curl │ wget │ vim │ nano │ htop │ tree                   │ │  │  │
│  │  │  └─────────────────────────────────────────────────────────────────┘ │  │  │
│  │  │                                                                       │  │  │
│  │  └───────────────────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                    │
└────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.3 Fluxul de date în rețea

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                         FLUXUL DE TRAFIC ÎN LABORATOR                            │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─────────────┐                                              ┌─────────────┐   │
│  │  Container  │ ◀──────── Docker Bridge Network ──────────▶ │  Container  │   │
│  │     A       │           (comunicare internă)               │     B       │   │
│  └──────┬──────┘                                              └──────┬──────┘   │
│         │                                                            │          │
│         └──────────────────────┬─────────────────────────────────────┘          │
│                                │                                                 │
│                                ▼                                                 │
│                    ┌───────────────────────┐                                    │
│                    │   Docker NAT Gateway   │                                    │
│                    │   (docker0 / bridge)   │                                    │
│                    └───────────┬───────────┘                                    │
│                                │                                                 │
│                                ▼                                                 │
│                    ┌───────────────────────┐                                    │
│                    │   WSL2 eth0 Interface  │                                    │
│                    │   (IP dinamic Linux)   │                                    │
│                    └───────────┬───────────┘                                    │
│                                │                                                 │
│    ══════════════════════════════════════════════════════════════════════════   │
│                    GRANIȚA WSL2 ↔ WINDOWS                                        │
│    ══════════════════════════════════════════════════════════════════════════   │
│                                │                                                 │
│                                ▼                                                 │
│         ┌──────────────────────────────────────────────────────────────┐        │
│         │                vEthernet (WSL)                                │        │
│         │    ← Wireshark capturează aici traficul WSL →                │        │
│         └──────────────────────────────────────────────────────────────┘        │
│                                │                                                 │
│                                ▼                                                 │
│                    ┌───────────────────────┐                                    │
│                    │  Windows Network Stack │                                    │
│                    │   (Internet Access)    │                                    │
│                    └───────────────────────┘                                    │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Structura repository-ului

### 4.1 Organizarea directoarelor

```
netENwsl/
│
├── 📁 00BEFOREanythingELSE/           # ⚠️ CITIȚI ÎNTÂI! Cerințe preliminare
│   ├── PREREQUISITES_EN.html          # Ghid interactiv HTML (engleză)
│   ├── PrerequisitesEN.md             # Ghid Markdown (engleză)
│   ├── PrerequisitesRO.md             # Ghid Markdown (română)
│   └── wireshark_capture_example.png  # Screenshot exemplu captură
│
├── 📁 1enWSL/                         # Săptămâna 1: Fundamente rețele
├── 📁 2enWSL/                         # Săptămâna 2: Modele & Socket-uri
├── 📁 3enWSL/                         # Săptămâna 3: Programare rețea
├── 📁 4enWSL/                         # Săptămâna 4: Fizic & Legătură date
├── 📁 5enWSL/                         # Săptămâna 5: Adresare IP & Subrețele
├── 📁 6enWSL/                         # Săptămâna 6: NAT/PAT, SDN
├── 📁 7enWSL/                         # Săptămâna 7: Filtrare & Securitate
├── 📁 8enWSL/                         # Săptămâna 8: HTTP & Proxy invers
├── 📁 9enWSL/                         # Săptămâna 9: Sesiune & Prezentare
├── 📁 10enWSL/                        # Săptămâna 10: Protocoale aplicație
├── 📁 11enWSL/                        # Săptămâna 11: FTP, DNS, SSH, LB
├── 📁 12enWSL/                        # Săptămâna 12: Email & RPC
├── 📁 13enWSL/                        # Săptămâna 13: IoT & Securitate
├── 📁 14enWSL/                        # Săptămâna 14: Integrare finală
│
└── 📄 README.md                       # Acest fișier
```

### 4.2 Statistici repository

| Metrică | Valoare |
|---------|---------|
| **Săptămâni acoperite** | 14 |
| **Dimensiune totală** | ~4.6 MB (fără Docker images) |
| **Limbaj principal** | Python (95.9%) |
| **Fișiere HTML** | 3.2% |
| **Alte fișiere** | 0.9% (Markdown, YAML, Dockerfile, etc.) |
| **Licență** | MIT |

---

# PARTEA II — CONFIGURAREA MEDIULUI DE LUCRU

---

## 5. Cerințe de sistem

### 5.1 Cerințe hardware

| Componentă | Minim | Recomandat | Observații |
|------------|-------|------------|------------|
| **Procesor** | 64-bit, 2 cores, VT-x/AMD-V | 64-bit, 4+ cores | Virtualizarea TREBUIE activată în BIOS |
| **RAM** | 8 GB | 16 GB | WSL2 + Docker + containere |
| **Stocare** | 25 GB liber | 50 GB liber | **SSD puternic recomandat** pentru I/O rapid |
| **Rețea** | Orice conexiune internet | Ethernet/WiFi stabil | Necesar pentru descărcare imagini Docker |

### 5.2 Cerințe software

| Component | Versiune | Scop | Verificare |
|-----------|----------|------|------------|
| **Windows** | 10 (21H2+) sau 11 | Sistem de operare gazdă | `winver` în Run |
| **WSL2** | 2.x (ultima) | Subsistem Linux | `wsl --status` |
| **Ubuntu** | 22.04 LTS | Distribuție Linux în WSL | `lsb_release -a` |
| **Docker Engine** | 28.2.2+ | Runtime containere | `docker --version` |
| **Docker Compose** | 1.29.x+ sau 2.x | Orchestrare multi-container | `docker compose version` |
| **Portainer CE** | 2.33.6 LTS | Management vizual containere | http://localhost:9000 |
| **Wireshark** | 4.4.x | Analiză pachete (Windows nativ) | Lansare aplicație |
| **Python** | 3.11+ | Execuție scripturi | `python3 --version` |
| **Git** | 2.40+ | Control versiuni | `git --version` |

### 5.3 Configurare WSL2 recomandată

Creați sau editați fișierul `%UserProfile%\.wslconfig` (ex: `C:\Users\NumeUtilizator\.wslconfig`):

```ini
[wsl2]
# Alocarea memoriei pentru WSL2
memory=8GB

# Numărul de procesoare alocate
processors=4

# Spațiu swap
swap=4GB

# Permite accesul la servicii WSL din Windows via localhost
localhostForwarding=true

[experimental]
# Eliberează memoria neutilizată gradual
autoMemoryReclaim=gradual

# Networking îmbunătățit (opțional)
networkingMode=mirrored
```

> 💡 **Notă:** După modificarea `.wslconfig`, executați `wsl --shutdown` și reporniți WSL pentru a aplica schimbările.

---

## 6. Credențiale standard

> ⚠️ **IMPORTANT:** Folosiți **exact** aceste credențiale pentru toate exercițiile de laborator pentru a asigura consistența și compatibilitatea cu materialele de curs.

### 6.1 Tabel centralizat credențiale

| Serviciu | Utilizator | Parolă | URL/Acces | Observații |
|----------|------------|--------|-----------|------------|
| **Ubuntu WSL** | `stud` | `stud` | Terminal WSL | Utilizator cu privilegii `sudo` |
| **Portainer** | `stud` | `studstudstud` | http://localhost:9000 | Parolă min. 12 caractere |
| **Portainer HTTPS** | `stud` | `studstudstud` | https://localhost:9443 | Certificat self-signed |
| **DVWA** (Săpt. 13) | `admin` | `password` | http://localhost:8080 | După configurare inițială |
| **FTP** (diverse săpt.) | `anonymous` | (gol) | localhost:2121 | Sau porturi specifice |

### 6.2 De ce aceste credențiale?

- **`stud/stud`** pentru Ubuntu — simplu de reținut, consistent cu mediul academic
- **`studstudstud`** pentru Portainer — Portainer impune o parolă de **minimum 12 caractere**
- **Credențiale consistente** — toate materialele de curs și scripturile sunt pre-configurate cu aceste valori

---

## 7. Instalare pas cu pas

### 7.1 Pasul 1: Activare WSL2

#### 7.1.1 Deschideți PowerShell ca Administrator

1. Apăsați `Win + X` sau click dreapta pe butonul Start
2. Selectați **"Windows Terminal (Admin)"** sau **"PowerShell (Admin)"**
3. Confirmați cu **"Da"** la promptul User Account Control

#### 7.1.2 Instalați WSL2

```powershell
wsl --install
```

**Ce face această comandă:**
- ✅ Activează funcția Windows Subsystem for Linux
- ✅ Activează funcția Virtual Machine Platform
- ✅ Descarcă și instalează kernel-ul Linux WSL2
- ✅ Setează WSL2 ca versiune implicită

#### 7.1.3 Reporniți calculatorul

```powershell
Restart-Computer
```

> 🔄 **Restart OBLIGATORIU!** Salvați toate documentele înainte de repornire.

#### 7.1.4 Verificați instalarea

După restart, deschideți PowerShell și verificați:

```powershell
wsl --status
```

**Output așteptat:**
```
Default Distribution: Ubuntu
Default Version: 2
Windows Subsystem for Linux was last updated on [date]
WSL automatic updates are on.
Kernel version: 5.15.x.x-microsoft-standard-WSL2
```

---

### 7.2 Pasul 2: Instalare Ubuntu 22.04

#### 7.2.1 Instalați Ubuntu

```powershell
wsl --install -d Ubuntu-22.04 --web-download
```

#### 7.2.2 Configurați utilizatorul

Când vi se cere, introduceți:

```
Enter new UNIX username: stud
New password: stud
Retype new password: stud
```

> 📝 **Notă:** Parola NU se afișează când o tastați — comportament normal Linux.

#### 7.2.3 Verificați instalarea

```powershell
wsl -l -v
```

**Output așteptat:**
```
  NAME            STATE           VERSION
* Ubuntu-22.04    Running         2
```

---

### 7.3 Pasul 3: Instalare Docker în WSL

#### 7.3.1 Deschideți terminalul Ubuntu

```powershell
wsl -d Ubuntu-22.04
```

#### 7.3.2 Actualizați sistemul

```bash
sudo apt update && sudo apt upgrade -y
```

#### 7.3.3 Instalați dependențele

```bash
sudo apt install -y ca-certificates curl gnupg lsb-release
```

#### 7.3.4 Adăugați cheia GPG Docker

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

#### 7.3.5 Adăugați repository-ul Docker

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

#### 7.3.6 Instalați Docker Engine

```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

#### 7.3.7 Adăugați utilizatorul în grupul docker

```bash
sudo usermod -aG docker $USER
```

#### 7.3.8 Porniți serviciul Docker

```bash
sudo service docker start
```

#### 7.3.9 Aplicați modificările de grup

```bash
newgrp docker
```

#### 7.3.10 Verificați instalarea

```bash
docker --version
docker run hello-world
```

---

### 7.4 Pasul 4: Instalare Portainer CE

#### 7.4.1 Creați volumul pentru date persistente

```bash
docker volume create portainer_data
```

#### 7.4.2 Rulați containerul Portainer

```bash
docker run -d \
  -p 9000:9000 \
  -p 9443:9443 \
  --name portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest
```

#### 7.4.3 Configurați contul administrator

1. Deschideți browserul și navigați la: **http://localhost:9000**
2. Creați contul de administrator:
   - **Username:** `stud`
   - **Password:** `studstudstud`
3. Click pe **"Create user"**

> ⚠️ **ATENȚIE:** Aveți **5 minute** să creați contul după prima pornire. Dacă depășiți, trebuie să recreați containerul.

#### 7.4.4 Conectați-vă la mediul local Docker

1. Selectați **"Get Started"**
2. Alegeți **"local"** environment
3. Click pe **"Connect"**

---

### 7.5 Pasul 5: Instalare Wireshark (Windows)

#### 7.5.1 Descărcați Wireshark

Navigați la: **https://www.wireshark.org/download.html**

Descărcați versiunea pentru **Windows x64 Installer**.

#### 7.5.2 Instalați Wireshark

1. Rulați installer-ul descărcat
2. La componente, asigurați-vă că **Npcap** este selectat
3. La opțiunile Npcap:
   - ✅ Bifați **"Install Npcap in WinPcap API-compatible Mode"**
   - ✅ Bifați **"Support raw 802.11 traffic"** (opțional)
4. Finalizați instalarea

#### 7.5.3 Verificați instalarea

1. Lansați Wireshark
2. Verificați că vedeți interfața **"vEthernet (WSL)"** în lista de interfețe
3. WSL trebuie să ruleze pentru a vedea această interfață

---

### 7.6 Pasul 6: Instalare pachete Python

#### 7.6.1 În terminalul Ubuntu WSL

```bash
# Instalare pip dacă nu există
sudo apt install -y python3-pip python3-venv

# Instalare pachete necesare pentru laborator
pip3 install --break-system-packages \
    docker \
    scapy \
    dpkt \
    requests \
    flask \
    paramiko \
    pyftpdlib \
    paho-mqtt \
    dnspython \
    grpcio \
    grpcio-tools \
    protobuf \
    PyYAML \
    colorama \
    pytest
```

#### 7.6.2 Verificare instalare

```bash
python3 -c "import docker; print('docker:', docker.__version__)"
python3 -c "import scapy; print('scapy: OK')"
python3 -c "import dpkt; print('dpkt: OK')"
python3 -c "import requests; print('requests: OK')"
```

---

### 7.7 Pasul 7: Configurare auto-start Docker (opțional)

Pentru ca Docker să pornească automat când deschideți Ubuntu:

#### 7.7.1 Editați fișierul .bashrc

```bash
nano ~/.bashrc
```

#### 7.7.2 Adăugați la sfârșit

```bash
# Auto-start Docker service
if service docker status 2>&1 | grep -q "is not running"; then
    sudo service docker start > /dev/null 2>&1
fi
```

#### 7.7.3 Configurați sudo fără parolă pentru Docker

```bash
echo "$USER ALL=(ALL) NOPASSWD: /usr/sbin/service docker *" | sudo tee /etc/sudoers.d/docker-service
```

---

## 8. Verificarea instalării

### 8.1 Script complet de verificare

Creați și rulați acest script în Ubuntu:

```bash
#!/bin/bash
# verify_lab_environment.sh
# Script de verificare completă a mediului de laborator

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

echo ""
echo "╔═══════════════════════════════════════════════════════════════════════════╗"
echo "║        VERIFICARE MEDIU LABORATOR REȚELE DE CALCULATOARE                  ║"
echo "║                         by Revolvix                                        ║"
echo "╚═══════════════════════════════════════════════════════════════════════════╝"
echo ""

check_required() {
    if eval "$2" &>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $1"
    else
        echo -e "  ${RED}✗${NC} $1"
        ((ERRORS++))
    fi
}

check_optional() {
    if eval "$2" &>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $1"
    else
        echo -e "  ${YELLOW}○${NC} $1 (opțional)"
        ((WARNINGS++))
    fi
}

echo -e "${BLUE}▶ INFORMAȚII SISTEM${NC}"
echo "  Hostname: $(hostname)"
echo "  Ubuntu: $(lsb_release -d 2>/dev/null | cut -f2)"
echo "  Kernel: $(uname -r)"
echo "  User: $(whoami)"
echo ""

echo -e "${BLUE}▶ COMPONENTE PRINCIPALE${NC}"
check_required "Python 3.11+" "python3 --version | grep -E 'Python 3\.(1[1-9]|[2-9][0-9])'"
check_required "pip3" "pip3 --version"
check_required "Git" "git --version"
check_required "curl" "curl --version"
check_required "wget" "wget --version"
echo ""

echo -e "${BLUE}▶ DOCKER${NC}"
check_required "Docker Engine" "docker --version"
check_required "Docker Compose" "docker compose version"
check_required "Docker daemon activ" "docker info"
check_required "Docker fără sudo" "docker ps"
echo ""

echo -e "${BLUE}▶ CONTAINERE ACTIVE${NC}"
docker ps --format "  {{.Names}}: {{.Status}}" 2>/dev/null || echo "  (niciun container activ)"
echo ""

echo -e "${BLUE}▶ INSTRUMENTE REȚEA${NC}"
check_required "tcpdump" "which tcpdump"
check_optional "tshark" "which tshark"
check_required "netcat" "which nc"
check_optional "nmap" "which nmap"
check_optional "iperf3" "which iperf3"
echo ""

echo -e "${BLUE}▶ BIBLIOTECI PYTHON${NC}"
check_required "docker" "python3 -c 'import docker'"
check_required "scapy" "python3 -c 'import scapy.all'"
check_required "dpkt" "python3 -c 'import dpkt'"
check_required "requests" "python3 -c 'import requests'"
check_required "flask" "python3 -c 'import flask'"
check_optional "paramiko" "python3 -c 'import paramiko'"
check_optional "pyftpdlib" "python3 -c 'import pyftpdlib'"
check_optional "paho-mqtt" "python3 -c 'import paho.mqtt.client'"
check_optional "dnspython" "python3 -c 'import dns.resolver'"
check_optional "grpcio" "python3 -c 'import grpc'"
echo ""

echo -e "${BLUE}▶ SERVICII${NC}"
check_required "Docker service" "sudo service docker status | grep -q running"
check_optional "Portainer container" "docker ps | grep -q portainer"
echo ""

echo -e "${BLUE}▶ REȚELE DOCKER${NC}"
docker network ls --format "  {{.Name}}: {{.Driver}}" 2>/dev/null
echo ""

echo "═══════════════════════════════════════════════════════════════════════════"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ TOATE COMPONENTELE NECESARE SUNT INSTALATE CORECT!${NC}"
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}   ($WARNINGS componente opționale lipsesc)${NC}"
    fi
else
    echo -e "${RED}❌ $ERRORS COMPONENTĂ(E) NECESARĂ(E) LIPSEȘTE/LIPSESC SAU E/SUNT CONFIGURATĂ(E) INCORECT${NC}"
fi
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

exit $ERRORS
```

### 8.2 Test rapid captură Wireshark

1. Deschideți **Wireshark** pe Windows
2. Selectați interfața **vEthernet (WSL)** și porniți captura
3. În terminalul Ubuntu, rulați:

```bash
docker run --rm alpine ping -c 5 8.8.8.8
```

4. În Wireshark, aplicați filtrul: `icmp`
5. Verificați că vedeți pachete **Echo request** și **Echo reply**

---

# PARTEA III — CURRICULA SĂPTĂMÂNALĂ DETALIATĂ

---

## 9. Ghid rapid de pornire a laboratoarelor

### 9.1 Workflow standard pentru fiecare săptămână

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     WORKFLOW STANDARD LABORATOR                               │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. CLONARE              2. VERIFICARE           3. PORNIRE                  │
│  ┌──────────────┐       ┌──────────────┐       ┌──────────────┐             │
│  │ git clone    │  ──▶  │ python       │  ──▶  │ python       │             │
│  │ (sparse)     │       │ verify_env.py│       │ start_lab.py │             │
│  └──────────────┘       └──────────────┘       └──────────────┘             │
│                                                        │                     │
│                                                        ▼                     │
│  6. CURĂȚARE             5. ANALIZĂ             4. EXERCIȚII                │
│  ┌──────────────┐       ┌──────────────┐       ┌──────────────┐             │
│  │ python       │  ◀──  │ Wireshark    │  ◀──  │ Exerciții    │             │
│  │ cleanup.py   │       │ PCAP files   │       │ Python       │             │
│  └──────────────┘       └──────────────┘       └──────────────┘             │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Comenzi standard disponibile în fiecare kit

```bash
# Verificare mediu
python setup/verify_environment.py

# Pornire servicii laborator
python scripts/start_lab.py

# Verificare status servicii
python scripts/start_lab.py --status

# Rulare demonstrații
python scripts/run_demo.py --demo 1

# Captură trafic
python scripts/capture_traffic.py --interface lo --port 9090 --output pcap/capture.pcap

# Oprire servicii
python scripts/stop_lab.py

# Curățare completă
python scripts/cleanup.py --full
```

---

## 10. Clonarea individuală a fiecărei săptămâni

### 10.1 Metodă recomandată: Git Sparse Checkout

Această metodă descarcă **doar fișierele necesare** pentru săptămâna respectivă, economisind spațiu și timp.

### 10.2 Comenzi de clonare pentru fiecare săptămână

> 📍 **Executați aceste comenzi în PowerShell sau Terminal Windows**

---

#### 📦 Clonare Săptămâna 1 — Fundamente ale rețelelor

```powershell
cd ~\Documents
git clone --filter=blob:none --sparse https://github.com/antonioclim/netENwsl.git WEEK1
cd WEEK1
git sparse-checkout set 1enWSL
Move-Item 1enWSL\* . -Force
Remove-Item 1enWSL -Force
```

---

#### 📦 Clonare Săptămâna 2 — Modele arhitecturale și socket-uri

```powershell
cd ~\Documents
git clone --filter=blob:none --sparse https://github.com/antonioclim/netENwsl.git WEEK2
cd WEEK2
git sparse-checkout set 2enWSL
Move-Item 2enWSL\* . -Force
Remove-Item 2enWSL -Force
```

---

#### 📦 Clonare Săptămâna 3 — Paradigme de programare în rețea

```powershell
cd ~\Documents
git clone --filter=blob:none --sparse https://github.com/antonioclim/netENwsl.git WEEK3
cd WEEK3
git sparse-checkout set 3enWSL
Move-Item 3enWSL\* . -Force
Remove-Item 3enWSL -Force
```

---

#### 📦 Clonare Săptămâna 4 — Nivelurile fizic și legătură de date

```powershell
cd ~\Documents
git clone --filter=blob:none --sparse https://github.com/antonioclim/netENwsl.git WEEK4
cd WEEK4
git sparse-checkout set 4enWSL
Move-Item 4enWSL\* . -Force
Remove-Item 4enWSL -Force
```

---

#### 📦 Clonare Săptămâna 5 — Nivelul rețea și adresare IP

```powershell
cd ~\Documents
git clone --filter=blob:none --sparse https://github.com/antonioclim/netENwsl.git WEEK5
cd WEEK5
git sparse-checkout set 5enWSL
Move-Item 5enWSL\* . -Force
Remove-Item 5enWSL -Force
```

---

#### 📦 Clonare Săptămâna 6 — NAT/PAT, protocoale suport și SDN

```powershell
cd ~\Documents
git clone --filter=blob:none --sparse https://github.com/antonioclim/netENwsl.git WEEK6
cd WEEK6
git sparse-checkout set 6enWSL
Move-Item 6enWSL\* . -Force
Remove-Item 6enWSL -Force
```

---

#### 📦 Clonare Săptămâna 7 — Interceptare pachete și securitate

```powershell
cd ~\Documents
git clone --filter=blob:none --sparse https://github.com/antonioclim/netENwsl.git WEEK7
cd WEEK7
git sparse-checkout set 7enWSL
Move-Item 7enWSL\* . -Force
Remove-Item 7enWSL -Force
```

---

#### 📦 Clonare Săptămâna 8 — Nivelul transport, HTTP și proxy

```powershell
cd ~\Documents
git clone --filter=blob:none --sparse https://github.com/antonioclim/netENwsl.git WEEK8
cd WEEK8
git sparse-checkout set 8enWSL
Move-Item 8enWSL\* . -Force
Remove-Item 8enWSL -Force
```

---

#### 📦 Clonare Săptămâna 9 — Nivelurile sesiune și prezentare

```powershell
cd ~\Documents
git clone --filter=blob:none --sparse https://github.com/antonioclim/netENwsl.git WEEK9
cd WEEK9
git sparse-checkout set 9enWSL
Move-Item 9enWSL\* . -Force
Remove-Item 9enWSL -Force
```

---

#### 📦 Clonare Săptămâna 10 — Protocoale de nivel aplicație

```powershell
cd ~\Documents
git clone --filter=blob:none --sparse https://github.com/antonioclim/netENwsl.git WEEK10
cd WEEK10
git sparse-checkout set 10enWSL
Move-Item 10enWSL\* . -Force
Remove-Item 10enWSL -Force
```

---

#### 📦 Clonare Săptămâna 11 — FTP, DNS, SSH, Load Balancing

```powershell
cd ~\Documents
git clone --filter=blob:none --sparse https://github.com/antonioclim/netENwsl.git WEEK11
cd WEEK11
git sparse-checkout set 11enWSL
Move-Item 11enWSL\* . -Force
Remove-Item 11enWSL -Force
```

---

#### 📦 Clonare Săptămâna 12 — Protocoale email și RPC

```powershell
cd ~\Documents
git clone --filter=blob:none --sparse https://github.com/antonioclim/netENwsl.git WEEK12
cd WEEK12
git sparse-checkout set 12enWSL
Move-Item 12enWSL\* . -Force
Remove-Item 12enWSL -Force
```

---

#### 📦 Clonare Săptămâna 13 — IoT și securitatea rețelelor

```powershell
cd ~\Documents
git clone --filter=blob:none --sparse https://github.com/antonioclim/netENwsl.git WEEK13
cd WEEK13
git sparse-checkout set 13enWSL
Move-Item 13enWSL\* . -Force
Remove-Item 13enWSL -Force
```

---

#### 📦 Clonare Săptămâna 14 — Recapitulare și evaluare

```powershell
cd ~\Documents
git clone --filter=blob:none --sparse https://github.com/antonioclim/netENwsl.git WEEK14
cd WEEK14
git sparse-checkout set 14enWSL
Move-Item 14enWSL\* . -Force
Remove-Item 14enWSL -Force
```

---

#### 📦 Clonare Cerințe Preliminare (00BEFOREanythingELSE)

```powershell
cd ~\Documents
git clone --filter=blob:none --sparse https://github.com/antonioclim/netENwsl.git PREREQUISITES
cd PREREQUISITES
git sparse-checkout set 00BEFOREanythingELSE
Move-Item 00BEFOREanythingELSE\* . -Force
Remove-Item 00BEFOREanythingELSE -Force
```

---

### 10.3 Clonare completă a repository-ului

Dacă preferați să aveți toate săptămânile într-un singur loc:

```powershell
cd ~\Documents
git clone https://github.com/antonioclim/netENwsl.git
cd netENwsl
```

---

## 11. Săptămâna 1: Fundamente ale rețelelor

**Director:** `1enWSL/`  
**Rețea Docker:** `172.20.1.0/24`  
**Porturi:** 9090 (TCP), 9091 (UDP), 9092 (Alternativ)

### 11.1 Sinopsis

Acest laborator introductiv stabilește competențele fundamentale în diagnosticarea rețelelor prin experimentare practică cu instrumente CLI esențiale. Studenții dezvoltă intuiție practică despre comportamentul rețelelor prin examinarea configurațiilor de interfață, validarea conectivității și capturarea traficului pentru analiza protocoalelor.

### 11.2 Obiective de învățare

| Nivel Bloom | Verb | Obiectiv concret |
|-------------|------|------------------|
| **A reține** | Reamintește | Comenzile Linux esențiale: `ip addr`, `ip route`, `ss`, `ping`, `netcat` |
| **A înțelege** | Explică | Scopul interfețelor de rețea, tabelelor de rutare și stărilor socket-urilor |
| **A aplica** | Demonstrează | Testarea conectivității folosind ICMP și interpretarea măsurătorilor de latență |
| **A aplica** | Implementează | Canale TCP/UDP de bază folosind netcat și socket-uri Python |
| **A analiza** | Examinează | Capturi de rețea pentru identificarea comportamentului protocoalelor |
| **A analiza** | Compară | Pattern-uri de comunicare TCP vs UDP prin examinarea pachetelor |
| **A evalua** | Diagnostichează | Probleme comune de conectivitate folosind depanare sistematică |

### 11.3 Tehnologii cheie

`ip`, `ss`, `ping`, `traceroute`, `netcat`, `tcpdump`, `tshark`, socket-uri Python

### 11.4 Exerciții

| Nr. | Titlu | Durată | Descriere |
|-----|-------|--------|-----------|
| 1 | Inspecție interfețe de rețea | 15 min | Enumerarea interfețelor, examinarea IP, documentarea routing |
| 2 | Testarea conectivității | 20 min | Teste ping progresive, măsurarea latenței |
| 3 | Comunicare TCP cu netcat | 25 min | Sesiuni bidirecționale, observarea stării conexiunii |
| 4 | Captură și analiză trafic | 30 min | TCP handshake, identificarea câmpurilor, export CSV |
| 5 | Analiză statistică PCAP | 20 min | Procesare programatică Python a capturilor |

### 11.5 Servicii disponibile

| Serviciu | Port | Acces |
|----------|------|-------|
| Container laborator | Shell Docker | `docker exec -it week1_lab bash` |
| Server test TCP | 9090 | `nc localhost 9090` |
| Server test UDP | 9091 | `nc -u localhost 9091` |
| Portainer | 9443 | https://localhost:9443 |

---

## 12. Săptămâna 2: Modele arhitecturale și programare socket

**Director:** `2enWSL/`  
**Rețea Docker:** `10.0.2.0/24`

### 12.1 Sinopsis

Acest laborator explorează modelele de referință OSI și TCP/IP prin exerciții practice de programare cu socket-uri. Studenții implementează pattern-uri de comunicare client-server, înțelegând cum fluxul de date traversează stiva de protocoale.

### 12.2 Obiective de învățare

| Nivel Bloom | Obiectiv |
|-------------|----------|
| **A reține** | Identificarea celor 7 straturi OSI și 4 straturi TCP/IP cu PDU-urile respective |
| **A înțelege** | Explicarea procesului de încapsulare și transformările PDU |
| **A aplica** | Implementarea clienților și serverelor TCP/UDP folosind API-ul socket Python |
| **A aplica** | Demonstrarea pattern-urilor de server concurent cu threading |
| **A analiza** | Trasarea fluxului de date prin multiple straturi în capturi |
| **A evalua** | Compararea operațiunilor socket blocante vs non-blocante |

### 12.3 Tehnologii cheie

Python `socket`, `threading`, `concurrent.futures`, modelul OSI, modelul TCP/IP, `scapy`, `dpkt`

### 12.4 Exerciții

| Nr. | Titlu | Descriere |
|-----|-------|-----------|
| 1 | Identificarea straturilor | Adnotare capturi cu delimitările straturilor |
| 2 | Echo Server/Client TCP | Implementare de bază cu error handling |
| 3 | Schimb datagrame UDP | Pattern-uri comunicare connectionless |
| 4 | Server TCP concurent | Multi-client handling cu thread pools |
| 5 | Analizor de protocoale | Parser personalizat cu scapy |

---

## 13. Săptămâna 3: Paradigme de programare în rețea

**Director:** `3enWSL/`  
**Rețea Docker:** `172.20.0.0/24`

### 13.1 Sinopsis

Laboratorul introduce pattern-uri avansate de programare incluzând UDP broadcast/multicast, tunelare TCP și design de protocoale la nivel aplicație.

### 13.2 Obiective de învățare

| Nivel Bloom | Obiectiv |
|-------------|----------|
| **A reține** | Distincțiile între adresare unicast, broadcast și multicast |
| **A înțelege** | Apartenență grupuri multicast și fundamentele IGMP |
| **A aplica** | Implementare broadcast UDP pentru descoperire servicii |
| **A aplica** | Configurare și utilizare socket-uri multicast |
| **A analiza** | Pattern-uri trafic multicast în capturi |
| **A crea** | Protocol simplu de descoperire folosind broadcast/multicast |

### 13.3 Tehnologii cheie

UDP multicast, broadcast sockets, opțiuni socket (`SO_BROADCAST`, `IP_ADD_MEMBERSHIP`), `struct`

---

## 14. Săptămâna 4: Nivelurile fizic și legătură de date

**Director:** `4enWSL/`  
**Rețea Docker:** `172.28.0.0/16`

### 14.1 Sinopsis

Laboratorul coboară la cele mai jos straturi accesibile, examinând încadrarea Ethernet, adresarea MAC și construcția de protocoale binare cu CRC32.

### 14.2 Tehnologii cheie

`struct`, `binascii`, `zlib.crc32`, cadre Ethernet, adresare MAC, protocoale binare

### 14.3 Exerciții principale

1. **Disecția cadrelor Ethernet** — Parsare raw frames
2. **Protocol mesaje binare** — Design header cu tip, lungime, secvență
3. **Implementare CRC32** — Verificare integritate
4. **Problema încadrării** — Byte-stuffing sau length-prefixing

---

## 15. Săptămâna 5: Nivelul rețea și adresare IP

**Director:** `5enWSL/`  
**Rețea Docker:** `10.5.0.0/24`

### 15.1 Sinopsis

Acoperire comprehensivă a adresării IP, metodologiilor de subrețele (CIDR, FLSM, VLSM) și fundamentelor IPv6.

### 15.2 Tehnologii cheie

Modulul `ipaddress`, notația CIDR, FLSM, VLSM, IPv4, IPv6, calculatoare de subrețele

### 15.3 Exerciții principale

1. **Calculator subrețele** — Tool Python pentru calcule CIDR
2. **Design VLSM** — Alocare subrețele la departamente
3. **Adresare IPv6** — Configurare și testare conectivitate
4. **Verificare adrese** — Validare configurații prin analiza pachetelor

---

## 16. Săptămâna 6: NAT/PAT, protocoale suport și SDN

**Director:** `6enWSL/`  
**Rețea Docker:** Topologie personalizată cu segmente multiple

### 16.1 Sinopsis

Network Address Translation, protocoale suport esențiale (ARP, DHCP, ICMP, NDP) și introducere în Software-Defined Networking.

### 16.2 Tehnologii cheie

`iptables`, NAT/PAT, ARP, DHCP, ICMP, NDP, Open vSwitch, os-ken (fork Ryu), Mininet

### 16.3 Exerciții principale

1. **Configurare NAT** — MASQUERADE pentru acces internet containere
2. **Port Forwarding** — Expunere servicii interne via DNAT
3. **Observare ARP** — Captură și analiză request/reply
4. **Introducere SDN** — L2 learning switch cu os-ken

---

## 17. Săptămâna 7: Interceptare pachete, filtrare și securitate

**Director:** `7enWSL/`  
**Rețea Docker:** `10.0.7.0/24`

### 17.1 Sinopsis

Competențe esențiale de securitate și forensică prin filtrarea pachetelor, configurarea firewall-ului și scanarea defensivă a porturilor.

### 17.2 Tehnologii cheie

`tcpdump`, `tshark`, filtre Wireshark, `iptables`, `nmap`, scanare porturi, Mininet

### 17.3 Exerciții principale

1. **Filtrare pachete** — Construirea regulilor iptables
2. **Analiză conexiuni** — Diagnosticare conexiuni filtrate
3. **Scanare porturi** — TCP connect și SYN scans
4. **Verificare firewall** — Validare eficacitate reguli

---

## 18. Săptămâna 8: Nivelul transport, HTTP și proxy invers

**Director:** `8enWSL/`  
**Rețea Docker:** `172.28.8.0/24`  
**Porturi:** 8080 (HTTP), 9443 (Portainer)

### 18.1 Sinopsis

Mecanisme nivel transport (TCP handshake, flow control) și aplicarea în implementarea serverelor HTTP cu Nginx ca reverse proxy.

### 18.2 Containere disponibile

| Container | Rol | Port |
|-----------|-----|------|
| `week8-nginx-proxy` | Reverse proxy + Load balancer | 8080 |
| `week8-backend-1` | Server HTTP backend | intern |
| `week8-backend-2` | Server HTTP backend | intern |
| `week8-backend-3` | Server HTTP backend | intern |
| `week8-portainer` | Management UI | 9443 |

### 18.3 Tehnologii cheie

TCP handshake, HTTP/1.1, `http.server`, Nginx, reverse proxy, load balancing, Docker Compose

---

## 19. Săptămâna 9: Nivelurile sesiune și prezentare

**Director:** `9enWSL/`  
**Rețea Docker:** `172.29.9.0/24`

### 19.1 Sinopsis

Management sesiuni și prezentare date, cu focus pe FTP (moduri activ/pasiv) și serializare binară.

### 19.2 Tehnologii cheie

FTP (activ/pasiv), `ftplib`, `pyftpdlib`, încadrare binară, `struct`, gestionare stare sesiune

---

## 20. Săptămâna 10: Protocoale de nivel aplicație

**Director:** `10enWSL/`  
**Rețea Docker:** `172.20.0.0/24`

### 20.1 Sinopsis

Survey protocoale critice: HTTP/HTTPS, REST API, DNS, SSH. Explorare TLS și operațiuni programatice.

### 20.2 Tehnologii cheie

HTTP/HTTPS, TLS/SSL, REST APIs, `requests`, DNS, `dnspython`, SSH, `paramiko`

---

## 21. Săptămâna 11: FTP, DNS, SSH și echilibrarea încărcării

**Director:** `11enWSL/`  
**Rețea Docker:** `172.28.0.0/16`

### 21.1 Sinopsis

Consolidare protocoale aplicație și strategii avansate de load balancing cu health checks.

### 21.2 Tehnologii cheie

Zone DNS, `dnslib`, caching resolvers, algoritmi Nginx load balancing, health checks

---

## 22. Săptămâna 12: Protocoale email și RPC

**Director:** `12enWSL/`  
**Rețea Docker:** `172.28.12.0/24`

### 22.1 Sinopsis

Protocoale email (SMTP, POP3, IMAP) și Remote Procedure Call (JSON-RPC, XML-RPC, gRPC).

### 22.2 Tehnologii cheie

SMTP, POP3, IMAP, `smtplib`, `email`, JSON-RPC, XML-RPC, gRPC, Protocol Buffers

---

## 23. Săptămâna 13: IoT și securitatea rețelelor

**Director:** `13enWSL/`  
**Rețea Docker:** `10.0.13.0/24`

### 23.1 Sinopsis

Protocoale Internet of Things și fundamentele securității rețelelor cu MQTT și vulnerability assessment.

### 23.2 Servicii disponibile

| Serviciu | Port | Credențiale | Descriere |
|----------|------|-------------|-----------|
| Mosquitto MQTT (plain) | 1883 | (fără) | Broker MQTT necriptat |
| Mosquitto MQTT (TLS) | 8883 | Certificat CA | Broker MQTT securizat |
| DVWA | 8080 | admin/password | Damn Vulnerable Web App |
| vsftpd | 2121 | anonymous | FTP cu vulnerabilități cunoscute |

### 23.3 Tehnologii cheie

MQTT, `paho-mqtt`, Mosquitto broker, TLS, port scanning, vulnerability assessment, DVWA

---

## 24. Săptămâna 14: Recapitulare integrată și evaluare

**Director:** `14enWSL/`  
**Rețea Docker:** `172.20.0.0/24`  
**Porturi:** 8080 (HTTP), 9443 (Portainer)

### 24.1 Sinopsis

Laborator de sinteză — construcția unei aplicații multi-tier complete cu load balancing, reverse proxy și validare comprehensivă.

### 24.2 Arhitectură finală

```
                        ┌───────────────────────────────────────────┐
                        │                  CLIENT                    │
                        │            (Cereri HTTP)                   │
                        └─────────────────────┬─────────────────────┘
                                              │
                                              ▼
                        ┌───────────────────────────────────────────┐
                        │           NGINX REVERSE PROXY              │
                        │          (Load Balancer)                   │
                        │       Round-Robin Distribution             │
                        └─────────┬───────────┬───────────┬─────────┘
                                  │           │           │
                        ┌─────────▼───┐ ┌─────▼─────┐ ┌───▼─────────┐
                        │  Backend 1  │ │ Backend 2 │ │  Backend 3  │
                        │   (HTTP)    │ │  (HTTP)   │ │   (HTTP)    │
                        └─────────────┘ └───────────┘ └─────────────┘
```

### 24.3 Obiective finale

- Sintetizarea tuturor conceptelor din semestru
- Deployment multi-container cu Docker Compose
- Trasare completă HTTP prin multiple hop-uri
- Gestionare scenarii de eșec

---

# PARTEA IV — REFERINȚE ȘI SUPORT

---

## 25. Structura standard a kit-urilor

Fiecare director `<N>enWSL/` urmează o organizare consistentă:

```
<N>enWSL/
│
├── 📄 README.md                   # Prezentare săptămână, obiective, exerciții
├── 📄 CHANGELOG.md                # Istoricul versiunilor
├── 📄 LICENSE                     # Licență MIT
│
├── 📁 setup/                      # Configurare mediu
│   ├── requirements.txt           # Dependențe Python
│   ├── install_prerequisites.py   # Script instalare
│   ├── verify_environment.py      # Validare mediu
│   └── configure_docker.py        # Configurare Docker
│
├── 📁 scripts/                    # Automatizare
│   ├── start_lab.py               # Pornire servicii
│   ├── stop_lab.py                # Oprire servicii
│   ├── run_demo.py                # Demonstrații
│   ├── capture_traffic.py         # Captură pachete
│   ├── cleanup.py                 # Curățare completă
│   └── utils/                     # Module partajate
│
├── 📁 src/                        # Cod sursă
│   ├── __init__.py
│   ├── exercises/                 # Exerciții (ex_N_XX_*.py)
│   ├── apps/                      # Aplicații complete
│   └── utils/                     # Module reutilizabile
│
├── 📁 docker/                     # Containerizare
│   ├── Dockerfile.lab             # Imagine container
│   ├── docker-compose.yml         # Orchestrare
│   ├── configs/                   # Configurări servicii
│   └── volumes/                   # Date persistente
│
├── 📁 docs/                       # Documentație
│   ├── theory_summary.md          # Fundamente teoretice
│   ├── commands_cheatsheet.md     # Referință rapidă
│   ├── troubleshooting.md         # Depanare
│   └── further_reading.md         # Referințe academice
│
├── 📁 tests/                      # Validare
│   ├── smoke_test.py              # Verificare rapidă
│   ├── test_environment.py        # Validare comprehensivă
│   ├── test_exercises.py          # Verificare exerciții
│   └── expected_outputs.md        # Output-uri referință
│
├── 📁 homework/                   # Teme pentru acasă
│   ├── README.md                  # Descriere teme
│   ├── exercises/                 # Enunțuri
│   └── solutions/                 # Soluții (parțiale)
│
├── 📁 pcap/                       # Capturi pachete
│   └── README.md
│
└── 📁 artifacts/                  # Output-uri generate
    └── .gitkeep
```

---

## 26. Planul de adresare IP

### 26.1 Subrețele pe săptămâni

| Săpt. | Director | Subrețea Docker | Gateway | Broadcast |
|-------|----------|-----------------|---------|-----------|
| 1 | `1enWSL` | `172.20.1.0/24` | 172.20.1.1 | 172.20.1.255 |
| 2 | `2enWSL` | `10.0.2.0/24` | 10.0.2.1 | 10.0.2.255 |
| 3 | `3enWSL` | `172.20.0.0/24` | 172.20.0.1 | 172.20.0.255 |
| 4 | `4enWSL` | `172.28.0.0/16` | 172.28.0.1 | 172.28.255.255 |
| 5 | `5enWSL` | `10.5.0.0/24` | 10.5.0.1 | 10.5.0.255 |
| 6 | `6enWSL` | SDN custom | variabil | variabil |
| 7 | `7enWSL` | `10.0.7.0/24` | 10.0.7.1 | 10.0.7.255 |
| 8 | `8enWSL` | `172.28.8.0/24` | 172.28.8.1 | 172.28.8.255 |
| 9 | `9enWSL` | `172.29.9.0/24` | 172.29.9.1 | 172.29.9.255 |
| 10 | `10enWSL` | `172.20.0.0/24` | 172.20.0.1 | 172.20.0.255 |
| 11 | `11enWSL` | `172.28.0.0/16` | 172.28.0.1 | 172.28.255.255 |
| 12 | `12enWSL` | `172.28.12.0/24` | 172.28.12.1 | 172.28.12.255 |
| 13 | `13enWSL` | `10.0.13.0/24` | 10.0.13.1 | 10.0.13.255 |
| 14 | `14enWSL` | `172.20.0.0/24` | 172.20.0.1 | 172.20.0.255 |

### 26.2 Convenții de alocare porturi

| Interval | Scop |
|----------|------|
| **9000** | Portainer HTTP |
| **9443** | Portainer HTTPS |
| **9090-9099** | Servicii test TCP/UDP generale |
| **8080-8089** | Servicii HTTP |
| **1883** | MQTT plaintext |
| **8883** | MQTT cu TLS |
| **2121** | FTP (port non-standard) |
| **5000-5999** | Aplicații Flask |

---

## 27. Tehnologii și instrumente utilizate

### 27.1 Runtime principal

| Tehnologie | Versiune | Scop |
|------------|----------|------|
| **Python** | 3.11+ | Limbaj principal programare |
| **Docker Engine** | 28.2.2+ | Runtime containere |
| **Docker Compose** | 2.x | Orchestrare multi-container |
| **Ubuntu** | 22.04 LTS | Distribuție Linux în WSL |

### 27.2 Instrumente analiză rețea

| Instrument | Scop | Instalare |
|------------|------|-----------|
| **tcpdump** | Captură pachete CLI | `apt install tcpdump` |
| **tshark** | CLI Wireshark | `apt install tshark` |
| **Wireshark** | Analizor grafic | Windows installer |
| **nmap** | Scanare și enumerare | `apt install nmap` |
| **netcat (nc)** | Tool universal TCP/UDP | `apt install netcat-openbsd` |
| **iperf3** | Testare performanță | `apt install iperf3` |
| **traceroute** | Trasare rută | `apt install traceroute` |
| **mtr** | traceroute + ping | `apt install mtr` |

### 27.3 Biblioteci Python

| Bibliotecă | Scop | Instalare |
|------------|------|-----------|
| `socket` | Programare rețea low-level | Built-in |
| `scapy` | Manipulare și construire pachete | `pip install scapy` |
| `dpkt` | Parsare pachete și PCAP | `pip install dpkt` |
| `requests` | Client HTTP | `pip install requests` |
| `flask` | Server HTTP | `pip install flask` |
| `paramiko` | Implementare SSH | `pip install paramiko` |
| `pyftpdlib` | Server FTP | `pip install pyftpdlib` |
| `paho-mqtt` | Client MQTT | `pip install paho-mqtt` |
| `dnspython` | Interogări DNS | `pip install dnspython` |
| `grpcio` | Framework gRPC | `pip install grpcio` |
| `docker` | Client API Docker | `pip install docker` |

### 27.4 Servicii infrastructură

| Serviciu | Versiune | Scop |
|----------|----------|------|
| **Portainer CE** | 2.33.6 LTS | Management vizual containere |
| **Nginx** | ultima | Reverse proxy, load balancer |
| **Mosquitto** | ultima | Broker MQTT |
| **Open vSwitch** | 3.x | Software-defined networking |
| **DVWA** | ultima | Training vulnerability assessment |

---

## 28. Ghid complet de depanare

### 28.1 Probleme WSL2

| Problemă | Cauză posibilă | Soluție |
|----------|----------------|---------|
| WSL2 nu pornește | Virtualizare dezactivată | Activați VT-x/AMD-V în BIOS |
| "Please enable Virtual Machine Platform" | Componentă Windows lipsă | `dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart` |
| WSL2 foarte lent | Resurse insuficiente | Editați `.wslconfig`, alocați mai multă memorie |
| "Kernel needs update" | Kernel WSL vechi | `wsl --update` |
| Ubuntu nu apare | Instalare incompletă | `wsl --install -d Ubuntu-22.04` |
| Rețea inaccesibilă | Configurare IP greșită | `wsl --shutdown` apoi reporniți |

### 28.2 Probleme Docker

| Problemă | Cauză posibilă | Soluție |
|----------|----------------|---------|
| "Cannot connect to Docker daemon" | Serviciu Docker oprit | `sudo service docker start` |
| "Permission denied" la docker.sock | Utilizator nu e în grup | `sudo usermod -aG docker $USER` apoi logout/login |
| "Port already in use" | Container/proces vechi | `docker ps -a` + `docker rm -f <container>` |
| Imagini nu se descarcă | Conexiune internet | Verificați DNS: `ping 8.8.8.8` |
| Container-ul cade imediat | Eroare în aplicație | `docker logs <container>` |
| Spațiu insuficient | Imagini/volume vechi | `docker system prune -a` |

### 28.3 Probleme Portainer

| Problemă | Cauză posibilă | Soluție |
|----------|----------------|---------|
| Nu pot accesa localhost:9000 | Container oprit | `docker start portainer` |
| "Portainer already initialized" | Timeout 5 minute depășit | Ștergeți și recreați (vezi mai jos) |
| Parolă uitată | N/A | Recreați containerul |

**Recrearea Portainer:**
```bash
docker stop portainer
docker rm portainer
docker volume rm portainer_data
docker volume create portainer_data
docker run -d -p 9000:9000 -p 9443:9443 --name portainer --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest
```

### 28.4 Probleme Wireshark

| Problemă | Cauză posibilă | Soluție |
|----------|----------------|---------|
| Nu se văd interfețe | Npcap lipsă | Reinstalați Wireshark cu Npcap |
| "vEthernet (WSL)" lipsește | WSL nu rulează | Porniți Ubuntu (`wsl`) apoi reporniți Wireshark |
| Nu se capturează trafic | Interfață greșită | Selectați "vEthernet (WSL)" |
| "Permission denied" | Drepturi insuficiente | Rulați Wireshark ca Administrator |

### 28.5 Probleme Python

| Problemă | Cauză posibilă | Soluție |
|----------|----------------|---------|
| "Module not found" | Pachet neinstalat | `pip install <pachet> --break-system-packages` |
| "externally-managed-environment" | Policy Python modern | Adăugați `--break-system-packages` |
| Versiune Python greșită | Python vechi | `sudo apt install python3.11` |
| Import scapy eșuează | Dependențe lipsă | `sudo apt install python3-scapy` |

---

## 29. Comenzi esențiale — Fișă de referință rapidă

### 29.1 Comenzi WSL (PowerShell)

```powershell
# Status WSL
wsl --status

# Lista distribuții
wsl -l -v

# Oprire toate instanțele
wsl --shutdown

# Pornire Ubuntu
wsl -d Ubuntu-22.04

# Actualizare kernel
wsl --update

# Setare versiune implicită
wsl --set-default-version 2
```

### 29.2 Comenzi Docker

```bash
# Informații sistem
docker info
docker version

# Containere
docker ps                    # Active
docker ps -a                 # Toate
docker start <container>     # Pornire
docker stop <container>      # Oprire
docker rm <container>        # Ștergere
docker logs <container>      # Log-uri
docker exec -it <c> bash     # Shell în container

# Imagini
docker images                # Lista
docker pull <image>          # Descărcare
docker rmi <image>           # Ștergere

# Rețele
docker network ls            # Lista
docker network inspect <n>   # Detalii

# Curățare
docker system prune -a       # Totul neutilizat
docker volume prune          # Volume neutilizate
```

### 29.3 Comenzi Docker Compose

```bash
# Pornire servicii
docker compose up -d

# Oprire servicii
docker compose down

# Status
docker compose ps

# Log-uri
docker compose logs -f

# Rebuild
docker compose build --no-cache

# Oprire cu ștergere volume
docker compose down -v
```

### 29.4 Comenzi rețea Linux

```bash
# Interfețe
ip addr show
ip link show
ip -br a                     # Format scurt

# Rutare
ip route show
ip route get 8.8.8.8

# Conexiuni
ss -tulpn                    # Porturi deschise
ss -t state established      # Conexiuni active

# Testare
ping -c 4 <host>
traceroute <host>
curl -I <url>

# DNS
dig <domain>
nslookup <domain>

# Captură
sudo tcpdump -i any -n
sudo tcpdump -i eth0 port 80 -w capture.pcap
```

### 29.5 Filtre Wireshark utile

```
# Protocol
tcp
udp
icmp
http
dns
tls

# Port
tcp.port == 80
udp.port == 53
tcp.dstport == 443

# IP
ip.addr == 192.168.1.1
ip.src == 10.0.0.1
ip.dst == 8.8.8.8

# TCP flags
tcp.flags.syn == 1
tcp.flags.rst == 1
tcp.flags.fin == 1

# Combinații
tcp.port == 80 && ip.addr == 192.168.1.1
http.request.method == "GET"
dns.qry.name contains "google"

# Handshake TCP
tcp.flags.syn == 1 && tcp.flags.ack == 0    # SYN
tcp.flags.syn == 1 && tcp.flags.ack == 1    # SYN-ACK
```

---

## 30. Licență

Acest proiect este licențiat sub **Licența MIT**.

```
MIT License

Copyright (c) 2025 Revolvix

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🎓 Succes la laborator!

Dacă ați parcurs acest ghid și ați configurat mediul corect, sunteți pregătiți să:

- ✅ Rulați experimente de rețea izolate cu containere Docker
- ✅ Capturați și analizați traficul de rețea cu Wireshark
- ✅ Gestionați containerele prin interfața web Portainer
- ✅ Automatizați sarcini de rețea cu Python
- ✅ Înțelegeți în profunzime cum funcționează protocoalele de rețea

---

> **by Revolvix**  
> Laborator Rețele de Calculatoare — ASE București, CSIE  
> Versiune documentație: Ianuarie 2025
