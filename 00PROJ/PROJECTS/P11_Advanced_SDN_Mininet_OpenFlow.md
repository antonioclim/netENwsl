# Project 11: Network definită through software (SDN) cu Mininet and OpenFlow

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
https://github.com/[username]/retele-proiect-11
```

#### Required Repository Structure

```
retele-proiect-11/
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

**Format:** `NUME_Prenume_GGGG_P11_TT.zip`

| Field | Description | Example |
|------|-----------|---------|
| NUME | Family name (UPPERCASE, no diacritics) | POPESCU |
| Prenume | First name (first letter capitalised) | Ion |
| GGGG | Group number (4 digits) | 1098 |
| P11 | Project number | P11 |
| TT | Deliverable type (S1-S4 or SXX) | E1 |

**Examples for this project:**
- `POPESCU_Ion_1098_P11_E1.zip` — Stage 1
- `POPESCU_Ion_1098_P11_E2.zip` — Stage 2
- `POPESCU_Ion_1098_P11_S07.zip` — Verification săptămâna 7

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

Descriere: This project constă în proiectarea and implementation unei networks definite through software (Software-Defined Network – SDN) using emulatorul Mininet and protocol OpenFlow. SDN is un model modern de arhitectură de network which decuplează planul de control de planul de date, oferind flexibilitate sporită and posibilitatea de a programa comportamentul network printr-un controller centralizat[1]. Studenții vor crea o topology virtuală complexă în Mininet (for example, cu mai multe switch-uri OpenFlow interconectate and zeci de host-uri), then vor dezvolta un controller SDN în Python which să gestioneze în mod dinamic traffic în network. Controller-ul can fi realizat fie using o platformă existentă (de tip POX, Ryu etc.), fie through programarea directă a unor reguli OpenFlow through API-ul oferit de Mininet. Scopul is implementation unor funcționalități avansate precum rutarea adaptivă a pachetelor, echilibrarea traficului or filtrarea and prioritizarea anumitor tipuri de traffic, demonstrând avantajele SDN față de rețelele tradiționale. Proiectul has o componentă tehnică puternică (setarea unui mediu de simulare, programarea controller-ului, analiza traficului) and o componentă pedagogică, întrucât îi provoacă pe students să gândească network în termeni algoritmici and să aplice cunoștințele teoretice about protocols la un sistem real emulator. Through experimentare, team va evidenția modules în which controller-ul central reacționează la evenimente din network (de ex. căderea unui nod, aglomerarea unei legături) through instalarea de noi reguli de forwardare în switch-uri. Rezultatul final va fi o network virtuală controlată programatic, în which se can vizualiza în timp real modules de funcționare al algoritmilor de control de nivel network.

### 🎯 Learning Objectives

- Să evalueze avantajele and dezavantajele soluției implementate comparativ cu alternative.
• Să compare performanța project cu soluții similare or benchmark-uri de referință.

### 📖 Key Concepts

Technologies Involved: Python (for programarea logicii controller-ului SDN), Mininet (emulare network virtuală), protocol OpenFlow 1.3+, controller OpenFlow (POX/RYU or implementation custom), utilitare de monitorizare a traficului (Wireshark, tcpdump) for inspectarea pachetelor, eventual Open vSwitch (integrat în Mininet) ca elemente de comutare. Se vor folosi biblioteci specifice Python for networks (example: biblioteca Mininet or interfete REST API if se folosește un controller extern).
Legătura cu weeks and kiturile (WEEK1-14): Proiectul valorifică cunoștințele acumulate în weeks dedicate rutării and administrării rețelelor. În mod particular, temele din săptămâna 5 (adresare IP, rutare statică and dinamică) and săptămâna 6 (introducere în SDN and virtualizare de network) stau la baza cerințelor project. Kitul de laborator al săptămânii 6, which include experimente de bază cu Mininet and OpenFlow, va oferi un point de pornire practic. Totodată, conceptual, project se leagă de discuțiile about algoritmi de rutare (săpt. 5-6) and de instrumentele de monitorizare a traficului prezentate în săptămâna 7 (captură de packets and filtrare), utile for testing soluției SDN.
Structura project în 4 stages: - Stage 1 (săptămâna 5): Definirea cerințelor and a design-ului arhitectural al network SDN. Echipa va realiza un plan al topologiei (număr de noduri, connections, rolul fiecărui element) and va stabili obiectivele precise (ex: implementation unui algoritm de rutare adaptivă). În this stage se vor instala and configura instrumentele de lucru (Mininet, mediul Python, eventuale packets for controller) and se va efectua un experiment initial simple în Mininet for a verifica funcționarea de bază (ex. ping between host-uri printr-un switch OpenFlow controlat de un controller default). - Stage 2 (săptămâna 9): Implementarea initial a controller-ului SDN and realizarea unei networks funcționale simple. Până la this point, studenții vor fi dezvoltat logica de bază a controller-ului (for example, un modules which acționează ca un learning switch or realizează o rutare statică prestabilită). Topologia creată în Mininet va fi populată cu câteva host-uri de test, iar controller-ul va instala reguli OpenFlow elementare (de tipul forwardare pe bază de MAC or IP). Se vor testa funcțiile elementare: conectivitatea capăt-la-capăt (using ping, iperf), capacitatea controller-ului de a procesa evenimente (ex: packets PacketIn OpenFlow) and de a insera intrări în tablorile de flux ale switch-urilor. - Stage 3 (săptămâna 13): Extinderea and finalizarea project SDN cu funcționalități avansate. În this stage, se implementează all requirements complexe asumate: for example, algoritmul adaptiv de rutare which detectează congestia and redirecționează traffic pe rute alternative or un modules de security which blochează traffic suspect. Se vor realiza teste extensive în scenarii variate: căderea unui nod de network (for a observa reacția controller-ului), simularea unui volum mare de traffic (for a evalua performanța and latența deciziilor controller-ului) etc. Studenții vor aduna metrici (timp de convergență, throughput, rate de pierdere packets) and le vor analiza critic, pregătind thus material for concluzii. - Stage 4 (prezentarea în săptămâna 14): Echipa va prezenta project în cadrul seminarului final, demonstrând practic funcționarea network SDN create. Prezentarea va include o descriere arhitecturală (topology and modules de interacțiune between controller and elementele de network), o demonstrație live (for example, rularea Mininet cu controller-ul activ and arătarea modului în which pachetele has redirecționate conform regulilor programate) and o discuție asupra rezultatelor obținute. Vor fi evidențiate beneficiile abordării SDN – cum ar fi flexibilitatea reconfigurării network în timp real – and provocările întâmpinate (de pildă, complexitatea depanării or limitările de performanță).

