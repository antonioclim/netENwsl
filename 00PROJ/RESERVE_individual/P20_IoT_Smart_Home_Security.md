# Project 20: Network IoT for casă inteligentă – simulare and măsuri de security

> **Course:** Computer Networks 
> **Programme:** Economic Informatics, Year 3, Semester 2 
> **Institution:** ASE Bucharest - CSIE 
> **Project type:** Rezervă (individual)

---

## 📋 ASSESSMENT AND DELIVERY GUIDE

### ⚠️ IMPORTANT: In-Person Assessment

**Project assessment takes place EXCLUSIVELY at the faculty, with mandatory physical attendance.**

- The final presentation (Stage 4) takes place before the instructor/committee
- You must demonstrate understanding of the code and project architecture
- Questions about implementation and theoretical concepts may be asked
- Absence from presentation = project failure

---

### 📅 Stage Calendar

| Stage | Week | Deadline | Deliverables | Score |
|-------|-----------|----------|------------|---------|
| **S1** - Design | Week 5 | Week 5 (2026) | Specifications + Diagrams + Plan | 20% |
| **S2** - Prototype | Week 9 | Week 9 (2026) | Partial working implementation | 25% |
| **S3** - Final | Week 13 | Week 13 (2026) | Complete version + Documentation | 35% |
| **S4** - Presentation | Week 14 | Week 14 (2026) | Live demo + Oral defence | 20% |

**Intermediate checks (optional, for feedback):** Weeks 3, 6, 8, 11

---

### 🐙 GitHub Publication

**MANDATORY:** The project must be published on GitHub before each stage.

#### Your Repository

```
https://github.com/[username]/retele-proiect-20
```

#### Required Repository Structure

```
retele-proiect-20/
├── README.md # Descriere proiect, instrucțiuni rulare
├── docs/ # Documentație
│ ├── specificatii.md # [E1] Specificații tehnice
│ ├── diagrame/ # [E1] Diagrame arhitectură
│ ├── raport_progres.md # [E2] Raport etapa 2
│ └── documentatie_finala.md # [E3] Documentație completă
├── src/ # Cod sursă
│ ├── main.py # Punct de intrare
│ ├── modules/ # Module aplicație
│ └── utils/ # Utilitare
├── docker/ # Configurații Docker
│ ├── docker-compose.yml
│ ├── Dockerfile
│ └── configs/ # Fișiere configurare servicii
├── tests/ # Teste
│ ├── test_basic.py
│ └── expected_outputs/
├── artifacts/ # Output-uri (capturi, loguri)
│ └── screenshots/
├── MANIFEST.txt # Fișier semnătură (generat automat)
├── CHANGELOG.md # Istoric modificări
└── .gitignore
```

#### What to Publish at Each Stage

| Stage | Required files/folders on GitHub |
|-------|---------------------------------------|
| **S1** | `README.md`, `docs/specificatii.md`, `docs/diagrame/`, `.gitignore` |
| **S2** | + `src/` (partial working code), `docker/`, `docs/raport_progres.md` |
| **S3** | + `tests/`, `artifacts/`, `docs/documentatie_finala.md`, `CHANGELOG.md` |
| **S4** | Complete repository + tag `v1.0-final` |

#### Git Commands for Each Stage

```bash
# Etapa 1 - După ce ai pregătit specificațiile
git add docs/ README.md .gitignore
git commit -m "E1: Specificații și design inițial"
git push origin main

# Etapa 2 - După implementarea prototipului
git add src/ docker/ docs/raport_progres.md
git commit -m "E2: Prototip funcțional"
git push origin main

# Etapa 3 - Versiunea finală
git add tests/ artifacts/ docs/documentatie_finala.md CHANGELOG.md
git commit -m "E3: Versiune finală completă"
git tag -a v1.0-final -m "Versiune finală proiect"
git push origin main --tags

# Etapa 4 - Ultimele ajustări înainte de prezentare
git add .
git commit -m "E4: Pregătire prezentare"
git push origin main
```

---

### 📦 Archive Naming Convention

