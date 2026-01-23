# Project 16: Analiza traficului HTTP using Wireshark

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
https://github.com/[username]/retele-proiect-16
```

#### Required Repository Structure

```
retele-proiect-16/
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

**Format:** `NUME_Prenume_GGGG_P16_TT.zip`

| Field | Description | Example |
|------|-----------|---------|
| NUME | Family name (UPPERCASE, no diacritics) | POPESCU |
| Prenume | First name (first letter capitalised) | Ion |
| GGGG | Group number (4 digits) | 1098 |
| P16 | Project number | P16 |
| TT | Deliverable type (S1-S4 or SXX) | E1 |

**Examples for this project:**
- `POPESCU_Ion_1098_P16_E1.zip` — Stage 1
- `POPESCU_Ion_1098_P16_E2.zip` — Stage 2
- `POPESCU_Ion_1098_P16_S07.zip` — Verification săptămâna 7

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

Descriere: This project constă în examinarea detaliată a comunicării HTTP through capturarea and analiza pachetelor de network. Studenții vor configura un mediu de test (for example, un server web simple and un browser web client) and vor folosi Wireshark for a captura traffic HTTP. Se va observa structura cererilor and răspunsurilor HTTP, incluzând antetele, codurile de stare and conținutul transmis. Scopul is de a înțelege în mod practic modules de funcționare al protocolului HTTP la nivel de packet and de a evidenția importanța elementelor precum metodele HTTP (GET/POST), codurile de stare (200, 404 etc.) and lipsa criptării pe HTTP. Analiza comparativă a traficului can include and diferențe between HTTP and HTTPS, subliniind necesitatea securizării comunicațiilor web. Proiectul has un caracter aplicativ, ajutând la consolidarea cunoștințelor teoretice about protocol HTTP through experimentare directă cu instrumente de analiză a network.

### 🎯 Learning Objectives


### 📖 Key Concepts

Technologies Involved: Wireshark (analizor de packets), un browser web (or utilitar HTTP precum curl), eventual un server web simple (ex: Python HTTP server or Apache local) for generarea traficului, protocol TCP/IP (suport for transportul HTTP), sistem de operare for rularea experimentelor (Windows/Linux), connection de network localhost or LAN for testing.
Legătura cu weeks and kiturile: Proiectul valorifică cunoștințele predate în săptămâna 1 (fundamentele rețelelor and instrumente de monitorizare) and săptămâna 10 (nivelul application – protocol HTTP). Se bazează pe kitul de captură and analiză a traficului introdus la laboratorul din săptămâna 1 (configuration Wireshark, utilitare de generare traffic) and aplică în practică conceptele teoretice about HTTP discutate în cursul din săptămâna 10. Studenții vor folosi abilitățile de filtrare and interpretare a pachetelor dobândite anterior for a realiza this project.
Structura pe 4 stages: 1. Stage 1: Pregătirea mediului and documentarea. În prima stage, team se familiarizează cu protocol HTTP (revizuind specificațiile de bază and examples) and instalează/configurează instrumentele necesare (Wireshark, server web local if is cazul). Se definește scenariul de test – for example, descărcarea unei pagini web simple – and se verifică conectivitatea between client and server. 2. Stage 2: Capturarea traficului HTTP. Se execută scenariul de test configurat, generând traffic HTTP (for example, accesarea paginii web de test through browser). Wireshark is folosit for a captura pachetele în timpul comunicării. Echipa aplică filtre adecvate (de ex. http or port 80) for a izola pachetele relevante. Se salvează capturile for analiza ulterioară. 3. Stage 3: Analiza and interpretarea datelor. În this stage, team inspectează în detaliu pachetele capturate. Se identifică cererea HTTP (linia de cerere, antetele trimise de client) and răspunsul HTTP (linia de status, antetele serverului and eventual corpul mesajului). Se analizează campurile importante precum URL-ul solicitat, code de status al răspunsului, tipul de conținut, lungimea conținutului etc. Totodată, se urmărește succesiunea pachetelor for a înțelege handshake-ul TCP initial and terminarea conexiunii. If se compară HTTP cu HTTPS, se observă că pachetele HTTPS has criptate (datele din payload nu has în clar). Se notează constatările, eventual cu capturi de ecran din Wireshark adnotate. 4. Stage 4: Concluzii and documentare. Echipa interpretează rezultatele analizei, formulând concluzii about modules de funcționare al HTTP and aspectele de security. De example, se can evidenția cum informațiile (inclusiv eventuale credențiale) circulă în clar through HTTP and riscurile asociate, respectiv beneficiile trecerii la HTTPS. Se elaborează raportul final al project, which va include descrierea metodologiei, capturi relevante ale pachetelor and explicațiile lor, precum and concluzii privind înțelegerea aprofundată a protocolului. Raportul va fi redactat academic, cu referiri la conceptele teoretice and bibliografia de specialitate.

### 🔮 VERIFICARE ÎNȚELEGERE

Before de a continua, răspundeți:

1. Ce tip de address is 192.168.1.50?
 → Address privată (RFC 1918)

2. Câte addresses IP utilizabile has într-o network /24?
 → 254 (256 - 1 network - 1 broadcast)

