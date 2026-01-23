# 📚 Projects Computer Networks

> **Course:** Computer Networks 
> **Programme:** Economic Informatics, Year 3, Semester 2 
> **Institution:** Academia de Studii Economice București - CSIE 
> **Semestru:** 2025-2026

---

## 📋 Cuprins

This repository conține **20 de projects** for disciplina Computer Networks, organizate în două categorii:

### 🎯 [PROIECTE/](PROIECTE/) — Projects principale (P01-P15)

Projects complete for teams de 1-3 students.

| Nr. | Project | Tehnologii |
|-----|---------|------------|
| P01 | [Firewall SDN Mininet](PROIECTE/P01_Firewall_SDN_Mininet.md) | Mininet, OpenFlow, POX/Ryu |
| P02 | [Network Hibridă Mininet Docker](PROIECTE/P02_Retea_Hibrida_Mininet_Docker.md) | Mininet, Docker, Python |
| P03 | [IDS Monitorizare Traffic](PROIECTE/P03_IDS_Monitorizare_Trafic_Python.md) | Python, Scapy, Threading |
| P04 | [Mesagerie Securizată](PROIECTE/P04_Mesagerie_Securizata_Client_Server.md) | Python, AES/RSA, Sockets |
| P05 | [Protocol Rutare Personalizat](PROIECTE/P05_Protocol_Rutare_Personalizat.md) | Python, Distance Vector/Link State |
| P06 | [SDN Controller OpenFlow](PROIECTE/P06_SDN_Mininet_Controller_OpenFlow.md) | Mininet, OpenFlow, Python |
| P07 | [Firewall IDS Software](PROIECTE/P07_Firewall_IDS_Monitorizare_Trafic.md) | Python, iptables, Logging |
| P08 | [Server Web Proxy Invers](PROIECTE/P08_Server_Web_Proxy_Invers.md) | Python, HTTP, Nginx |
| P09 | [Server FTP Multi-Client](PROIECTE/P09_Server_FTP_Multi_Client.md) | Python, FTP, Docker |
| P10 | [Orchestrare DNS SSH FTP](PROIECTE/P10_Orchestrare_DNS_SSH_FTP_Docker.md) | Docker Compose, BIND, vsftpd |
| P11 | [SDN Advanced OpenFlow](PROIECTE/P11_SDN_Avansat_Mininet_OpenFlow.md) | Mininet, OpenFlow, QoS |
| P12 | [Microservicii Load Balancing](PROIECTE/P12_Microservicii_Docker_Load_Balancing.md) | Docker, Nginx, HAProxy |
| P13 | [Application Distribuită RPC](PROIECTE/P13_Aplicatie_Distribuita_RPC.md) | gRPC/JSON-RPC, Docker |
| P14 | [Security IDS IPS](PROIECTE/P14_Securitate_IDS_IPS_Simulare.md) | Snort/Suricata, Python |
| P15 | [IoT Edge Computing MQTT](PROIECTE/P15_IoT_Edge_Computing_MQTT.md) | MQTT, Mosquitto, Docker |

### 📦 [REZERVA_individual/](REZERVA_individual/) — Projects rezervă (P16-P20)

Projects mai simple, for lucru individual or cazuri speciale.

| Nr. | Project | Tehnologii |
|-----|---------|------------|
| P16 | [Analiza HTTP Wireshark](REZERVA_individual/P16_Analiza_HTTP_Wireshark.md) | Wireshark, HTTP |
| P17 | [Network LAN NAT DHCP](REZERVA_individual/P17_Retea_LAN_NAT_DHCP.md) | Cisco Packet Tracer |
| P18 | [Chat TCP Client Server](REZERVA_individual/P18_Chat_TCP_Client_Server.md) | Python, Sockets TCP |
| P19 | [Scanner Porturi Security](REZERVA_individual/P19_Scanner_Porturi_Securitate.md) | Python, Sockets |
| P20 | [IoT Casă Inteligentă](REZERVA_individual/P20_IoT_Casa_Inteligenta_Securitate.md) | Packet Tracer, IoT |

---

## ⚠️ IMPORTANT: Reguli de assessment

### 1. Prezența fizică mandatory

**Evaluarea project se makes EXCLUSIV la facultate!**

- Prezentarea final (Stage 4) necesită prezență fizică
- Each member al echipei must să demonstreze că înțelege code
- Întrebări din implementation and teorie has posibile
- **Absence from presentation = project failure**

### 2. GitHub mandatory

Each project must publicat pe GitHub:

```
https://github.com/[username]/retele-proiect-XX
```

Structura repository-ului and ce se postează la each stage has detaliate în file fiecărui project.

### 3. Calendarul etapelor

| Stage | Week | Deliverables | Score |
|-------|-----------|------------|---------|
| **S1** - Design | Week 5 | Specificații + Diagrame | 20% |
| **S2** - Prototype | Week 9 | Implementation parțială | 25% |
| **S3** - Final | Week 13 | Versiune complete | 35% |
| **S4** - Presentation | Week 14 | Demo live | 20% |

---

## 🛠️ Mediul de lucru

### Configurația standard

```
Windows 11 → WSL2 → Ubuntu 22.04 → Docker Engine → Portainer CE
```

### Credențiale implicite

| Service | Utilizator | Password |
|----------|------------|--------|
| Ubuntu WSL | `stud` | `stud` |
| Portainer | `stud` | `studstudstud` |

### Points de acces

| Service | URL |
|----------|-----|
| Portainer | http://localhost:9000 |
| Servicii laborator | Variază (8080, 8081, etc.) |

---

## 📖 Cum să începi

1. **Alege un project** din lista de mai sus
2. **Citește file** project ales for requirements detaliate
3. **Creează repository** pe GitHub conform structurii indicate
4. **Urmează calendarul** etapelor and postează progresul
5. **Pregătește prezentarea** for assessment final

---

## 📚 Resurse adiționale

- **Materialele de laborator:** Folderele `{NN}roWSL` din repository-ul cursului
- **Documentația Docker:** https://docs.docker.com
- **Documentația Mininet:** http://mininet.org
- **Tutoriale Wireshark:** https://www.wireshark.org/docs/

---

## 📝 Convenția de denumire arhive

**Format:** `NUME_Prenume_GGGG_PXX_TT.zip`

| Field | Description | Example |
|------|-----------|---------|
| NUME | Nume familie (MAJUSCULE) | POPESCU |
| Prenume | Prenume (prima literă mare) | Ion |
| GGGG | Număr grupă | 1098 |
| PXX | Număr project | P05 |
| TT | Stage (E1-E4) or week (S07) | E2 |

**Example:** `POPESCU_Ion_1098_P05_E2.zip`

---

*Computer Networks — ASE Bucharest — Semester 2, 2025-2026* 
*Last update: Ianuarie 2026*