**Format:** `NUME_Prenume_GGGG_P20_TT.zip`

| Field | Description | Example |
|------|-----------|---------|
| NUME | Family name (UPPERCASE, no diacritics) | POPESCU |
| Prenume | First name (first letter capitalised) | Ion |
| GGGG | Group number (4 digits) | 1098 |
| P20 | Project number | P20 |
| TT | Deliverable type (S1-S4 or SXX) | E1 |

**Examples for this project:**
- `POPESCU_Ion_1098_P20_E1.zip` — Stage 1
- `POPESCU_Ion_1098_P20_E2.zip` — Stage 2
- `POPESCU_Ion_1098_P20_S07.zip` — Verification săptămâna 7

---

### 📊 Assessment Rubric

#### Stage 1 — Design (100 points)

| Criterion | Points | Description |
|----------|--------|-----------|
| Complete specifications | 30 | All requirements identified and documented |
| Architecture diagrams | 20 | Network topology, data flow, components |
| Implementation plan | 15 | Realistic timeline with milestones |
| Repository initialised | 15 | GitHub correctly configured with basic structure |
| Correct MANIFEST.txt | 10 | Valid signature |
| Archive naming | 10 | Follows convention |

#### Stage 2 — Prototype (100 points)

| Criterion | Points | Description |
|----------|--------|-----------|
| Partial functionality | 35 | Minimum 50% of functional requirements |
| Code quality | 25 | Clean, commented, structured |
| Docker configured | 15 | Functional Compose, containers start |
| Progress report | 10 | Documents what is done and what remains |
| MANIFEST.txt | 10 | Valid signature |
| On-time delivery | 5 | Meets deadline |

#### Stage 3 — Final Version (100 points + 10 bonus)

| Criterion | Points | Description |
|----------|--------|-----------|
| Complete functionality | 40 | All requirements implemented |
| Final code quality | 20 | Production-ready code |
| Teste | 15 | Unit and integration tests |
| Documentation | 10 | Complete README, code comments |
| Comparative analysis | 5 | Comparison with alternatives |
| MANIFEST.txt | 10 | Valid signature |
| **Extension bonus** | +10 | Additional features (3-person teams) |

#### Stage 4 — Presentation (100 points)

| Criterion | Points | Description |
|----------|--------|-----------|
| Working live demo | 35 | Application runs and demonstrates requirements |
| Technical presentation | 25 | Explains architecture and decisions |
| Answers to questions | 20 | Demonstrates deep understanding |
| Team contribution | 15 | Each member knows all the code |
| Time compliance | 5 | 10-15 minutes per team |

---

### 👥 Team Size

| Team | Requirements |
|--------|---------|
| **1 person** | Complete basic functionality |
| **2 persons** | + Extended testing + Detailed documentation |
| **3 persons** | + Advanced extensions + Performance analysis |

---

## 📚 PROJECT DESCRIPTION

Descriere: Proiectul își propune realizarea unei simulări de casă inteligentă (smart home) using dispozitive IoT (Internet of Things) and assessment aspectelor de security asociate. Studenții vor crea, în Cisco Packet Tracer (or mediu similar), o mică network IoT ce include senzori and actuatori (for example: un senzor de temperatură, un senzor de mișcare, o cameră IP, o lumină inteligentă or o yală inteligentă), interconectate printr-un hub / gateway IoT towards network locală and Internet. Dispozitivele IoT vor fi programate să comunice – de pildă, senzorul de mișcare detectează prezența and trimite un semnal which aprinde automat lumina. Simularea va evidenția protocoalele folosite de dispozitive (HTTP, MQTT etc.) and modules în which datele has transmise în network. A doua componentă majoră a project is security: se vor analiza riscurile de security într-o thus de network (comunicații necriptate, dispozitive neautentificate, network Wi-Fi vulnerabilă) and se vor implementa măsuri de protecție de bază. De example, se va activa criptarea WPA2 pe network Wi-Fi folosită de dispozitivele IoT, se va folosi un canal securizat (HTTPS/MQTTS) for comunicarea datelor senzorilor towards server central and se vor configura passwords puternice for accesul la dispozitive. Proiectul combină thus cunoștințele de rețelistică cu noțiuni moderne de IoT and security, oferind o perspectivă integratoare asupra aplicării rețelelor în mediul smart home.

