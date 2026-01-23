# Project 02: Network hibridă cu Mininet and containere Docker

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
https://github.com/[username]/retele-proiect-02
```

#### Required Repository Structure

```
retele-proiect-02/
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

**Format:** `NUME_Prenume_GGGG_P02_TT.zip`

| Field | Description | Example |
|------|-----------|---------|
| NUME | Family name (UPPERCASE, no diacritics) | POPESCU |
| Prenume | First name (first letter capitalised) | Ion |
| GGGG | Group number (4 digits) | 1098 |
| P02 | Project number | P02 |
| TT | Deliverable type (S1-S4 or SXX) | E1 |

**Examples for this project:**
- `POPESCU_Ion_1098_P02_E1.zip` — Stage 1
- `POPESCU_Ion_1098_P02_E2.zip` — Stage 2
- `POPESCU_Ion_1098_P02_S07.zip` — Verification săptămâna 7

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
This project propune construirea unei networks hibride which integrează noduri containerizate Docker într-o topology virtuală Mininet. Scopul is de a experimenta cu conectivitatea containerelor într-un mediu de network personalizat and de a explora modules în which aplicațiile containerizate comunică peste network. Practic, se va extinde funcționalitatea Mininet through utilizarea unei platforme precum Containernet (o versiune extinsă a Mininet which suportă containere Docker ca host-uri)[3]. Thus, unele noduri din topology emulată nu vor fi simple host-uri Linux generice, ci containere Docker which rulează services reale (for example, un server web Nginx or o bază de date MySQL).
Scenariul concret al project ar putea fi simularea unei mici infrastructuri de microservicii: de pildă, un container rulează un service web, alt container rulează un service de baze de date, iar alte containere acționează ca clients. These containere has interconectate through switch-uri virtuale în Mininet, permițând controlul detaliat al topologiei (for example, putem insera un router virtual between services for a testa latența or putem limita banda between containere). Proiectul va demonstra cum se configurează network Docker (bridge, interfețe virtuale) în contextul Mininet and cum can fi orchestrate containerele în cadrul unei networks personalizate. Totodată, oferă ocazia de a testa comunicarea inter-container în condiții variate (ex. restricții de network, latență simulată, pierdere de packets) and de a observa performanța. Rezultatul final va fi o platformă de test reproductibilă, which combină flexibilitatea Mininet cu realismul containerelor, utilă for prototiparea serviciilor distribuite.

### 🎯 Learning Objectives

Înțelegerea modului în which containerele Docker se conectează în network (bridge networks, veth pairs, etc.) and modules de integrare a acestora într-o topology personalizată.
Familiarizarea cu conceptul de virtualizare la nivel de container versus virtualizare de network (Mininet) and explorarea beneficiilor integrării lor.
Dezvoltarea abilităților de configuration a ambiențelor de network complexe, which imită scenarii reale de microservicii, într-un mediu controlat de laborator.
Măsurarea and analizarea performanței network containerizate: latență, debit (throughput), comportament în condiții de pierdere a pachetelor, etc., using instrumente de test (iperf, ping, Apache Benchmark for HTTP, etc.).

### 🛠️ Technologies and Tools


### 📖 Key Concepts

