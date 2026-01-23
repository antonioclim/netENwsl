# Project 12: Service web distribuit în containere Docker cu echilibrare de încărcare Nginx

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
https://github.com/[username]/retele-proiect-12
```

#### Required Repository Structure

```
retele-proiect-12/
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

**Format:** `NUME_Prenume_GGGG_P12_TT.zip`

| Field | Description | Example |
|------|-----------|---------|
| NUME | Family name (UPPERCASE, no diacritics) | POPESCU |
| Prenume | First name (first letter capitalised) | Ion |
| GGGG | Group number (4 digits) | 1098 |
| P12 | Project number | P12 |
| TT | Deliverable type (S1-S4 or SXX) | E1 |

**Examples for this project:**
- `POPESCU_Ion_1098_P12_E1.zip` — Stage 1
- `POPESCU_Ion_1098_P12_E2.zip` — Stage 2
- `POPESCU_Ion_1098_P12_S07.zip` — Verification săptămâna 7

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


### 🛠️ Technologies and Tools


### 🎯 Learning Objectives


### 📖 Key Concepts


### 🛠️ Technologies and Tools

Legătura cu weeks and kiturile (WEEK1-14): This project integrează cunoștințe din partea a doua a cursului, în special cele legate de services Internet and virtualizare. Temele din săptămâna 8 (services Web and noțiuni de HTTP, proxy invers), săptămâna 9 (protocol FTP and testing multi-client cu containere), săptămâna 10 (services DNS/SSH/FTP orchestrate în container) and săptămâna 11 (applications distribuite, Nginx load balancing pe containere Docker) has direct relevante. Kitul practic de la săptămâna 11, which demonstrează utilizarea Nginx ca load balancer for applications în Docker Compose, constituie un example de bază pe which studenții îl can extinde substanțial în cadrul project. Totodată, cunoștințele generale about networks din weeks anterioare (protocol TCP, modelul client-server din weeks 2-4) has necesare for a înțelege cum comunică microserviciile between ele. Proiectul consolidează and extinde these elemente, ducându-le spre un context aplicat de tip enterprise.

### 🛠️ Technologies and Tools


### 🔮 VERIFICARE ÎNȚELEGERE - DOCKER ȘI CONTAINERE

Before de a executa comenzile, răspundeți:

1. Câte containere vor fi create conform fișierului docker-compose.yml?
 → Numărați serviciile definite în file de configuration.

2. Ce ports vor fi expuse pe host?
 → Căutați secțiunile ports: din each service.

3. Ce se întâmplă if port dorit is already ocupat de alt proces?
 → Verificați cu: ss -tlnp | grep :PORT
 → Eroare așteptată: "port is already allocated"

4. Cum comunică containerele between ele în aceeași network Docker?
 → Through numele serviciului (Docker DNS intern), nu through localhost.


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


### Extensii for teams de 3 vs. 2/1 members: În cazul unei teams de 3 students, se așteaptă o complexitate mai mare a sistemului. Aceasta can include adăugarea unui microserviciu suplimentar (for example, un service de authentication separat or un service de caching), implementation unui sistem de logare centralizată a evenimentelor (de tip ELK stack simplificat) for a monitoriza distribuția traficului or utilizarea unei scheme mai complexe de orchestrare (precum definirea unui health-check în Docker Compose for restartarea automată a containerelor nefuncționale). Totodată, echipele mai numeroase can investiga and aspecte de security, precum rularea containerelor cu privilegii restrânse, folosirea rețelelor Docker distincte for izolare or configuration HTTPS pe Nginx cu certificate auto-semnate. For echipele de 2 students or individuale, scope-ul can fi redus: de pildă, can have only două services principale (frontend and backend + DB), iar echilibrarea de încărcare să fie demonstrată between două instanțe ale backend-ului. Complexitatea configurărilor Docker can fi mai mică, concentrându-se pe funcționalitatea de bază (without optimizări elaborate de security or monitorizare). Important is ca and în varianta simplificată arhitectura pe microservicii and folosirea unui load balancer să fie prezente, even if la scară redusă, iar studenții să poată explica avantajele obținute (for example, cum adăugarea unei a doua instanțe backend îmbunătățește timpul de răspuns sub sarcină).


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

---

## 🔮 Verification înțelegere — Docker

Before de a rula comenzile, răspunde:

1. **Câte containere vor fi create conform docker-compose.yml?**
 - Numără serviciile definite în file

2. **Ce ports vor fi expuse pe host?**
 - Caută secțiunile `ports:` din each service

3. **Ce se întâmplă if port 80 e already ocupat?**
 - Verifică cu: `ss -tlnp | grep :80`
 - Eroare așteptată: "port is already allocated"

After `docker ps`, verifică că all containerele have status "Up".

---

## 📊 Peer Instruction — Docker

**Întrebare:** Containerele `web` and `db` has în aceeași network Docker. Cum se conectează `web` la `db`?

- A) `localhost:5432`
- B) `db:5432` ✓
- C) `172.17.0.1:5432`
- D) `host.docker.internal:5432`

**Explicație:** Docker DNS rezolvă automat numele serviciilor din Compose.


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


### 💡 For HTTP/REST

Din TW ai lucrat cu Express.js and REST. Now construiești de la zero:

```python
# Parsarea HTTP manual vs Express automat
# În Express: req.headers, req.body, req.params

def parse_http_request(raw_data):
 """Ce face Express automat, tu faci manual"""
 lines = raw_data.decode().split('\r\n')
 method, path, version = lines[0].split() # GET /api/users HTTP/1.1
 
 headers = {}
 for line in lines[1:]:
 if ': ' in line:
 key, value = line.split(': ', 1)
 headers[key] = value
 
 return method, path, headers

# Răspunsul HTTP manual vs res.json()
def http_response(status, body):
 """Ce face res.json() automat"""
 return f"HTTP/1.1 {status}\r\nContent-Type: application/json\r\n\r\n{body}"
```

---

## 📚 RELEVANT LABORATORY MATERIALS

Consultă these resurse din arhiva **netROwsl** for conceptele necesare:


### 📁 `11roWSL/` — Echilibrare de Sarcină

**What you'll find relevant:**
- Nginx/HAProxy, algoritmi de load balancing

**Recommended files:**
- `11roWSL/README.md` — overview and laboratory steps
- `11roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `11roWSL/docs/fisa_comenzi.md` — useful commands
- `11roWSL/src/` — Python code examples
- `11roWSL/homework/` — similar exercises


### 📁 `10roWSL/` — REST and Servicii

**What you'll find relevant:**
- Microservicii, API gateway

**Recommended files:**
- `10roWSL/README.md` — overview and laboratory steps
- `10roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `10roWSL/docs/fisa_comenzi.md` — useful commands
- `10roWSL/src/` — Python code examples
- `10roWSL/homework/` — similar exercises


### 📁 `08roWSL/` — Server HTTP

**What you'll find relevant:**
- HTTP backend-uri, health checks

**Recommended files:**
- `08roWSL/README.md` — overview and laboratory steps
- `08roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `08roWSL/docs/fisa_comenzi.md` — useful commands
- `08roWSL/src/` — Python code examples
- `08roWSL/homework/` — similar exercises


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
