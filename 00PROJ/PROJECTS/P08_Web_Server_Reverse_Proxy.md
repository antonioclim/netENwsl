# Project 08: Server web personalizat and proxy invers

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
https://github.com/[username]/retele-proiect-08
```

#### Required Repository Structure

```
retele-proiect-08/
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

**Format:** `NUME_Prenume_GGGG_P08_TT.zip`

| Field | Description | Example |
|------|-----------|---------|
| NUME | Family name (UPPERCASE, no diacritics) | POPESCU |
| Prenume | First name (first letter capitalised) | Ion |
| GGGG | Group number (4 digits) | 1098 |
| P08 | Project number | P08 |
| TT | Deliverable type (S1-S4 or SXX) | E1 |

**Examples for this project:**
- `POPESCU_Ion_1098_P08_E1.zip` — Stage 1
- `POPESCU_Ion_1098_P08_E2.zip` — Stage 2
- `POPESCU_Ion_1098_P08_S07.zip` — Verification săptămâna 7

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

Descriere: În this project, studenții vor construi un sistem web simplificat, format dintr-un server HTTP creat de la zero and un proxy invers plasat în fața acestuia, cu scopul de a îmbunătăți scalabilitatea and security serviciului. Practic, application constă într-un server web minimal (realizat de students, for example în Python, using socket-uri TCP) which can răspunde la cereri HTTP de bază (precum cereri GET for anumite resurse statice), iar în fața acestuia un server de tip proxy invers (precum Nginx configurat corespunzător or even o application custom) which primește cererile clienților and le redirecționează towards server backend. Proxy-ul invers can oferi funcționalități suplimentare precum cache (for a servi direct cererile repetitive without a mai deranja backend-ul), terminarea conexiunilor TLS (if se extinde project pe partea de securizare HTTPS) or echilibrarea încărcării between mai multe instanțe de server (if server web is replicat, for example, pe ports diferite). Scopul educațional al project is dublu: (1) studenții înțeleg în profunzime protocol HTTP through implementation unui server “de la firul ierbii”, parcurgând întregul flux de procesare a unei cereri web (citirea cererii brute, interpretarea header-elor HTTP, formarea unui răspuns valid conform protocolului); (2) studenții se familiarizează cu arhitectura pe mai multe straturi a aplicațiilor web moderne, unde un proxy invers acționează ca intermediar between clients and serverele de application, aducând beneficii de performanță and security. Proiectul is extrem de practic: de la rularea serverului web personalizat (for example, pornirea lui pe un anumit port and servirea unui file HTML simple) până la configuration unui proxy (for example, Nginx or Apache în mod proxy) which să preia traffic de pe port 80 and să îl redirecționeze intern towards port pe which rulează server custom. Se vor realiza teste cu browsere reale or cu utilitare precum curl, for a confirma că întreg lanțul funcționează: o cerere HTTP de la client trece through proxy, ajunge la server implementat de student, acesta generează un răspuns (for example, conținutul unui file or un mesaj dinamic), iar răspunsul se întoarce la client through proxy. Studenții vor putea observa îmbunătățirile aduse de proxy: for example, if se activează caching, a doua cerere for aceeași resursă statică nu mai ajunge la backend (proxy-ul răspunde direct), scăzând latența. Optional, se can experimenta pornirea a două instanțe ale serverului backend (pe diferite ports) and configuration proxy-ului să facă load balancing (rund robin) – optional, ca extensie – for a vedea cum se distribuie cererile. All these activități contribuie la consolidarea cunoștințelor about protocoalele web and about infrastructura serverelor web.

### 🎯 Learning Objectives


### 📖 Key Concepts

