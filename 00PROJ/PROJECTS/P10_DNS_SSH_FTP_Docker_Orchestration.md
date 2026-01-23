# Project 10: Orchestrarea serviciilor de network (DNS, SSH, FTP) cu Docker

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
https://github.com/[username]/retele-proiect-10
```

#### Required Repository Structure

```
retele-proiect-10/
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

**Format:** `NUME_Prenume_GGGG_P10_TT.zip`

| Field | Description | Example |
|------|-----------|---------|
| NUME | Family name (UPPERCASE, no diacritics) | POPESCU |
| Prenume | First name (first letter capitalised) | Ion |
| GGGG | Group number (4 digits) | 1098 |
| P10 | Project number | P10 |
| TT | Deliverable type (S1-S4 or SXX) | E1 |

**Examples for this project:**
- `POPESCU_Ion_1098_P10_E1.zip` — Stage 1
- `POPESCU_Ion_1098_P10_E2.zip` — Stage 2
- `POPESCU_Ion_1098_P10_S07.zip` — Verification săptămâna 7

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

Descriere: Proiectul numărul 10 își propune realizarea unei mici infrastructuri de network containerizate which integrează mai multe services esențiale – un server DNS, un server SSH and un server FTP – orchestrate într-un mediu Docker comun. Scopul is ca studenții să înțeleagă modules în which diferite services de network can coopera and can fi gestionate împreună using instrumente moderne de containerizare and orchestrare. Concret, team va configura trei containere principale, each rulând câte un service: - Un container DNS (using for example BIND9 or un server DNS minimalist) which să rezolve numele celorlalte services în network virtuală (for example, un nume de domeniu intern precum ftp.local towards IP-ul serverului FTP and ssh.local towards IP-ul serverului SSH). - Un container SSH (bazat pe o imagine de Linux which has un server OpenSSH instalat) permițând logarea remote securizată. Acesta va simula o mașină în which utilizatorii se can conecta through SSH. - Un container FTP (for example rulând vsftpd or using server implementat în Proiectul 9 if se dorește reutilizarea) for transfer de files.
All these containere vor fi plasate în aceeași network Docker internă, so that să poată comunica between ele through hostname-urile definite (DNS-ul custom va juca un rol crucial here). În plus, se va include un container client (or se vor folosi direct utilitare pe host) for a testa accesul la these services: for example, rularea unor comenzi nslookup towards DNS, ssh towards server SSH and ftp towards server FTP, using numele de domeniu interne stabilite. Proiectul implică thus configuration corectă a fiecărui service (zone DNS, utilizatori and chei SSH, directories and permisiuni FTP etc.), precum and scrierea unui file Docker Compose which să pornească toată suita de containere and să asigure conectivitatea lor. Un aspect important is gestionarea rețelelor Docker: se va crea o network custom (bridge network) for these services, în which DNS-ul can funcționa ca nameserver central. Studenții vor învăța cum să expună porturile serviciilor towards sistemul gazdă (if doresc acces din exterior, for example port 21 FTP, 22 SSH, 53 DNS), but accentul project is pe serviciile ce comunică between ele în interior. Se vor aborda aspecte de security and izolare: each service rulează într-un container dedicat, so that eventualele probleme ale unuia (ex. un crash or un atac asupra serverului FTP) să nu compromită direct celelalte services. Studenții vor experimenta actualizarea unei componente without a le opri pe celelalte (ex. reconfigurarea serverului DNS and repornirea containerului DNS, verificând că SSH and FTP rămân funcționale). În ansamblu, project reflectă scenariul real din administrația de sistem, la scară mică, demonstrând beneficiile containerizării în rularea serviciilor de infrastructură de network.

### 🎯 Learning Objectives


### 📖 Key Concepts