Networks virtualizate – folosirea Mininet for a crea networks virtuale personalizate (nivel 2/3) cu parametri controlați (topology, bandwidth, delay).
Containere Docker – noțiuni de containerizare, imagini Docker, network implicită a containerelor (bridge Docker) vs. networks personalizate.
Integrarea containerelor în network – conectarea containerelor la switch-urile Mininet through interfețe virtuale, utilizarea Containernet or configuration manuală cu veth pairs.
Protocoale de comunicație client-server – exemplificate de serviciile rulate în containere (HTTP for web, SQL for DB, etc.), plus mecanisme de rezoluție DNS interne Docker, if e cazul.
Testing and monitorizare de network – folosirea de utilitare (tcpdump, iperf, ab - Apache Benchmark) for a genera traffic and a colecta date de performanță.
Technologies Involved
Mininet/Containernet – platforma de emulare a network. Containernet extinde Mininet for a suporta containere Docker ca noduri.
Docker – for a crea containere ce rulează services (imagini de Linux cu aplicațiile necesare). Vor fi utilizate comenzi Docker Compose or Docker CLI for gestionarea containerelor.
Python – limbaj folosit for a orchestra scenariul (Mininet has API Python; se can scrie un script Python which construiește topology, lansează containere and configurează legăturile).
Linux networking tools – tc (Traffic Control) for a induce latență/pierderea de packets pe linkuri if se dorește, brctl/ovs-vsctl for configurări fine ale bridge-urilor (if e cazul la nivel jos).
Servicii de test – ex: server HTTP (Nginx/Apache în container), server de bază de date (MySQL/PostgreSQL), plus clients (curl, wget, scripturi Python) for a genera traffic de test.
Connection to Weekly Course Topics
Week 10: Virtualizare de network – project combină virtualizarea network (Mininet) cu virtualizarea containerelor (Docker), extinzând conceptele discutate în curs (vezi file „Virtualizare and Cloud” din arhiva WEEK10).
Week 11: Networks de containere and Docker – se aplică direct cunoștințele about rețelele containerelor Docker (bridge, overlay) prezentate în săptămâna 11 (ex. laboratorul „Docker Networking” din arhivă), integrând containere în topology Mininet.
Week 5: Adresare IP – definirea adreselor IP for containere în network Mininet cere înțelegerea subrețelelor (similar cu exercițiile din Week5 privind configuration adreselor IP manual for noduri).
Week 8: Protocoale de application – rularea unui service web and a unei baze de date în containere atinge conceptele discutate în curs about protocols de nivel application (HTTP, SQL over TCP etc.) and modules lor de funcționare în network.
Etapele project

### 📋 Stage 1 (Week 5) – Planificare and setup initial: Investigarea modului în which Containernet (or alternativa manuală) permite integrarea containerelor în Mininet. Alegerea unui scenariu de utilizare – for example, application web cu 2-3 microservicii. Se vor defini rolurile containerelor (ex: container A – server web, container B – bază de date, container C – client simulând utilizatorul). Livrabil: document de design ce include diagrama topologiei network (arată switch-urile, containerele and legăturile among ele, plus subrețelele/IP-urile alocate fiecărui container), precum and pașii de configuration a mediului (versiuni de Mininet/Containernet, imagini Docker ce vor fi folosite or create). Se va pregăti mediul de dezvoltare: instalarea Mininet/Containernet and crearea unui repository for project (cu eventuale Dockerfile-uri or un docker-compose.yml de bază).


### 🔨 Stage 2 (Week 9) – Implementation parțială: Construirea efectivă a topologiei and rularea containerelor. Se can realiza un script Python which pornește Mininet, adaugă noduri de tip Docker container (using API-ul Containernet) and configurează conexiunile. Se vor crea or descărca imaginile Docker necesare (for example, o imagine cu server web configurat). Se testează comunicarea de bază: for example, client din container C makes o cerere HTTP towards containerul A (server web) – packet traversează network Mininet and răspunsul ajunge înapoi. Livrabil: code sursă al scriptului de configuration a network (în repository), fișierele Dockerfile or compose for definirea containerelor and un jurnal de teste inițiale (loguri which arată că containerele se pingăsc reciproc, că server web răspunde la cereri din partea clientului etc.).


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