### 🎯 Learning Objectives


### 📖 Key Concepts


### 🛠️ Technologies and Tools

Legătura cu weeks and kiturile: Proiectul sintetizează tema din săptămâna 13 (IoT and security în networks). În curs, la final, s-have discutat conceptele IoT and provocările de security, iar this project le materializează într-un example concret. La laboratorul final (săptămâna 13) probabil studenții have văzut demonstrații or have lucrat cu dispozitive IoT în Packet Tracer, ori have analizat security unor services IoT. Kitul de laborator aferent (ex. un file Packet Tracer cu câteva device-uri IoT configurate minimal) va servi ca point de plecare, pe which studenții îl vor extinde adăugând propriile automatizări and configurări de security. Proiectul is un capstone ce reunește cunoștințe din multiple arii: networks wireless (capitolul de legătură de date and Wi-Fi), protocols de nivel application (HTTP/REST – capitolele 10-12) and security (ultimul capitol), aplicându-le asupra IoT, un domeniu de actualitate. Thus, studenții vor vedea aplicabilitatea concretă a conceptelor în implementation unei case inteligente sigure.
Structura pe 4 stages: 1. Stage 1: Proiectarea scenariului IoT and a network. Se începe through definirea cazului de utilizare: for example, monitorizarea and controlul automat al unei case inteligente. Echipa decide ce dispozitive IoT să includă and ce reguli de automatizare vor implementa. Se desenează o schiță a network: casa va have un router/gateway which oferă connection la internet (simulat) and un Home Gateway IoT la which se conectează senzorii and actuatoarele (în Packet Tracer, Home Gateway-ul can fi un device dedicat which comunică wireless cu device-urile IoT). Se va stabili modules de conectare: se prevede o network Wi-Fi la which se conectează camerele IP and alte device-uri, iar cele IoT can folosi protocol propriu (PT has concept de IoT Network over wireless). Totodată, se identifică potențiale riscuri de security din design and se notează unde se vor aplica măsuri (ex: connection Wi-Fi – va fi securizată, accesul remote – va fi restricționat). La finalul acestei stages există un plan clar cu lista dispozitivelor (ex: 1 senzor de ușă, 1 senzor de mișcare, 1 cameră, 1 bec inteligent, 1 hub IoT, 1 router), protocoalele de comunicație for each and obiectivele de security. 2. Stage 2: Implementation în simulator a network and funcționalității IoT. Echipa construiește topology în Cisco Packet Tracer conform designului. Se configurează routerul main al casei (adresare IP, DHCP for dispozitive, activare Wi-Fi AP). Se plasează Home Gateway-ul IoT and dispozitivele IoT (senzori, actuatori) and se conectează la network (în PT, de obicei senzorii se conectează wireless la Home Gateway pe o network IoT distinctă, iar Home Gateway se conectează la routerul main). Se implementează logica IoT: for example, în PT, for un senzor de mișcare and o lampă, se can folosi Physical Workspace and Programming – se accesează interfața senzorului and se creează o asociere: “if MotionDetector detectează = true, then trimite mesaj de ON la SmartLamp”. Se configurează camera IP cu o address IP din LAN and se simulează streaming-ul (deși PT nu arată video, putem considera service activ pe port). La this stage, team se asigură că din point de vedere functional sistemul merge: if se declanșează senzorul, lumina se aprinde (PT vizualizează asta), if se accesează interfata camerei (via IP) se primește un răspuns etc. Comunicarea towards un server extern (if există de ex. un service cloud) se can simula through trimiterea datelor senzorilor la un IoT Server (PT has un IoT cloud server configurabil) – for example, Home Gateway transmite datele towards un server central (acesta putând fi un PC server din internet). 3. Stage 3: Implementarea and testing măsurilor de security. Odată functional sistemul, se trece la securizarea lui. Se configurează network Wi-Fi a casei cu WPA2-PSK: se setează o password puternică and se reconectează device-urile Wi-Fi using this password (PT permite setarea securității pe modulul wireless). Se verifică că un dispozitiv neautorizat (adăugat de test în apropiere) nu se can conecta without cheie. Then, se asigură că comunicațiile IoT sensibile has criptate: for example, if Home Gateway transmite datele senzorilor la un server extern, se optează for un protocol securizat – if initial era HTTP, se schimbă la HTTPS (în simulare se can presupune, even if PT nu simulează complete TLS, se can folosi un server ce acceptă numai connections pe port SSL). If se folosește MQTT, se can menționa MQTT peste TLS (MQTTS) – PT however nu detaliază asta, but se can explica teoretic în documentation. Totodată, se setează credențiale pe dispozitive: for example, camera IP – se configurează un username/password for acces (if PT permite), Home Gateway – se schimbă parola implicită de admin. Echipa va simula and potențiale atacuri: for example, va încerca o captură de packets Wi-Fi (PT can arăta că datele has criptate and so neinteligibile) or va încerca să se conecteze la Home Gateway without autorizare (eșuând). Se vor documenta these teste ca dovadă că măsurile implementate have efect. Tot în this stage, se can configura reguli de bază de firewall pe routerul main al casei (ex: blocarea accesului din internet towards dispozitivele IoT, permițând only connections inițiate din LAN). 4. Stage 4: Documentare and prezentarea concluziilor. În raportul final, se descrie arhitectura sistemului IoT realizat, cu diagrame which evidențiază conexiunile among componente. Se explică funcționalitatea (ce makes each senzor, ce acțiuni automatizate have loc) and se menționează protocoalele folosite. Then, un accent important al documentației is pe analiza de security: se enumeră vulnerabilitățile identificate initial and se descrie for each ce contramăsură s-a aplicat. De example: “Traficul initial al senzorului era necriptat HTTP, susceptibil la interceptare – am rezolvat using HTTPS for transmiterea datelor.”, “Network wireless era initial deschisă – am activat WPA2 cu o password complexă.”, “Camera IP have credențiale default – le-am schimbat and am restricționat accesul din exterior through firewall.”. Se can include capturi din simulare, cum ar fi configurațiile de security or rezultate ale testelor (ex: un ping din afara network towards un dispozitiv IoT blocat de firewall). În concluzii, team va discuta importanța securității în IoT, evidențiind cât de ușor can fi compromise thus de sisteme if has lăsate nesecurizate and cum măsurile luate îmbunătățesc semnificativ postura de security. Totodată, se can menționa soluții adiționale ce depășesc sfera project (ex: networks separate for IoT, monitorizarea traficului IoT for anomalii, actualizarea firmware-ului dispozitivelor periodic etc.), arătând o viziune complete asupra problemei.