Technologies Involved: Docker and Docker Compose (ultimele versiuni) vor fi instrumentele centrale. Imaginii docker: - For DNS: imagine oficială bind9 or construirea unei imagini pornind de la Debian/Alpine cu bind instalat and configurat. - For SSH: imagine linux (ex. atmoz/sftp for un setup rapid de SFTP or ubuntu:latest cu OpenSSH server configurat). - For FTP: imagine vsftpd (există imagini pregătite pe DockerHub) or un server custom (if se folosește project anterior, se creează un Dockerfile ce copiază binarul/server Python and rulează). - For testing se can folosi alpine cu utilitarele dig, ftp, ssh instalate for a executa comenzi de test. Configurări: files de zonă DNS (montate ca volum în containerul DNS), file de config vsftpd (volum la container FTP), chei SSH (volum la container SSH for persistență). Linux command-line tools: dig (DNS lookup), ping, ftp/lftp, ssh/scp, etc., for verificări. Eventual netcat for debug de ports. Git for versionare and can un Makefile for a porni/opri rapid Compose.
Legătura cu temele and kiturile săptămânilor 1–13: This project is practic încununarea multor subiecte parcurse de-a lungul semestrului, punându-le cap la cap într-un sistem complete. Legătura directă is cu săptămâna 10 – “Servicii de network: DNS, SSH, FTP în containere orchestrate cu Docker”. Conform fișei, exact asta have făcut studenții la seminarul 10, so project extinde laboratorul acela, cerând o realizare mai amplă and integrată. În that context, studenții have already cunoștințele de bază about configuration DNS (probabil s-have jucat cu dnsmasq or BIND), about configuration unui server FTP/SSH în container. Proiectul îi forțează să refacă those configuri pe cont propriu, ceea ce consolidează învățarea. Proiectul atinge and săptămâna 11 (Aplicații distribuite cu Docker Compose, Nginx etc.) because folosesc Compose for orchestrare and creează un mic ecosistem de containere – exact conceptul de microservicii studiat. Week 7 and 13 (security networks) can fi aduse în discuție: ex. în securizarea SSH (chei in loc de passwords), în izolare. Week 5 (config infrastructură) e tangential relevantă – modules în which se atribuie IP-uri containerelor e similar cu configuration unei networks virtuale. Week 8 (reverse proxy) nu e direct folosită here, deși studenții ar putea, ca extensie, să introducă and un proxy invers în fața FTP for a securiza conexiunile, but nu is necesar. Una peste alta, project se bazează intens pe seminarele 9-11, integrând totodată cunoștințe de la început (protocoluri de bază) and de la final (administrare securizată). Is ultimul pas before de project final, so se potrivește ca nivel de dificultate cumulativă.
Structură în 4 stages:
Extensii for teams de 3 vs. teams de 2/1: O team de 3 students va putea aborda project într-un mod mai cuprinzător, posibil integrând services adiționale or configurări mai complexe. De example, o extensie valoroasă for echipele mari ar fi adăugarea unui proxy invers and server web la infrastructură: implementation unui container cu Nginx configurat ca reverse proxy for server FTP (transformând accesul la files într-un service web HTTP) or for a oferi o interfață web towards un depozit de files. Aceasta ar demonstra cunoștințele din project 8 integrate here. Totodată, echipele de 3 ar putea configura replicare DNS – adică să aibă un al doilea container DNS ca slave for zona, simulând redundanța. Un alt aspect de extins is security: for example, implementation SSL/TLS for service FTP (FTPS) and for service SSH forțarea autentificării through chei and dezactivarea parolelor, plus eventuale iptables rules în containere (deși network e izolată). Echipele mai numeroase ar putea automatiza testele cu un script which rulează în containerul client and raportează succesele (facilitând check). Tot ele ar putea documenta modules de recuperare în caz de eșec: ex. if DNS-ul cade, cum se reconfirmă rezolvarea (script de healthcheck în Compose). For echipele de 1-2 students, focalizarea va fi pe a makes cele 3 services să funcționeze corect împreună conform cerințelor de bază, without neapărat a adăuga componente extra. Un student singur ar putea alege să folosească imagini already existente and să integreze totul mai degrabă decât să construiască imagini de la zero, ceea ce e acceptabil if configuration is however personalizată. Complexitatea orchestratului can fi redusă: for example, if întâmpină dificultăți majore cu DNS-ul custom, un student ar putea folosi DNS-ul intern al Docker (which rezolvă numele containerelor after service name), deși nu e atât de educativ – however, minim ar trebui să demonstreze că numele DNS funcționează. Diferența de assessment va ține cont de these aspecte: echipele mari, through implementările and extensiile lor, vor arăta o stăpânire mai bună a subiectului and vor fi punctate în consecință, while echipele mici vor fi apreciate for simplitatea functional and claritatea cu which acoperă requirements esențiale.

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

Mockapetris, P. V. (1987). Domain names - Implementation and Specification. RFC 1035 (IETF). https://doi.org/10.17487/RFC1035
Burns, B., Grant, B., Oppenheimer, D., Brewer, E., & Wilkes, J. (2016). Borg, Omega and Kubernetes. Communications of the ACM, 59(5), 50-57. https://doi.org/10.1145/2890784
Yazán, A., Tipantuña, C., & Carvajal-Rodriguez, J. (2024). Containers-Based Network Services Deployment: A Practical Approach. Enfoque UTE, 15(1), 36-44. https://doi.org/10.29019/enfoqueute.1005
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

---

## 📚 RELEVANT LABORATORY MATERIALS

Consultă these resurse din arhiva **netROwsl** for conceptele necesare:


### 📁 `11roWSL/` — FTP, DNS, SSH

**What you'll find relevant:**
- Configuration BIND, vsftpd, OpenSSH

**Recommended files:**
- `11roWSL/README.md` — overview and laboratory steps
- `11roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `11roWSL/docs/fisa_comenzi.md` — useful commands
- `11roWSL/src/` — Python code examples
- `11roWSL/homework/` — similar exercises


### 📁 `10roWSL/` — Servicii de Network

**What you'll find relevant:**
- Docker Compose, orchestrare multi-container

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