### ✅ Stage 3 (Week 13) – Experimente and finalizare: Introducerea de scenarii de test mai complexe and colectarea rezultatelor. De example, măsurarea timpului de răspuns al serviciului web din container A for diferite dimensiuni de traffic or sub diferite întârzieri simulate pe legătura towards client. Se can aplica limite de bandă or latență pe legăturile din Mininet for a vedea impactul asupra performanței aplicației distribuite. Totodată, se va asigura solideză: containerele pornesc în ordinea corectă, if un container is repornit, network still funcționează etc. Livrabil: code final (script Python, configurații) însoțit de documentation (README cu instrucțiuni clare de rulare a experimentului de towards oricine), grafică/diagrama actualizată a topologiei finale and un report de experimentare. Raportul va include descrierea testelor efectuate, metricile culese (latență, throughput, timpi de răspuns) sub formă de tabele/grafice, plus discuții. Se vor evidenția eventualele probleme întâlnite and soluțiile adoptate.


### 📊 PEER INSTRUCTION - DOCKER ȘI REȚELE CONTAINERE

Discutați cu colegii and alegeți împreună răspunsul corect:

Întrebarea 1: Containerele web and db has în aceeași network Docker bridge. Cum can web să se conecteze la port 5432 al db?

A) localhost:5432 - containerele partajează același localhost
B) db:5432 - Docker DNS rezolvă automat numele serviciului ✓
C) 172.17.0.1:5432 - address gateway-ului bridge
D) host.docker.internal:5432 - referință la mașina host

Explicație: Docker Compose creează DNS intern. Containerele se găsesc through numele serviciului, nu through localhost (which e izolat per container).

Întrebarea 2: Un container expune port 8080:80. Ce înseamnă this configuration?

A) Containerul ascultă pe 8080, host-ul expune pe 80
B) Host-ul ascultă pe 8080, containerul intern pe 80 ✓
C) Ambele ports has echivalente
D) Portul 8080 is blocat de firewall

Explicație: Formatul is HOST_PORT:CONTAINER_PORT. Accesați service din browser la http://localhost:8080


### 🎤 Stage 4 (Week 14) – Prezentare final: Prezentarea va sublinia arhitectura hibridă a network create, modules de integrare Docker–Mininet and rezultatele cheie ale experimentelor. Se va realiza o demonstrație: for example, accesarea serviciului web din containerul A de towards containerul C, cu monitorizarea traficului în direct (using ping or ab for a arăta latența and throughput-ul). Livrabil: slide-urile prezentării and un demo live (or înregistrat) which să ilustreze funcționalitatea network hibride and eventual diferențele față de o configurație clasică.

Extensii posibile for teams de 3 vs. 2/1 students
For echipele de 3: project se can extinde through creșterea complexității topologiei and a serviciilor. De example, se can lansa mai multe instanțe de containere for scalare (simulând un cluster de microservicii) and implementa un load-balancer în network which distribuie traffic between ele. O altă extensie ar fi integrarea unui orchestrator simple (ex. Docker Compose or even Kubernetes minikube if se dorește un challenge suplimentar) for a gestiona containerele la scară mai mare. Tot for teams mai mari, s-ar putea monitoriza resursele (CPU, memorie) consumate de containere sub sarcină and include analiza acestor date în report.
For teams mai mici (2 or 1 student): se recomandă limitarea numărului de services/container la cele esențiale (for example only 2 containere which comunică direct) and evitarea configurărilor very complicate de network. Un singur switch and o singură subnet can fi suficiente. Optional, se can reduce amploarea testelor de performanță – de pildă, assessment se can makes only calitativ (se vede că comunicarea has loc) and cu câteva măsurători simple de timp de răspuns, without a intra în optimizări avansate. Thus, still se demonstrează integrarea Docker-Mininet, but volumul de muncă rămâne gestionabil.

### ❓ ÎNTREBĂRI FRECVENTE - DOCKER

Q: Eroare "port is already allocated" la pornirea containerelor
A: Portul e ocupat de alt proces. Soluții:
 - Verificați: ss -tlnp | grep :PORT
 - Opriți procesul existent or schimbați port în docker-compose.yml

Q: Containerele nu can comunica between ele
A: Verificați configuration network:
 - docker network ls (listează rețelele)
 - docker network inspect NETWORK_NAME (detalii)
 - Asigurați-vă că serviciile has în aceeași network