### 📖 Key Concepts


### ❓ ÎNTREBĂRI FRECVENTE - MEDIU DE LUCRU

Q: WSL won't start or is very lent
A: Verificări recomandate:
 - Virtualizarea e activată în BIOS
 - Rulați: wsl --update
 - Alocați mai multă memorie în .wslconfig

Q: Cum accesez fișierele Windows din WSL Ubuntu?
A: Are montate în /mnt/:
 - /mnt/c/ for C: - /mnt/d/ for D:
Q: Comenzile docker nu funcționează
A: Verificați:
 - docker --version (instalat corect?)
 - Docker Desktop e pornit (pe Windows)
 - Userul e în grupul docker: sudo usermod -aG docker $USER


### 📚 Bibliografie

Riahi Sfar, A., Natalizio, E., Challal, Y., & Chtourou, Z. (2018). A roadmap for security challenges in the Internet of Things. Digital Communications and Networks, 4(2), 118–137. DOI: 10.1016/j.dcan.2017.04.003
Sebestyen, H., & Popescu, D. E. (2025). A Literature Review on Security in the Internet of Things: Identifying and Analysing Critical Categories. Computers, 14(2), 61. DOI: 10.3390/computers14020061
[1] TXT - » RFC Editor
https://www.rfc-editor.org/refs/ref3022.txt
[2] [3] [PDF] RFC 7857 - Updates to Network Address Translation †NAT ...
https://people.computing.clemson.edu/~jmarty/courses/commonCourseContent/Module5-NetworkConceptsAppliedToLinuxNetworkProgramming/AdditionalMaterial/rfc7857.pdf
[4] Foundations of Python network programming | WorldCat.org
https://search.worldcat.org/it/title/Foundations-of-Python-network-programming/oclc/894116307
[5] Staff View: Foundations of Python Network Programming
https://psnz.umt.edu.my/seal/Record/978-1-4302-5855-1/Details
[6] Machine Learning and Port Scans: A Systematic Review - arXiv
https://arxiv.org/abs/2301.13581
[7] A Survey on different Port Scanning Methods and the Tools used to ...
https://www.semanticscholar.org/paper/A-Survey-on-different-Port-Scanning-Methods-and-the-Upadhya/89b68de41599859989a7564091b6df7f8f03bd2e
---

