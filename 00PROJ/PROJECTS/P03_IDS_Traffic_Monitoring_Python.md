# Project 03: Monitorizarea traficului and detectarea intruziunilor cu Python

> **Course:** Computer Networks 
> **Programme:** Economic Informatics, Year 3, Semester 2 
> **Institution:** ASE Bucharest - CSIE 
> **Project type:** Main

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
https://github.com/[username]/retele-proiect-03
```

#### Required Repository Structure

```
retele-proiect-03/
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

**Format:** `NUME_Prenume_GGGG_P03_TT.zip`

| Field | Description | Example |
|------|-----------|---------|
| NUME | Family name (UPPERCASE, no diacritics) | POPESCU |
| Prenume | First name (first letter capitalised) | Ion |
| GGGG | Group number (4 digits) | 1098 |
| P03 | Project number | P03 |
| TT | Deliverable type (S1-S4 or SXX) | E1 |

**Examples for this project:**
- `POPESCU_Ion_1098_P03_E1.zip` — Stage 1
- `POPESCU_Ion_1098_P03_E2.zip` — Stage 2
- `POPESCU_Ion_1098_P03_S07.zip` — Verification săptămâna 7

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

Detailed Description
This project vizează realizarea unui sistem simplificat de monitorizare a traficului de network combinat cu elemente de IDS (Intrusion Detection System), using instrumente software and scripturi Python. Studenții vor dezvolta o application capabilă să captureze packets într-o network locală (or să proceseze files capturate) and să le analizeze for a identifica tipare suspecte or activități malițioase de tip atac informatic. Practic, project constă în două componente principale: (1) un modules de captură and înregistrare a traficului de network (for example using biblioteca pcapy or scapy în Python, ori through interfata tshark/Wireshark) and (2) un modules de detecție a anomaliilor bazat pe those capturi (using reguli simple or praguri prestabilite).
Scenariile de atac ce can fi detectate de sistemul propus includ, for example, un scan de ports (caracterizat de un număr mare de connections towards ports diferite într-un interval scurt), un posibil atac de tip DoS (un val intens de packets ICMP Echo Request – ping – towards o țintă) or traffic ce indică o tentativă de acces neautorizat (for example, multiple încercări de authentication eșuate într-un protocol). Echipa va defini un set de semnături or euristici simple for thus de evenimente and va implementa logica în Python: pe măsură ce pachetele has procesate, scriptul va genera alerte if is depășit un anumit prag (ex: >100 de connections pe secundă de la aceeași sursă) or if apar tipare cunoscute (ex: un string specific într-un payload which corespunde unui exploit). Rezultatul va fi un tool de monitorizare which can afișa statistici de traffic în timp real and raporta alerte de security, demonstrând conceptele de bază ale unui sistem de detecție a intruziunilor.

### 🎯 Learning Objectives

Familiarizarea cu captura de traffic la nivel de packets în network and formatele de stocare (PCAP), alături de instrumente precum tcpdump or Wireshark for inspecția traficului.

### 🛠️ Technologies and Tools

Înțelegerea conceptelor de bază din security rețelelor, cum ar fi tipurile de atacuri (scanare, DoS, brute-force) and definirea de heuristici de detecție for acestea.
Dezvoltarea abilităților de a proiecta un sistem de monitorizare: colectare de date, procesare în timp real (or aproape real), generare de log-uri/alerte and prezentarea informației într-un mod util.
Conștientizarea limitărilor unui IDS simple and a conceptului de rată de alarme fals pozitive vs. fals negative, precum and a importanței ajustării pragurilor de detecție.

### 📖 Key Concepts

