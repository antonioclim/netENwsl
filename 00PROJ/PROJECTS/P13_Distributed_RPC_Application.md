# Project 13: Application distribuită bazată pe apeluri de procedură la distanță (RPC)

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
https://github.com/[username]/retele-proiect-13
```

#### Required Repository Structure

```
retele-proiect-13/
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

**Format:** `NUME_Prenume_GGGG_P13_TT.zip`

| Field | Description | Example |
|------|-----------|---------|
| NUME | Family name (UPPERCASE, no diacritics) | POPESCU |
| Prenume | First name (first letter capitalised) | Ion |
| GGGG | Group number (4 digits) | 1098 |
| P13 | Project number | P13 |
| TT | Deliverable type (S1-S4 or SXX) | E1 |

**Examples for this project:**
- `POPESCU_Ion_1098_P13_E1.zip` — Stage 1
- `POPESCU_Ion_1098_P13_E2.zip` — Stage 2
- `POPESCU_Ion_1098_P13_S07.zip` — Verification săptămâna 7

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

Descriere: În cadrul acestui project, studenții vor realiza un sistem software distribuit în which comunicarea between componente se makes through apeluri de procedură la distanță (Remote Procedure Calls – RPC). Modelul RPC permite unui program să invoce o subrutină pe un alt calculator din network ca and cum ar fi un apel local, abstractizând detaliile comunicării and ale serializării datelor[3]. Proiectul va consta într-o application multi-nod (minim două or trei noduri de network simulate) which colaborează for a îndeplini o sarcină comună, using mecanismul RPC for a-and cere services reciproc. De example, se can implementa un sistem distribuit de procesare a unor calcule: un nod client trimite cereri de calcul towards unul or mai multe noduri server through RPC, serverele procesează and trimit rezultatele înapoi. O altă idee is un service compus: un server central which agregă informații de la alți doi servers specializate (through apeluri RPC towards each) and răspunde then clientului final. Studenții can alege să folosească fie o bibliotecă/framework existent for RPC (precum gRPC, Apache Thrift, JSON-RPC, XML-RPC etc.), fie – for un nivel ridicat de dificultate – să implementeze un mini-sistem RPC simplificat (de ex. definind propriul protocol de cerere-răspuns peste TCP sockets). Folosirea gRPC (un framework modern dezvoltat de Google) is încurajată, întrucât acesta oferă un suport solid for definirea interfețelor (using files .proto for Interface Definition Language) and generează automat code de serializare/deserializare eficient (bazat pe Protocol Buffers). Proiectul va necesita proiectarea atentă a interfețelor remote: team must să decidă ce functions or metode vor fi expuse de servers for a fi apelate la distanță and ce parametri/structuri de date vor fi transmise. Se vor aborda concepte ca marshalling (codificarea datelor for transmitere) and unmarshalling (reconstrucția la recepție), tratarea erorilor de network and eventual mecanisme de time-out or reîncercare automată a apelurilor eșuate. Din point de vedere pedagogic, project evidențiază modules în which aplicațiile distribuite can fi proiectate for a fi transparente din perspectiva programatorului – acesta scrie aproape același code ca for un apel local, diferențele being ascunse de infrastructura RPC. Studenții vor deprinde modules de gândire orientat pe services remote, vor aprecia avantajele but and limitările modelului (de ex., vor observa că apelurile remote has ordine de magnitudine mai lente decât cele locale and necesită gestionarea atentă a excepțiilor and a latenței). La final, sistemul realizat va fi testat through scenarii distribuite (ex: cereri simultane de la mai mulți clients towards server, volum mărit de date transmis) and se va evalua corectitudinea and eficiența comunicării.

### 🎯 Learning Objectives


### 📖 Key Concepts

