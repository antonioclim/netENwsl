# Project 19: Instrument de scanare a porturilor for analiza securității network

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
https://github.com/[username]/retele-proiect-19
```

#### Required Repository Structure

```
retele-proiect-19/
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

**Format:** `NUME_Prenume_GGGG_P19_TT.zip`

| Field | Description | Example |
|------|-----------|---------|
| NUME | Family name (UPPERCASE, no diacritics) | POPESCU |
| Prenume | First name (first letter capitalised) | Ion |
| GGGG | Group number (4 digits) | 1098 |
| P19 | Project number | P19 |
| TT | Deliverable type (S1-S4 or SXX) | E1 |

**Examples for this project:**
- `POPESCU_Ion_1098_P19_E1.zip` — Stage 1
- `POPESCU_Ion_1098_P19_E2.zip` — Stage 2
- `POPESCU_Ion_1098_P19_S07.zip` — Verification săptămâna 7

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

Descriere: This project has ca temă dezvoltarea unui utilitar simple de scanare a porturilor and utilizarea sa for a evalua configurația de security a unui sistem din network. Scopul is de a înțelege cum funcționează scanarea porturilor – o tehnică folosită atât de administratorii de network (for inventarierea serviciilor deschise), cât and de potențiali atacatori (for identificarea punctelor vulnerabile)[6][7]. Studenții vor implementa o application which, dat being un nume de host or o address IP, încearcă connections towards o serie de ports (ex. 1-1024 or un subset relevant) and raportează which ports has deschise, închise or filtrate. Scanarea se va realiza initial la nivel de TCP connect() – adică through încercarea de a stabili o connection TCP pe each port and observarea rezultatului – metodă simple ce indică porturile deschise if connection reușește. After implementation, utilitarul va fi folosit for a scana un sistem de test, iar rezultatele vor fi analizate: ce services rulează pe porturile deschise, ce implicații de security există and ce măsuri ar trebui luate (for example, închiderea porturilor neutilizate or protejarea serviciilor expuse). Proiectul oferă thus o perspectivă practică asupra securității network la nivel de host and a modalităților de identificare a vulnerabilităților simple.

### 🎯 Learning Objectives


### 📖 Key Concepts