Protocoale de network and formate de packets – structură de packets Ethernet, IP, TCP/UDP, ICMP; interpretarea header-elor (addresses, ports, flag-uri) din perspective de security.
Analiza traficului – metrici de traffic (număr de packets, byte transferați, sesiuni active), distribuții pe protocols/ports; folosirea filtrării BPF (Berkeley Packet Filter) for a selecta packets relevante.
Detecția intruziunilor – semnături vs. detecție pe bază de anomalii; examples de semnături simple (ex: secvență de bytes specifici într-un payload ce indică un exploit cunoscut) and examples de anomalii (traffic voluminos atipic).
Security network – tipuri de atacuri comune (scanare ports, Ping flood, SYN flood, atacuri la nivel application) and impactul lor asupra network; mecanisme defensive (IDS/IPS, firewall) and locul unui IDS în infrastructură.
Programare Python advanced – lucru cu packets binare, structuri de date eficiente for contorizare (dicționare for numărarea conexiunilor per IP, for example), programare orientată eveniment (captură continuă de packets).
Technologies Involved
Limbajul Python – limbaj main for implementation; se vor folosi modules third-party specializate:
Scapy – bibliotecă puternică for manipularea pachetelor (can captura, construi and interpreta packets de la nivel link până la application).
Pcapy/dpkt – biblioteci alternative bazate pe libpcap for captură raw de packets.
Wireshark/Tshark – instrument grafic (Wireshark) or linie de comandă (tshark) for capturarea and inspectarea traficului, utilizat for validarea funcționării (de ex., compararea rezultatelor scriptului Python cu cele capturate de Wireshark).
Linux – se va folosi un mediu Linux for acces la interfața de network în modules promiscuu. Utilitare precum tcpdump can fi folosite la nevoie for a genera files PCAP ce vor fi analizate offline de script.
Network de test – se can folosi fie network locală reală (în limite sigure) for a genera traffic (ex: scanare de ports cu nmap pe un host de test), fie o network virtuală izolată (ex: 2-3 VM-uri în VirtualBox/Mininet) unde să se lanseze atacuri simulate.
Biblioteci de logare and alertare – ex: modules Python for log (logging) or even email/SMS (if se dorește trimiterea alertelor într-un anumit format).
Connection to Weekly Course Topics
Week 7: Transport (TCP/UDP) – interpretarea flag-urilor TCP (SYN, FIN, etc.) is esențială for a detecta anumite atacuri (ex: scanare TCP SYN); conceptele studiate la curs ajută la recunoașterea comportamentelor anormale în secvențele TCP.
Week 9: Securitatea rețelelor – project se bazează direct pe noțiunile de atac and apărare discutate în cursul din sapt. 9 (vezi prezentarea „Introducere IDS and IPS” din arhiva WEEK9, which oferă context teoretic).
Week 12: Programare de network în Python – se aplică practic cunoștințele de scripting de network din lab. Week12 („Packet Sniffing cu Python” din arhivă), extinzându-le cu logică de detecție a intruziunilor.
Week 8: Protocoale de application – anumite atacuri țintesc nivelul application (ex: HTTP flood), so înțelegerea modului în which funcționează protocoalele de application (discutate în curs) can ajuta la interpretarea traficului capturat.
Etapele project

### 📋 Stage 1 (Week 5) – Documentare and definire specificații: Cercetarea tipurilor de atacuri de network ce can fi detectate cu metode simple and alegerea a 2-3 tipare de detectat (for example: scanare de ports, ICMP flood, authentication eșuată repetată pe FTP). Se stabilește metodologia: captura în timp real vs. offline (din file), instrumentele ce vor fi folosite (ex: scapy for captura live). Livrabil: un plan de project ce conține lista de scenarii de atac ce vor fi detectate, for each specificându-se ce metrică or semnătură va fi folosită (ex: “scanare ports – criterion: >20 de ports distincte accesate de același IP sursă în < 1 minut”). Totodată, se va pregăti mediul de lucru: instalarea bibliotecilor necesare (scapy etc.) and eventual scrierea unui script Python minimal which să captureze packets and să afișeze câteva informații (ca proof-of-concept). Codul initial se încarcă în repository.


### 🔨 Stage 2 (Week 9) – Dezvoltare componentă de captură and monitorizare: Implementarea modulului which colectează traffic and calculează statisticile necesare. De example, se can realiza un sniffer which rulează pe o interfață de network and înregistrează pachetele într-o structură de date. Se vor folosi dicționare or contori for a ține evidența numărului de connections/packets per address IP sursă, per port destinație etc., în timp real. Se implementează afișarea periodică (ex: la each 5 secunde) a unor statistici sumare pe consolă (traffic total, top 5 addresses sursă after număr de packets, etc.). Livrabil: code Python actualizat în repository, cu funcționalitatea de sniffing and monitorizare de bază completată, plus un scurt report/intermediar or capturi de ecran which demonstrează rularea sniffer-ului pe o network de test (de ex., se pornește scriptul and se execută un ping de test, iar scriptul loghează pachetele ICMP observate).


### 🔮 VERIFICARE ÎNȚELEGERE - CONCEPTE REȚEA

Before de configuration, verificați că înțelegeți:

1. Ce tip de address is 192.168.1.50?
 → Address privată (RFC 1918), nu can fi rutată direct pe Internet

2. Câte addresses IP utilizabile has într-o network /24?
 → 254 addresses (256 total minus 1 for network minus 1 for broadcast)

3. Ce rol has NAT în network voastră?
 → Traduce adresele IP private în address publică for acces Internet


### ✅ Stage 3 (Week 13) – Dezvoltare componentă de detecție and alerte & testing final: Se integrează în script logica de detecție a intruziunilor conform specificațiilor stabilite. De example, se implementează o function which, la each interval, analizează datele colectate: if o anumită address IP has comunicări towards > X ports unice, se generează o alertă de tip “Possible port scan from IP ...”. Similar for celelalte tipare (DoS – pps peste prag, etc.). Alerta can fi sub formă de mesaj în consolă, log în file or notificare. Se vor genera then într-un mediu controlat trafice which să declanșeze these alerte (for example, using nmap for scanare or un script which makes multe connections). Se evaluează acuratețea: alertele apar când must and absența alertelor false la traffic normal. Livrabil: code sursă final (documentat, cu eventuale files de configuration for praguri), alături de un jurnal de testing detaliat. Jurnalul va descrie cum s-a simulat each scenariu de atac and if sistemul a detectat, incluzând fragmente de loguri/alerte generate. Se vor nota limitări (ex: “sistemul nu distinge between scanare and un program legitim which makes connections multiple – posibile alarme false”).


### 📊 PEER INSTRUCTION - CONCEPTE REȚEA

Discutați cu colegii and alegeți împreună răspunsul corect:

Întrebarea 1: Un dispozitiv has address IP 192.168.1.50. Ce tip de address is aceasta?

A) Address publică, rutabilă pe Internet
B) Address privată conform RFC 1918 ✓
C) Address de loopback
D) Address broadcast

Explicație: Range-uri private: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16. Acestea necesită NAT for acces Internet.

Întrebarea 2: Într-o network cu masca /24, câte addresses IP has disponibile for dispozitive?

A) 256 addresses
B) 254 addresses ✓
C) 255 addresses
D) 252 addresses

Explicație: /24 = 256 addresses totale. Scădem: 1 address de network (ex: .0) and 1 broadcast (ex: .255) = 254 utilizabile.


### 🎤 Stage 4 (Week 14) – Prezentare final: În cadrul prezentării, team va explica arhitectura soluției (modules de captură, modules de detecție), then va demonstra live funcționarea IDS-ului. De example, vor rula scriptul pe o interfață de network while un member execută un atac de test (cum ar fi un port scan), arătând cum alerta apare în consola aplicației. Se vor discuta pe scurt and idei de îmbunătățire (cum ar fi folosirea unor algoritmi de învățare automată for detecție advanced, deși neimplementați here). Livrabil: prezentarea (slides) and, optional, un set de files PCAP pregătite for demo (în cazul în which se preferă redarea offline a unui atac în locul execuției lui live, for consecvență).

Extensii posibile for teams de 3 vs. 2/1 students
O team de 3 students ar putea extinde considerabil project spre un IDS mai sofisticat. De pildă, ar putea implementa o interfață grafică simple (GUI web) which afișează în timp real grafic traffic and alertele, using un framework Python (Flask + chart libraries). Totodată, s-ar putea adăuga mai multe tipuri de detecții (ex: detecție de scanare DNS or de atacuri SQL injection la nivel de conținut, if se analizează payload-ul pachetelor). O altă extensie ar fi includerea unei componente de ** răspuns activ** – for example, la detectarea unui atac, scriptul să ruleze o comandă de blocare a IP-ului agresor (through configuration unui firewall local).
O team de 1-2 students se can limita la implementation nucleului functional: captură and una-două reguli de detecție de bază. De example, un project simplificat ar putea only să detecteze scanările de ports, without alte tipuri de atac. În plus, if implementation capturii live se dovedește complicată, team mică can alege să analizeze files PCAP capturate anterior, concentrându-se mai mult pe partea de analiză offline decât pe ingineria timp-real. Thus volumul de code scade, but obiectivele de învățare (analiza traficului and recunoașterea tiparelor) rămân atinse.

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