### 🔮 VERIFICARE ÎNȚELEGERE - SDN ȘI OPENFLOW

Before de a rula comenzile, răspundeți la următoarele întrebări:

1. Când rulați pingall în Mininet, between which perechi de host-uri va eșua ping-ul?
 → Analizați regulile de firewall din controller for a prezice rezultatul.

2. Ce mesaje OpenFlow vor apărea în log-ul controller-ului la primul ping?
 → Răspuns așteptat: PacketIn (cerere ICMP), then FlowMod (instalare regulă).

3. After instalarea regulii, ce se întâmplă la al doilea ping between aceleași host-uri?
 → Pachetele has procesate direct de switch, without PacketIn towards controller.

4. Câte reguli vor fi în tabela de flux after pingall?
 → Verificați cu: dpctl dump-flows


### 📊 PEER INSTRUCTION - SDN ȘI OPENFLOW

Discutați cu colegii and alegeți împreună răspunsul corect:

Întrebarea 1: After ce controller-ul instalează o regulă OpenFlow cu actions=drop, ce se întâmplă cu pachetele which make match?

A) Are trimise înapoi la sursă cu ICMP Destination Unreachable
B) Are șterse silențios without nicio notificare ✓
C) Are redirecționate towards controller for logging
D) Are puse în coadă până expiră timeout-ul flow-ului

Explicație: Acțiunea drop elimină packet complete. For ICMP unreachable ar fi nevoie de o regulă explicită which să trimită this mesaj.

Întrebarea 2: Ce tip de mesaj OpenFlow trimite switch-ul towards controller când primește un packet for which nu există regulă?

A) FlowMod (modificare flux)
B) PacketIn (packet primit) ✓
C) PacketOut (trimite packet)
D) PortStatus (stare port)

Explicație: PacketIn = switch întreabă controller-ul ce să facă. FlowMod = controller instalează regulă în switch.


### Extensii for teams de 3 vs. 2/1 members: For echipele formate din 3 students, se așteaptă un nivel suplimentar de complexitate. De example, team can implementa o network multi-domeniu cu două controllere SDN ierarhizate (un controller local and un controller global de coordonare) or can adăuga functions extra precum mecanisme de security (firewall SDN integrat) ori algoritmi de load balancing for distribuirea traficului between mai multe servers. Totodată, can fi incluse scripturi de automatizare (ex: un dashboard web simple for vizualizarea topologiei and a fluxurilor în timp real). For echipele de 2 students or individuale, complexitatea can fi ajustată: is suficientă o singură network SDN cu un controller centralizat and un set de functions de bază (de ex. rutare statică cu posibilitate de actualizare manuală or un singur tip de eveniment gestionat – cum ar fi eșecul unui link). Numărul de noduri din topology can fi mai redus, iar focusul can fi pus pe înțelegerea corectă a mecanismelor OpenFlow and mai puțin pe optimizarea perfectă a performanțelor. Thus, criteriile de assessment vor ține cont de dimensiunea echipei, punând accent pe originalitatea soluției and corectitudinea functional mai degrabă decât pe anvergura implementării în cazul echipelor mai mici.