3. Ce code HTTP indică "resursă negăsită"?
 → 404 Not Found


📊 PEER INSTRUCTION

Întrebare: Ce makes NAT (Network Address Translation)?

A) Criptează traffic
B) Traduce addresses private în publice ✓
C) Alocă addresses automat
D) Filtrează packets

Explicație: NAT permite dispozitivelor cu IP privat să acceseze Internetul.


### 📊 Extensii for teams de 3/2/1: - Teams de 3 persons: Pe lângă scenariul de bază, se va analiza traffic for varietate de cazuri HTTP. De example, team can realiza capturi for o cerere POST (trimiterea unui formular) or descărcarea unui file and va compara these tipuri de traffic cu cererile GET. Totodată, se va include o analiză comparativă HTTP vs HTTPS, arătând exact ce informații has vizibile în HTTP but ascunse în HTTPS (through realizarea unei capturi Wireshark pe accesarea aceluiași site through HTTP and then through HTTPS). This extensie demonstrează înțelegerea aprofundată a securității comunicațiilor web. - Teams de 2 persons: Se va realiza scenariul standard descris mai sus, concentrându-se pe o singură interacțiune HTTP (for example, accesarea unei pagini web) and analiza detaliată a acesteia. Echipa va evidenția componentele cererii and răspunsului and va discuta problemele de security, but complexitatea cazurilor analizate can fi mai redusă decât la echipele de 3 (for example, se can omite compararea cu HTTPS if timpul nu permite). - Teams de 1 person: Proiectul va fi redus ca amploare – for example, analiza unei tranzacții HTTP very simple (cum ar fi o singură cerere GET towards un server local and răspunsul aferent). Studentul individual va captura traffic and va identifica elementele esențiale (metoda, URL, code status, antete principale), elaborând un scurt report. Extensiile opționale (compararea mai multor metode HTTP or HTTPS) nu has obligatorii for team de o person, however can fi menționate ca parte din concluzii teoretice.


### ❓ ÎNTREBĂRI FRECVENTE - HTTP/WIRESHARK

Q: Nu văd niciun traffic HTTP în Wireshark
A: Verificați:
 - Interfața selectată (for localhost, folosiți loopback/lo)
 - Filtrul aplicat (http or tcp.port == 80)
 - Că server and client has pornite

Q: Traficul HTTPS apare ca date criptate, nu can vedea conținutul
A: Is comportamentul normal and corect al HTTPS. For debugging:
 - Folosiți HTTP for teste locale (nu în producție!)
 - Or configurați Wireshark cu cheile TLS (advanced)

Q: Cum pornesc rapid un server HTTP for teste?
A: Python oferă un server simple:
 python3 -m http.server 8080
 Then accesați http://localhost:8080


### 📚 Bibliografie

Fielding, R. T., Gettys, J., Mogul, J. C., Frystyk, H., Masinter, L., Leach, P., & Berners-Lee, T. (1999). Hypertext Transfer Protocol – HTTP/1.1. RFC 2616, IETF. DOI: 10.17487/RFC2616
Luthfansa, Z. M., & Rosiani, U. D. (2021). Pemanfaatan Wireshark untuk Sniffing Komunikasi Data Berprotokol HTTP pada Jaringan Internet. Journal of Information Engineering and Educational Technology, 5(1), 34–39. DOI: 10.26740/jieet.v5n1.p34-39
---

## 🔮 Verification înțelegere — HTTP

Before de a captura traffic:

1. **Câte packets TCP apar for o cerere HTTP GET?**
 - 3 handshake + request + response + FIN = minim 6-8 packets

2. **Ce code de status indică "resursă negăsită"?**
 - 404 Not Found

3. **Ce diferență există between HTTP and HTTPS în Wireshark?**
 - HTTP: conținut vizibil în clar
 - HTTPS: date criptate TLS

---

## 📊 Peer Instruction — HTTP

**Întrebare:** Ce înseamnă code HTTP 301?

- A) Cerere reușită (OK)
- B) Resursă mutată permanent (redirect) ✓
- C) Eroare de server
- D) Resursa nu există

**Explicație:** 2xx=Success, 3xx=Redirect, 4xx=Client error, 5xx=Server error


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


### 📁 `07roWSL/` — Interceptarea Pachetelor

**What you'll find relevant:**
- Wireshark, filtre de display and capture

**Recommended files:**
- `07roWSL/README.md` — overview and laboratory steps
- `07roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `07roWSL/docs/fisa_comenzi.md` — useful commands
- `07roWSL/src/` — Python code examples
- `07roWSL/homework/` — similar exercises


### 📁 `08roWSL/` — Server HTTP

**What you'll find relevant:**
- HTTP request/response, headers, status codes

**Recommended files:**
- `08roWSL/README.md` — overview and laboratory steps
- `08roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `08roWSL/docs/fisa_comenzi.md` — useful commands
- `08roWSL/src/` — Python code examples
- `08roWSL/homework/` — similar exercises


### 📁 `10roWSL/` — HTTPS

**What you'll find relevant:**
- TLS handshake, certificate inspection

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