Technologies Involved: Limbaj de programare for server (Python is sugestia, using modulul socket or biblioteci web simple; alternativ Java cu servlets minime or C cu sockets – but Python va fi mai accesibil). Server proxy – de preferat Nginx, dat being că is very folosit ca reverse proxy and studenții ar beneficia să-l învețe; se vor scrie files de configuration Nginx (bloc server cu directiva proxy_pass towards backend). Optional, Docker can fi folosit for a containeriza server custom and Nginx-ul, demonstrând thus portabilitatea configurației (for example, un docker-compose cu două services: web and proxy). Instrumente de test: curl (for a trimite cereri HTTP manual and a vedea răspunsul brut), browsere web (for a testa accesul la service web through proxy), ab (ApacheBench) or wrk (for teste de performanță rudimentare, ca să compare timpi cu caching vs. without caching). For debugging, Wireshark can fi util if se doresc inspectate pachetele HTTP brute, however log-urile text ale serverelor vor fi probabil suficiente.
Legătura cu temele and kiturile săptămânilor 1–13: This project cumulează cunoștințe din mai multe weeks, în main din zona serviciilor Internet studiate after jumătatea cursului. Week 8 is direct relevantă: there studenții have parcurs implementation unui server HTTP simple and conceptul de proxy invers (probabil through examples practice cu Nginx). Proiectul extinde exact these aspecte – practic, is o aplicare amplă a tematicii de la seminarul 8. Totodată, realizarea serverului custom has legături cu weeks 2–4, când s-a discutat programarea pe socket-uri and implementation de protocols text/binar pe TCP/UDP. În those laboratoare, studenții have dobândit abilitățile tehnice de bază for a construi now un protocol ca HTTP (which is tot un protocol text bazat pe TCP) – ei have implementat can un chat TCP simple or un protoco tip echo server, iar now ridică complexitatea la nivelul unui protocol real, HTTP. Week 9, deși axată pe FTP and testing multi-client cu containere, is utilă because noțiunile de concurență and testing sub încărcare apar and here (server web must testat cu mai mulți clients simultan, similr cu testing FTP). Week 11 (Aplicații distribuite cu Nginx and Docker) is very relevantă: there studenții have văzut cum se can folosi containere multiple cu Docker Compose and un proxy for a gestiona traffic towards mai multe services – cunoștințe direct aplicabile în extensiile project (for example, containerizarea soluției or folosirea Nginx la potențial maxim). Even and săptămâna 13 (security) has legătură: se can menționa, for example, cum proxy-ul invers can oferi un point central for implementation unor politici de security (filtrarea unor URL-uri malițioase, protecție împotriva unor atacuri web simple). Thus, project servește ca punte de legătură between mai multe subiecte din fișa disciplinei: programare de network, services web, infrastructură distribuită and security, într-un tot unitar.
Structură în 4 stages:
Extensii for teams de 3 vs. teams de 2/1: Proiectul is conceput să fie modular, permițând echipelor mai mari să implementeze caracteristici adiționale which demonstrează un plus de cunoaștere. O team de 3 students, for example, ar trebui să abordeze atât partea de server custom, cât and configuration advanced a proxy-ului. Ei ar putea implementa suport for mai multe tipuri de conținut pe server web (for example, servirea dinamică a unui conținut generat pe loc – un script CGI simple or un răspuns which include data curentă, nu only files statice). Totodată, ar putea gestiona connections simultane through multithreading or multiprocessing pe server custom, asigurându-se că can deservi at least 5-10 clients concurenți without blocaje. Pe componenta de proxy, team de 3 can activa and ajusta parametri de performanță (dimensiunea cache-ului, politici de expirare) and can prezenta metrici cuantificabile (cache hit rate, reducerea load-ului pe backend). O altă extensie valoroasă is containerizarea complete a aplicației: team can furniza un file Docker Compose cu două services (backend-ul custom and Nginx) so that project să poată fi pornit ușor oriunde, consolidând totodată cunoștințele legate de săptămâna 11. For echipele mai mici (2 students or individual), se recomandă focalizarea pe requirements de bază – un singur server backend and un proxy functional – eventual without implementation echilibrării încărcării pe multiple instanțe. Un student singur, for example, ar putea decide să nu activeze TLS or authentication, concentrându-se în schimb pe asigurarea compatibilității HTTP and pe cache. Diferențierea se va vedea and în nivelul de detaliu al documentației: echipele mari can furniza o documentation mai amplă (inclusiv tutorial de deploy, scripturi de automatizare), pe când cele mici can livra un report mai succint. Esențial is că all echipele, indiferent de mărime, vor obține o mai bună înțelegere a funcționării serverelor web and a proxy-urilor, but complexitatea and polish-ul implementării vor fi mai ridicate în proiectele echipelor de 3, conform așteptărilor.

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

Fielding, R. T., & Reschke, J. (2014). Hypertext Transfer Protocol (HTTP/1.1): Message Syntax and Routing. RFC 7230 (IETF). https://doi.org/10.17487/RFC7230
Mohan, K., & Rengarajan, A. (2024). Reverse Proxy Technology. International Journal of Innovative Research in Computer and Communication Engineering, 12(2), 1067-1071. https://doi.org/10.15680/IJIRCCE.2024.1202057
Skvorc, D., & Ilakovac, V. (2014). An Educational HTTP Proxy Server. Procedia Engineering, 69, 128-132. https://doi.org/10.1016/j.proeng.2014.02.212
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

---

## 📚 RELEVANT LABORATORY MATERIALS

Consultă these resurse din arhiva **netROwsl** for conceptele necesare:


### 📁 `08roWSL/` — Server HTTP and Proxy Invers

**What you'll find relevant:**
- HTTP protocol, reverse proxy cu Nginx

**Recommended files:**
- `08roWSL/README.md` — overview and laboratory steps
- `08roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `08roWSL/docs/fisa_comenzi.md` — useful commands
- `08roWSL/src/` — Python code examples
- `08roWSL/homework/` — similar exercises


### 📁 `10roWSL/` — HTTP/S and REST

**What you'll find relevant:**
- Request/response handling, headers

**Recommended files:**
- `10roWSL/README.md` — overview and laboratory steps
- `10roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `10roWSL/docs/fisa_comenzi.md` — useful commands
- `10roWSL/src/` — Python code examples
- `10roWSL/homework/` — similar exercises


### 📁 `11roWSL/` — Load Balancing

**What you'll find relevant:**
- Distribuția cererilor between backend-uri

**Recommended files:**
- `11roWSL/README.md` — overview and laboratory steps
- `11roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `11roWSL/docs/fisa_comenzi.md` — useful commands
- `11roWSL/src/` — Python code examples
- `11roWSL/homework/` — similar exercises


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