Q: Cum văd log-urile unui container for debugging?
A: Folosiți comenzile:
 - docker logs CONTAINER_NAME
 - docker compose logs SERVICE_NAME
 - docker compose logs -f (follow în timp real)


### 📚 Bibliografie

Dupont, C., & Qu, C. (2018). Containernet: A Network Emulator with Docker Support for SDN Experimentation. In Proceedings of the IEEE Conference on Network Function Virtualization and Software Defined Networks (NFV-SDN) (pp. 1-2). (Containernet – introducere and utilizare practică)
Hausenblas, M. (2018). Container Networking: From Docker to Kubernetes. O’Reilly Media. (prezentare a conceptelor de networks for containere Docker and integrarea în infrastructuri cloud)
Merkel, D. (2014). Docker: Lightweight Linux Containers for Consistent Development and Deployment. Linux Journal, 2014(239), Articol 2. (introducere în containerizarea Docker and avantajele sale în medii de dezvoltare)
Alwahibee, A., Köpsel, A., & Karl, H. (2019). A Performance Evaluation of Container Networking. IEEE Transactions on Network and Service Management, 16(4), 1550-1563. https://doi.org/10.1109/TNSM.2019.2947599 (lucrare academică ce evaluează performanța rețelelor containerizate, relevantă for teste de performanță)
Documentation Containernet: Containernet GitHub Repository & Wiki. (2021). Disponibil la: https://github.com/containernet/containernet/wiki (resursă practică for configuration Containernet and examples de utilizare).
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

## ❓ Frequently Asked Questions — Docker

**Q: Eroare "port is already allocated"** 
A: Portul e ocupat. Verifică: `ss -tlnp | grep :PORT` and oprește procesul or schimbă port.

**Q: Containerele nu comunică between ele** 
A: Verifică network: `docker network ls` and `docker network inspect NETWORK`

**Q: Cum văd logurile unui container?** 
A: `docker logs CONTAINER` or `docker compose logs SERVICE`


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


### 💡 For Docker and Containere

Din TW știi npm and package.json. Docker e similar but for mediu complete:

```yaml
# docker-compose.yml e similar cu package.json pentru dependențe
# dar include și mediul de runtime

services:
 web:
 image: nginx
 ports:
 - "8080:80" # Similar cu "scripts": {"start": "node index.js"} pe port
 
 api:
 build: ./api # Similar cu npm install din package.json
 environment:
 - DB_HOST=db # Similar cu process.env.DB_HOST
```

```bash
# Comenzi similare
npm install → docker compose build
npm start → docker compose up
npm stop → docker compose down
npm run dev → docker compose up --watch
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


### 📁 `06roWSL/` — NAT/PAT and SDN

**What you'll find relevant:**
- Integrarea rețelelor virtuale cu containere

**Recommended files:**
- `06roWSL/README.md` — overview and laboratory steps
- `06roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `06roWSL/docs/fisa_comenzi.md` — useful commands
- `06roWSL/src/` — Python code examples
- `06roWSL/homework/` — similar exercises


### 📁 `02roWSL/` — Programare Socket

**What you'll find relevant:**
- Comunicarea between noduri

**Recommended files:**
- `02roWSL/README.md` — overview and laboratory steps
- `02roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `02roWSL/docs/fisa_comenzi.md` — useful commands
- `02roWSL/src/` — Python code examples
- `02roWSL/homework/` — similar exercises


### 📁 `01roWSL/` — Fundamentele Rețelelor

**What you'll find relevant:**
- Topologii, adresare, comenzi de bază

**Recommended files:**
- `01roWSL/README.md` — overview and laboratory steps
- `01roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `01roWSL/docs/fisa_comenzi.md` — useful commands
- `01roWSL/src/` — Python code examples
- `01roWSL/homework/` — similar exercises


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