═══════════════════════════════════════════════════════════════════════════════
📊 CERINȚĂ SUPLIMENTARĂ: ANALIZĂ COMPARATIVĂ
═══════════════════════════════════════════════════════════════════════════════
Pe lângă implementation tehnică, includeți în raportul final o secțiune de analiză comparativă (1-2 pagini) which să conțină:

1. COMPARAȚIE CU ALTERNATIVE
 • Identificați at least 2 tehnologii/abordări alternative for problema rezolvată
 • Argumentați de ce ați ales abordarea actuală

2. METRICI DE PERFORMANȚĂ
 Măsurați and raportați at least 2 metrici relevante:
 • Latență (timp de răspuns) or Throughput
 • Timp de convergență or Utilizare resurse

3. LIMITĂRI ȘI ÎMBUNĂTĂȚIRI
 • Ce limitări conștiente has soluția voastră?
 • Cum ar putea fi extinsă or îmbunătățită?
═══════════════════════════════════════════════════════════════════════════════


### ❓ ÎNTREBĂRI FRECVENTE - SDN/MININET

Q: Mininet won't start and afișează "Error creating interface"
A: Rulați cu sudo and curățați sesiunile anterioare:
 sudo mn -c
 sudo mn --topo single,3 --controller remote

Q: Controller-ul nu primește mesaje PacketIn
A: Verificați că switch-ul e conectat la controller:
 - dpctl show
 - Asigurați-vă că IP-ul controller-ului e corect în topology

Q: Cum testez că firewall-ul funcționează corect?
A: Folosiți comenzi de test în Mininet CLI:
 - h1 ping h2 (for traffic which ar trebui blocat)
 - h1 curl h2:80 (for traffic which ar trebui permis)
 - Verificați log-urile controller-ului for decizii


### 📚 Bibliografie

---

## 🔮 Verification înțelegere — SDN and OpenFlow

Before de a rula comenzile, răspunde la these întrebări:

1. **Când rulezi `pingall` în Mininet, between which host-uri va eșua ping-ul?**
 - Analizează regulile de firewall din controller
 - Răspuns așteptat: Perechile which încalcă regulile (ex: ICMP blocat)

2. **Ce mesaje OpenFlow apar în log-ul controller-ului la primul ping?**
 - PacketIn (cerere ICMP) → FlowMod (instalare regulă)

3. **Ce se întâmplă la al doilea ping between aceleași host-uri?**
 - Switch-ul procesează direct, without PacketIn

Verifică cu `dpctl dump-flows` câte reguli has instalate.

---

## 📊 Peer Instruction — SDN

**Întrebare:** After ce controller-ul instalează o regulă cu `actions=drop`, ce se întâmplă cu pachetele?

- A) Are trimise înapoi cu ICMP unreachable
- B) Are șterse silențios without notificare ✓
- C) Are redirecționate towards controller
- D) Are puse în coadă

**Explicație:** Acțiunea `drop` elimină packet complete, without nicio notificare.


---

## ❓ Frequently Asked Questions — SDN/Mininet

**Q: Mininet won't start - eroare "cannot create interface"** 
A: Run with sudo and clean previous sessions:
```bash
sudo mn -c
sudo mn --topo single,3 --controller remote
```

**Q: Controller-ul nu primește PacketIn** 
A: Check the connection switch-controller cu `dpctl show`

**Q: Cum testez că firewall-ul funcționează?** 
A: Folosește `h1 ping h2` for traffic blocat and `h1 curl h2:80` for traffic permis


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

---

## 📚 RELEVANT LABORATORY MATERIALS

Consultă these resurse din arhiva **netROwsl** for conceptele necesare:


### 📁 `06roWSL/` — SDN

**What you'll find relevant:**
- OpenFlow avansate, QoS, traffic engineering

**Recommended files:**
- `06roWSL/README.md` — overview and laboratory steps
- `06roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `06roWSL/docs/fisa_comenzi.md` — useful commands
- `06roWSL/src/` — Python code examples
- `06roWSL/homework/` — similar exercises


### 📁 `07roWSL/` — Filtrare Pachete

**What you'll find relevant:**
- Deep packet inspection, metrici

**Recommended files:**
- `07roWSL/README.md` — overview and laboratory steps
- `07roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `07roWSL/docs/fisa_comenzi.md` — useful commands
- `07roWSL/src/` — Python code examples
- `07roWSL/homework/` — similar exercises


### 📁 `05roWSL/` — Adresare IP

**What you'll find relevant:**
- Routing decisions bazate pe IP

**Recommended files:**
- `05roWSL/README.md` — overview and laboratory steps
- `05roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `05roWSL/docs/fisa_comenzi.md` — useful commands
- `05roWSL/src/` — Python code examples
- `05roWSL/homework/` — similar exercises


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