## 🔮 Verification înțelegere — IoT and MQTT

Before de testing:

1. **Cine primește mesajul publicat pe "casa/living/temp"?**
 - Toți clienții abonați la this topic or "casa/living/#"

2. **Ce se întâmplă if broker-ul MQTT nu rulează?**
 - Eroare: Connection refused

3. **Ce QoS folosim for date critice?**
 - QoS 2 (Exactly once)


---

## ❓ Frequently Asked Questions

**Q: WSL won't start or e lent** 
A: Verifică virtualizarea în BIOS and rulează `wsl --update`

**Q: Cum accesez fișierele Windows din WSL?** 
A: Are în `/mnt/c/`, `/mnt/d/` etc.

**Q: Docker nu funcționează** 
A: Verifică: `docker --version`, Docker Desktop pornit, user în grupul docker


---


---

## 🔗 JAVASCRIPT → PYTHON TRANSITION

You have solid experience in JavaScript from the Web Technologies course. Here's how concepts translate to Python for networking:

### Basic Equivalences

| JavaScript (TW) | Python (Networks) | Note |
|-----------------|-----------------|------|
| `const fn = (x) => x * 2` | `fn = lambda x: x * 2` | Arrow functions → lambda |
| `arr.map(x => x * 2)` | `[x * 2 for x in arr]` | List comprehension is more Pythonic |
| `arr.filter(x => x > 0)` | `[x for x in arr if x > 0]` | Or `filter()` |
| `arr.reduce((a,b) => a+b, 0)` | `sum(arr)` or `functools.reduce()` | Python has `sum()` built-in |
| `JSON.parse(str)` | `json.loads(str)` | JSON parsing |
| `JSON.stringify(obj)` | `json.dumps(obj)` | JSON serialisation |
| `async/await` | `async/await` cu `asyncio` | Syntax is similar! |
| `fetch(url)` | `requests.get(url)` | Or `aiohttp` for async |
| `Buffer.from(str)` | `str.encode('utf-8')` | Text → bytes conversion |
| `buf.toString()` | `bytes.decode('utf-8')` | Bytes → text conversion |

### Servere: Express.js vs Python

```javascript
// Express.js (TW)
const express = require('express');
const app = express();

app.get('/api/data', (req, res) => {
 res.json({ message: 'Hello' });
});

app.listen(3000);
```

```python
# Flask (Python)
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/api/data')
def get_data():
 return jsonify({'message': 'Hello'})

app.run(port=3000)
```

### Async: Promises vs asyncio

```javascript
// JavaScript async (TW)
async function fetchData() {
 const response = await fetch(url);
 const data = await response.json();
 return data;
}
```

```python
# Python asyncio
import aiohttp
import asyncio

async def fetch_data():
 async with aiohttp.ClientSession() as session:
 async with session.get(url) as response:
 data = await response.json()
 return data
```