Technologies Involved: Limbajul de implementation va fi preferabil Python (există biblioteci for RPC, for example gRPC Python or Pyro4 for RPC Python-specific). Alternativ, se can folosi and alte limbaje depending on familiaritatea echipei (Java RMI, C# WCF, etc.), but Python has avantajul simplității and integrării bune cu protocols moderne. If se folosește gRPC, then se va lucra and cu files .proto and generatorul de code aferent (grpcio). For testing and monitorizare, se can utiliza scripturi de încărcare (generând multe apeluri RPC simultane) and instrumente de logging/distribuire (gRPC oferă logging intern; Wireshark can fi folosit for a inspecta pachetele if se folosește un transport cunoscut). Proiectul mai necesită configuration unui mediu de network de test – for example, se can folosi containere Docker or mașini virtuale for a rula componentele pe gazde “separate” logic. Un simple laborator se can baza even pe rularea mai multor procese pe același calculator gazdă, pe ports diferite, simulând noduri distincte.
Legătura cu weeks and kiturile (WEEK1-14): Proiectul se leagă direct de conținutul din săptămâna 12, unde s-have introdus conceptele de apeluri de metode la distanță (RPC) and s-a sugerat un framework practic. Kitul aferent săptămânii 12 oferă, probabil, un example simple de implementation RPC (can using un framework ușor or un service web cu apeluri la distanță), which va servi ca point de plecare conceptual. Proiectul se bazează pe cunoștințele acumulate în primele weeks privind programarea socket (weeks 2–4) – întrucât RPC, la nivel de transport, se bazează pe sockeți TCP/UDP – and pe noțiunile de concurență and sincronizare. În plus, elemente din săptămâna 8 (proxies, eventual REST vs. RPC) can oferi context în diferențierea abordărilor. Through realizarea acestui project, studenții adâncesc înțelegerea modului de construire a serviciilor distribuite, complementând cunoștințele dobândite about arhitecturile pe microservicii (săptămâna 11) cu o perspectivă la nivel de apel de functions.

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


### Extensii for teams de 3 vs. 2/1 members: O team de 3 students can aborda requirements suplimentare semnificative. De example, can implementa un sistem cu mai multe services interconectate: nu only un model simple client-server, ci and comunicare server-server (un server which la rândul său apelează functions la alt server, formând un lanț). Totodată, can integra un registru de services rudimentar – un nod central unde serverele se înregistrează, iar clienții cer address serviciilor (similar cu un service discovery). O altă extensie interesantă for echipele mari is implementation unui grad de toleranță la defecte: for example, replicarea unui server and realizarea unui mecanism simple de fail-over (if server main nu răspunde, client încearcă apelul la server replică). For echipele de 2 students, project can fi limitat la o interacțiune mai simple (un client and un server unic, without replici or lanțuri de apeluri). Optional, se can folosi un framework mai high-level (ex: JSON-RPC peste HTTP) for a reduce volumul de code necesar, concentrându-se pe înțelegerea conceptelor. O team de 1 student ar putea implementa un prototip minimal: for example, un server which expune 2-3 operații and un client which le apelează secvențial, without requirements de concurență ridicată. Even and în varianta simplificată, accentul se va pune pe corectitudinea apelurilor remote and pe documentarea clară a designului, mai degrabă decât pe complexitatea infrastructurii.


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


### 📁 `12roWSL/` — RPC

**What you'll find relevant:**
- gRPC, JSON-RPC, Protocol Buffers

**Recommended files:**
- `12roWSL/README.md` — overview and laboratory steps
- `12roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `12roWSL/docs/fisa_comenzi.md` — useful commands
- `12roWSL/src/` — Python code examples
- `12roWSL/homework/` — similar exercises


### 📁 `10roWSL/` — REST

**What you'll find relevant:**
- Comparație REST vs RPC

**Recommended files:**
- `10roWSL/README.md` — overview and laboratory steps
- `10roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `10roWSL/docs/fisa_comenzi.md` — useful commands
- `10roWSL/src/` — Python code examples
- `10roWSL/homework/` — similar exercises


### 📁 `02roWSL/` — Sockets

**What you'll find relevant:**
- Comunicare bidirecțională

**Recommended files:**
- `02roWSL/README.md` — overview and laboratory steps
- `02roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `02roWSL/docs/fisa_comenzi.md` — useful commands
- `02roWSL/src/` — Python code examples
- `02roWSL/homework/` — similar exercises


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