Scarfone, K., & Mell, P. (2007). Guide to Intrusion Detection and Prevention Systems (IDPS). NIST Special Publication 800-94. (Ghid exhaustiv oferit de NIST about conceptele and practicile IDS/IPS)
Sanders, C. (2010). Practical Packet Analysis: Using Wireshark to Solve Real-World Network Problems (2nd ed.). No Starch Press. (Carte orientată pe interpretarea pachetelor and traffic, utilă for partea de monitorizare and înțelegere a tiparelor de traffic)
Biondi, P. (2004). Scapy Project Documentation. Retrieved 2023, from https://scapy.readthedocs.io (Documentația oficială Scapy, incluzând tutoriale about sniffing and examples de utilizare a librăriei în scenarii de security)
Roesch, M. (1999). Snort - Lightweight Intrusion Detection for Networks. Proceedings of the 13th USENIX Conference on System Administration (LISA ’99), 229-238. (Lucrarea initial which prezintă Snort, un IDS open-source; oferă context about detectarea bazată pe semnături and performanța în timp real)
RFC 783 – Postel, J., & Reynolds, J. (1981). TFTP Protocol (Revision 2). IETF. (Example de protocol simple susceptibil la abuz; deși nu is adresat direct în project, RFC-ul ilustrează structurarea unui protocol, utilă când interpretăm payload-urile – referință optional for detalii de implementation protocolară)
---

## 🔮 Verification înțelegere — Networks

Before de configuration:

1. **Ce tip de address is 192.168.1.50?**
 - Address privată (RFC 1918)

2. **Câte addresses IP utilizabile has într-o network /24?**
 - 254 (256 - 1 network - 1 broadcast)

3. **Ce makes NAT?**
 - Traduce addresses private în publice for acces Internet

---

## 📊 Peer Instruction — Networks

**Întrebare:** Un dispozitiv has IP 192.168.1.50. Ce tip de address is?

- A) Address publică
- B) Address privată (RFC 1918) ✓
- C) Address loopback
- D) Address broadcast


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


### 💡 For Socket Programming

Din TW știi `fetch()` for HTTP. Now lucrezi la nivel mai jos:

```python
# Serverul tău de chat e similar cu Express, dar la nivel TCP
import socket
import threading

def handle_client(conn, addr):
 """Similar cu app.get('/route', handler) dar pentru conexiuni raw"""
 while True:
 data = conn.recv(1024) # Similar cu req.body
 if not data:
 break
 conn.send(data) # Similar cu res.send()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5000)) # Similar cu app.listen(5000)
server.listen(5)

while True:
 conn, addr = server.accept()
 # threading e similar cu async în conceptul de concurență
 threading.Thread(target=handle_client, args=(conn, addr)).start()
```


### 💡 For Programare Asincronă

Din TW cunoști async/await cu Promises. Python e similar:

```python
# JavaScript Promise → Python asyncio

# JS: const results = await Promise.all([fetch(url1), fetch(url2)]);
# Python:
results = await asyncio.gather(
 fetch_async(url1),
 fetch_async(url2)
)

# JS: setTimeout(() => {}, 1000)
# Python:
await asyncio.sleep(1)

# JS: .then().catch()
# Python: try/except în async function
```

---

## 📚 RELEVANT LABORATORY MATERIALS

Consultă these resurse din arhiva **netROwsl** for conceptele necesare:


### 📁 `07roWSL/` — Interceptarea and Filtrarea Pachetelor

**What you'll find relevant:**
- Captură and analiză packets cu Scapy/tshark

**Recommended files:**
- `07roWSL/README.md` — overview and laboratory steps
- `07roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `07roWSL/docs/fisa_comenzi.md` — useful commands
- `07roWSL/src/` — Python code examples
- `07roWSL/homework/` — similar exercises


### 📁 `13roWSL/` — IoT and Security

**What you'll find relevant:**
- Detectarea intruziunilor, pattern matching

**Recommended files:**
- `13roWSL/README.md` — overview and laboratory steps
- `13roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `13roWSL/docs/fisa_comenzi.md` — useful commands
- `13roWSL/src/` — Python code examples
- `13roWSL/homework/` — similar exercises


### 📁 `04roWSL/` — Protocoale Personalizate

**What you'll find relevant:**
- Parsarea header-elor, struct modules

**Recommended files:**
- `04roWSL/README.md` — overview and laboratory steps
- `04roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `04roWSL/docs/fisa_comenzi.md` — useful commands
- `04roWSL/src/` — Python code examples
- `04roWSL/homework/` — similar exercises


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