Technologies Involved: Limbaj de programare cu acces la socket-uri raw or TCP – Python recomandat (simplifică paralelizarea and tratarea excepțiilor), posibile biblioteci precum socket, threading/asyncio. Eventual utilizarea modulului scapy (advanced, for SYN scan, but optional). Sistem de operare: preferabil Linux for teste mai facile de network, but and Windows e posibil. Utilitare de monitorizare (for a vedea if porturile has deschise – de ex. netstat) and eventual un instrument third-party (nmap) for a compara rezultatele scanner-ului realizat cu cele ale unui instrument consacrat. Totodată, cunoștințe about services comune (for interpretarea rezultatului scanării). Proiectul nu necesită hardware special, only acces la o mașină de test (can fi even localhost-ul).
Legătura cu weeks and kiturile: Proiectul se conectează cu săptămâna 13, unde have been studiate noțiuni de security în networks and instrumente precum scanarea de ports and testing vulnerabilităților. În laboratorul 7 (Interceptarea pachetelor and scanarea porturilor) studenții have experimentat probabil folosirea unor unelte ca nmap or implementation unui mic filtru de packets. Kitul de laborator aferent (ex. script de scanare parțial implementat or examples de rezultate nmap) va servi ca point de plecare. Proiectul extinde these cunoștințe, solicitând studenților să își dezvolte propriul program de scanare, consolidând totodată cunoștințele de socket programming (weeks 2-3) and de protocols de transport (săptămâna 8). Thus, is un example integrator: folosește programare de network for un scop de security, reunind elemente de curs din capitole diferite.
Structura pe 4 stages: 1. Stage 1: Definirea specificațiilor and mediului de lucru. În prima stage, se stabilește ce tip de scanare se va implementa and which is ținta de test. De example, team decide să implementeze un TCP connect scan pe un interval de ports 1-1024 al unui server de test (which can fi o mașină locală or o address IP din network proprie, cu permisiune). Se pregătește mediul de lucru: se identifică o mașină țintă cu câteva ports cunoscute deschise (ex. se can activa pe mașina țintă un server web pe port 80, un SSH pe 22, etc., for a have rezultate de scanare variate). Totodată, se conturează algoritmul: iterarea peste ports and for each port, încercarea de conectare TCP cu un anumit timeout. Se selectează limbajul de implementation and se configurează project. 2. Stage 2: Implementarea scanner-ului de ports. Echipa dezvoltă programul conform planului. Se implementează citirea parametrilor (for example IP țintă and range de ports de scanat). For each port din interval, se creează un socket TCP neconectat and se apelează metoda de conectare (connect) towards IP-ul țintă la that port, cu un timeout scurt (ex. 1-2 secunde). If connection is stabilită cu succes, rezultatul se notează ca “port deschis”, then se închide imediat connection. If se primește refuz de connection (error de tip connection refused), se notează “port închis”. If apelul expiră (timeout) without răspuns, is posibil un “port filtrat” (nesigur, but se va interpreta ca posibil filtrat de firewall). For eficiență, se can implementa this scanare în paralel: for example, using thread-uri or task-uri asincrone for a scana mai multe ports simultan, ținând cont however de limitările resurselor. Rezultatele fiecărui test has stocate (for example într-o structură de date) for a fi raportate ulterior. Codul must să fie solid, gestionând excepțiile posibile (erori de network, cazuri în which ținta nu is disponibilă deloc etc.). 3. Stage 3: Testarea aplicației and colectarea rezultatelor. Odată implementat scanner-ul, se trece la testing sa pe ținta aleasă. Se rulează scanarea and se observă output-ul generat – which ports have been raportate deschise. Echipa validează these rezultate comparând cu realitatea: for example, if știu că pe mașina țintă rulează un service pe port X, acesta ar trebui să apară ca deschis; if port Y a been blocat de firewall, scanner-ul lor ar trebui să arate timeout. Optional, se can rula în paralel un instrument consacrat (cum ar fi nmap -sT) pe același target and port range, for a verifica if rezultatele propriului utilitar has corecte or if have ratat ceva. Se make ajustări if e nevoie (for example, mărirea timeout-ului if network e mai lentă or corectarea interpretării unor erori). În final, se obține o listă de ports deschise pe sistemul de test. 4. Stage 4: Analiza de security and documentarea. Ultima stage is dedicată interpretării rezultatelor scanării and scrierii raportului. Echipa va identifica, for each port deschis găsit, ce service probabil rulează there (through convențiile cunoscute – for example 80 http, 22 ssh, 3389 RDP etc. or eventual using mici packets de banner grabbing: trimiterea unei cereri simple and citirea răspunsului, if doresc). Se va discuta implicarea fiecărui service în security sistemului: for example, “am găsit port 21 deschis, ceea ce sugerează un server FTP – se știe că FTP transmite datele necriptat and ar putea reprezenta un risc de security if nu e configurat adecvat”. Se vor recomanda măsuri de remediere for a securiza sistemul: închiderea porturilor ne-necesare, aplicarea de politici firewall, actualizarea serviciilor, utilizarea de versiuni securizate (ex. SFTP instead of FTP). Raportul va descrie and cum funcționează scanner-ul implementat, ce limitări has (spre example, faptul că detectarea unui port filtrat nu e 100% sigură or că scanarea TCP connect is mai lentă and mai zgomotoasă față de un SYN scan). Vor fi incluse fragmente de code relevante (pseudo-code) and eventual capturi cu execuții. Echipa va reflecta asupra modului în which this project i-a ajutat să înțeleagă mai bine atât programarea de network, cât and perspectiva unui administrator de security ce examinează suprafața de atac a propriului sistem.
Extensii for teams de 3/2/1: - Teams de 3 persons: Se can aventura în implementation unor caracteristici avansate which să îmbunătățească scanner-ul or analiza de security. De example, implementation unui mod de scanare UDP for câteva ports importante (deși mai dificil de interpretat because UDP nu răspunde cu ACK la succes) or implementation unui SYN scan (trimițând manual packets TCP SYN using o bibliotecă ca Scapy and interpretând răspunsurile SYN/ACK or RST – practic replicând comportamentul nmap -sS). O altă extensie utilă ar fi includerea de banner grabbing: for porturile deschise identificate, programul can încerca să trimită automat o solicitare minimă (for example, un “HEAD / HTTP/1.0” for port 80) and să capteze răspunsul for a identifica versiunea serviciului. În plus, team can extinde analiza post-scanare: de pildă, interogarea unei baze de date de vulnerabilități cunoscute pe baza versiunii serviciilor (aceasta however only la nivel de discuție, nu implementation integrată). These extensii vor demonstra cunoștințe aprofundate and abilități tehnice ridicate, but nu has obligatorii. - Teams de 2 persons: Vor realiza scanner-ul de ports standard and analiza de security de bază, conform descrierilor din etapele 2-4. Distribuirea muncii can fi so that un member se concentrează pe partea de code and funcționalitatea tehnică, iar celălalt pe documentare and interpretare, deși ambele părți must să colaboreze strâns. O mică extensie posibilă for două persons is rularea scanner-ului pe mai multe ținte din network (for example, scanarea a 2-3 mașini diferite) and compararea rezultatelor, for a oferi un context mai larg în report. Important is however ca utilitarul să funcționeze corect and raportul să conțină o discuție coerentă about security sistemului scanat. - Teams de 1 person: Un student individual can reduce anvergura project for a fi realizabil într-un timp mai scurt, but păstrând esența educațională. De example, se can limita scanarea la primele 1024 ports TCP ale propriei mașini (localhost), unde studentul știe ce services has active and thus can verifica ușor rezultatele. Implementarea can fi secvențială (without paralelizare), if gestionarea thread-urilor e prea complexă de integrat de o singură person – accentul va fi pe corectitudinea detecției porturilor deschise. Analiza de security va fi mai simple and focalizată pe interpretarea câtorva ports găsite (ex: “Am scanat localhost and am găsit port 80 deschis – am un server Apache, must să mă asigur că e actualizat la zi and configurat corespunzător.”). Even and without all optimizările, studentul must să demonstreze că a înțeles mecanismul and can comenta asupra implicațiilor de security, în loc să ofere only un code functional.

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