### Sockets: Node.js vs Python

```javascript
// Node.js net module
const net = require('net');
const client = net.createConnection({ port: 8080 }, () => {
 client.write('Hello');
});
client.on('data', (data) => console.log(data.toString()));
```

```python
# Python socket
import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 8080))
client.send(b'Hello')
data = client.recv(1024)
print(data.decode())
```


### 💡 For MQTT and IoT

MQTT e similar cu WebSockets pe which le-ai folosit can în TW:

```python
# WebSocket (TW) vs MQTT (Rețele)

# WebSocket: conexiune bidirecțională client-server
# MQTT: publish/subscribe prin broker

import paho.mqtt.client as mqtt

# Similar cu socket.on('message', callback) din Socket.IO
def on_message(client, userdata, msg):
 print(f"Topic: {msg.topic}, Message: {msg.payload.decode()}")

client = mqtt.Client()
client.on_message = on_message

# Similar cu socket.emit() dar prin broker
client.connect("localhost", 1883)
client.subscribe("casa/living/temp") # Similar cu socket.join('room')
client.publish("casa/living/temp", "22.5") # Similar cu io.to('room').emit()
```


### 💡 For Security and Encryption

Din TW ai folosit HTTPS and can crypto în Node.js:

```python
# Node.js crypto → Python cryptography

# Criptare simetrică (AES)
from cryptography.fernet import Fernet
key = Fernet.generate_key()
cipher = Fernet(key)
encrypted = cipher.encrypt(b"mesaj secret")

# Hash (similar cu crypto.createHash în Node)
import hashlib
hash_obj = hashlib.sha256(b"password")
hash_hex = hash_obj.hexdigest()

# În Express aveai middleware pentru autentificare
# În Python implementezi manual sau folosești biblioteci
```

---

## 📚 RELEVANT LABORATORY MATERIALS

Consultă these resurse din arhiva **netROwsl** for conceptele necesare:


### 📁 `13roWSL/` — IoT and Security

**What you'll find relevant:**
- Dispozitive IoT, security, authentication

**Recommended files:**
- `13roWSL/README.md` — overview and laboratory steps
- `13roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `13roWSL/docs/fisa_comenzi.md` — useful commands
- `13roWSL/src/` — Python code examples
- `13roWSL/homework/` — similar exercises


### 📁 `03roWSL/` — Multicast

**What you'll find relevant:**
- Comunicare between dispozitive

**Recommended files:**
- `03roWSL/README.md` — overview and laboratory steps
- `03roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `03roWSL/docs/fisa_comenzi.md` — useful commands
- `03roWSL/src/` — Python code examples
- `03roWSL/homework/` — similar exercises


### 📁 `10roWSL/` — REST

**What you'll find relevant:**
- API-uri for control dispozitive

**Recommended files:**
- `10roWSL/README.md` — overview and laboratory steps
- `10roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `10roWSL/docs/fisa_comenzi.md` — useful commands
- `10roWSL/src/` — Python code examples
- `10roWSL/homework/` — similar exercises


### 📁 `00-startAPPENDIX(week0)/PYTHON ghid de auto-perfectionare/`

**Resources for Python networking:**
- `GHID_PYTHON_NETWORKING_RO.md` — complete Python guide for networking
- `cheatsheets/PYTHON_RAPID.md` — quick syntax reference
- `examples/01_socket_tcp.py` — TCP sockets example
- `examples/02_bytes_vs_str.py` — working with bytes (important!)
- `examples/03_struct_parsing.py` — binary data parsing


### 📁 `00-startAPPENDIX(week0)/00CURS/`

**Theoretical materials:**
- HTML presentations for each week (S1-S14)
- In-depth concepts for the exam


## 📝 Final Notes

- **Always verify** că the GitHub repository is updated before the deadline
- **Test** the application on a clean computer before presentation
- **Prepare** answers for questions about architecture and code
- **Communicate** with the team to coordinate contributions

---

*Last update: 23 January 2026* 
*Computer Networks — ASE Bucharest*