Bhuyan, M. H., Bhattacharyya, D. K., & Kalita, J. K. (2011). Surveying Port Scans and Their Detection Methodologies. The Computer Journal, 54(10), 1565–1581. DOI: 10.1093/comjnl/bxr035
Abu Bakar, R., & Kijsirikul, B. (2023). Enhancing Network Visibility and Security with Advanced Port Scanning Techniques. Sensors, 23(17), 7541. DOI: 10.3390/s23177541
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


### 📁 `02roWSL/` — Programare Socket

**What you'll find relevant:**
- TCP connect scan, socket timeout

**Recommended files:**
- `02roWSL/README.md` — overview and laboratory steps
- `02roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `02roWSL/docs/fisa_comenzi.md` — useful commands
- `02roWSL/src/` — Python code examples
- `02roWSL/homework/` — similar exercises


### 📁 `07roWSL/` — Interceptare Pachete

**What you'll find relevant:**
- Analiza răspunsurilor TCP

**Recommended files:**
- `07roWSL/README.md` — overview and laboratory steps
- `07roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `07roWSL/docs/fisa_comenzi.md` — useful commands
- `07roWSL/src/` — Python code examples
- `07roWSL/homework/` — similar exercises


### 📁 `13roWSL/` — Security

**What you'll find relevant:**
- Ethical hacking, vulnerability assessment

**Recommended files:**
- `13roWSL/README.md` — overview and laboratory steps
- `13roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `13roWSL/docs/fisa_comenzi.md` — useful commands
- `13roWSL/src/` — Python code examples
- `13roWSL/homework/` — similar exercises


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
