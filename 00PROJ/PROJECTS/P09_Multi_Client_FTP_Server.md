# Project 09: Server FTP simplificat and testing multi-client cu containere

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
https://github.com/[username]/retele-proiect-09
```

#### Required Repository Structure

```
retele-proiect-09/
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

**Format:** `NUME_Prenume_GGGG_P09_TT.zip`

| Field | Description | Example |
|------|-----------|---------|
| NUME | Family name (UPPERCASE, no diacritics) | POPESCU |
| Prenume | First name (first letter capitalised) | Ion |
| GGGG | Group number (4 digits) | 1098 |
| P09 | Project number | P09 |
| TT | Deliverable type (S1-S4 or SXX) | E1 |

**Examples for this project:**
- `POPESCU_Ion_1098_P09_E1.zip` — Stage 1
- `POPESCU_Ion_1098_P09_E2.zip` — Stage 2
- `POPESCU_Ion_1098_P09_S07.zip` — Verification săptămâna 7

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

Descriere: This project se concentrează pe realizarea unui service de transfer de files în network, similar ca principiu cu protocol FTP (File Transfer Protocol), however într-o versiune simplificată and adaptată for scop didactic. Studenții vor implementa un server de files which can gestiona connections de la mai mulți clients simultan, permițând acestora să listeze fișierele disponibile pe server and să descarce or încărceze files. Protocolul implementat can fi inspirat de FTP clasic – cu o connection de control through which se transmit comenzi precum LIST, GET (download), PUT (upload) and eventual o connection separată de date for transferul efectiv al fișierelor – or can fi o variantă simplificată ce folosește o singură connection TCP atât for comenzi cât and for date (for a reduce complexitatea). Indiferent de arhitectura aleasă, accentul va fi pus pe tratarea concurenței (mulți clients can cere simultan files), pe integritatea transferurilor and pe gestionarea erorilor (de ex., if un client cere un file inexistent, server trimite un mesaj de eroare adecvat). After implementation serverului and a unui client elementar de test (or folosirea unui client generic de telnet/FTP if protocol e compatibil), project trece la a doua componentă majoră: testing and assessment în mediu multi-client using containere Docker. Practic, team va crea un mediu de test automatizat în which mai multe instanțe de client (realizate fie ca scripturi, fie using imagini Docker which rulează comenzi de transfer) se conectează la server FTP implementat, for a demonstra că acesta can deservi concomitent mai mulți utilizatori and for a măsura performanța (ex. timp de răspuns, lățime de bandă utilizată, eventual detectarea condițiilor de bottleneck). Se urmărește ca studenții să deprindă utilizarea containerelor for simularea unui mediu de network complex: for example, se can folosi Docker Compose for a lansa un container server and N containere client, each client executând un set de operațiuni (download/upload) towards server. Thus, testele can evidenția cum crește timpul de transfer când mai mulți clients descarcă același file simultan (limitare de lățime de bandă) or cum server makes față la cereri paralele (through thread-uri or procese multiple). Pe latura educațională, project oferă o înțelegere solidă a protocolului FTP and a problemelor practice precum segmentarea fișierelor, confirmarea primirii datelor, gestionarea directorilor, but and o perspectivă asupra orchestrării containerelor for teste. Studenții vor învăța importanța sincronizării accesului la resurse comune (for example, două transferuri simultane which scriu în același file pe server can cauza probleme ce must evitate) and vor acumula experiență în dezvoltarea de applications client-server solide.

### 🎯 Learning Objectives


### 📖 Key Concepts


### 🛠️ Technologies and Tools

Legătura cu temele and kiturile săptămânilor 1–13: Proiectul is strâns legat de weeks de curs/laborator în which s-have discutat protocoalele de aplicatie and programarea pe socket-uri. În special, săptămâna 3 and 4 – “Programare pe socket-uri: implementation unui server concurent TCP and UDP and a clienților aferenți plus analiza traficului” – oferă baza for implementation serverului FTP: în those laboratoare studenții have scris servers concurrente simple (de chat, for example) and now aplică aceleași principii într-un context mai complex de transfer de files. Week 5 (“Adresare and rutare; introducere simulator de network; configuration infrastructură”) a pregătit studenții în configuration mediilor de network, cunoștințe utile for înțelegerea modului în which Docker conectează containerele într-o network virtuală izolată (conceptual similar cu un simulator de network). Week 8 (services Internet – implementation server HTTP) is înrudită, because and there s-a implementat un protocol textual client-server; experiența dobândită la project 8 can fi reutilizată here and viceversa. În mod deosebit, săptămâna 9 is direct relevantă: la seminarul 9 studenții have experimentat cu un server FTP custom and testing multi-client în containere – practic exact ceea ce makes obiectul project, so project consolidează and extinde laboratorul 9. Studenții can folosi even soluțiile or ideile din kitul săptămânii 9 ca point de plecare, îmbunătățindu-le. Mai mult, project atinge and conceptele de orchestrare din săptămâna 11 (containere multiple cu Docker Compose) când vine vorba de a porni întregul mediu de test. Week 13 (security în networks) can fi tangential implicată if discutăm aspecte de securizare a FTP (protocol notoriu for transmiterea parolelor in clar – if team implementează authentication, can discuta about this risc and about FTP Secure etc., deși implementation efectivă de encryption e în afara scopului). Per ansamblu, project is un excelent example de integrare a cunoștințelor de networks (socket-uri, protocols, concurrency) cu cele de inginerie software (utilizarea containerelor, testing automatizată) dobândite pe parcursul semestrului.
Structură în 4 stages:
Extensii for teams de 3 vs. teams de 2/1: For echipele de 3 students, se așteaptă o abordare mai cuprinzătoare a project, eventual cu implementation unor caracteristici suplimentare față de requirements de bază. De example, o team mare ar putea introduce authentication pe server FTP simplificat: clienții must să trimită un nume de utilizator and o password la început (ex. comanda USER and PASS ca în FTP), iar server verifică datele (într-un file de config simple) before de a permite accesul la comenzi. Aceasta aduce în discuție and gestiunea permisiunilor – team ar putea implementa and conceptul de directories home separate for utilizatori (or at least restricționarea accesului la anumite files). O altă extensie posibilă for 3 members is compatibilitatea cu un client FTP existent: for example, ajustarea protocolului and a formatului mesajelor so that un client standard (FileZilla or linia de comandă ftp) să poată realiza at least operațiile elementare (LIST, RETR, STOR) cu server lor. Aceasta ar necesita eforturi de conformitate cu RFC 959 (standardul FTP), but ar fi very instructiv. Totodată, echipele de 3 ar trebui să pună accent and pe aspecte de security: can implementa un mod pasiv în which server deschide un port dinamic for transfer de date (mai apropiat de FTP-ul original) or can adăuga o funcționalitate de checksum la finalul transferurilor for check integrității (client trimite hash-ul fișierului încărcat, server îl compară cu hash-ul local calculat). În ceea ce privește testing, echipele mari ar putea crește nivelul de complexitate: for example, să testeze cu 10-15 containere client rulând simultan or să folosească un utilitar de testing automată a performanței (scripting cu expect or pexpect for a simula interacțiuni reale). În schimb, echipele de 1-2 students se can limita la requirements esențiale: server concurent, transfer corect de files, teste cu ~3 clients simultani. For aceștia, focusul ar fi pe a livra o implementation stabilă and bine documentată a cerințelor de bază, lăsând aspectele precum autentificarea or compatibilitatea extinsă ca discuție teoretică la prezentare, nu neapărat implementate. Indiferent de mărimea echipei, calitatea codului (structurare, claritatea protocului), a testelor and capacitatea de a interpreta rezultatele is fundamentală and va fi criteriul main de assessment, extensiile being un bonus ce reflectă efortul suplimentar al echipelor mai numeroase.

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

Postel, J. B., & Reynolds, J. K. (1985). File Transfer Protocol (FTP). RFC 959 (IETF). https://doi.org/10.17487/RFC0959
Ponmalar, P. P., & Elakkiya, G. (2023). Multiple Client-Server Communication Using Socket in Python. International Journal of Science and Research, 12(4), 253-256. https://doi.org/10.21275/SR23326120021
Boettiger, C. (2015). An introduction to Docker for reproducible research. ACM SIGOPS Operating Systems Review, 49(1), 71-79. https://doi.org/10.1145/2723872.2723882
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


### 📁 `11roWSL/` — FTP, DNS, SSH

**What you'll find relevant:**
- Protocolul FTP, comenzi, transfer files

**Recommended files:**
- `11roWSL/README.md` — overview and laboratory steps
- `11roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `11roWSL/docs/fisa_comenzi.md` — useful commands
- `11roWSL/src/` — Python code examples
- `11roWSL/homework/` — similar exercises


### 📁 `02roWSL/` — Programare Socket

**What you'll find relevant:**
- Server concurent, threading/async

**Recommended files:**
- `02roWSL/README.md` — overview and laboratory steps
- `02roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `02roWSL/docs/fisa_comenzi.md` — useful commands
- `02roWSL/src/` — Python code examples
- `02roWSL/homework/` — similar exercises


### 📁 `09roWSL/` — Nivelul Sesiune

**What you'll find relevant:**
- Authentication, sesiuni utilizator

**Recommended files:**
- `09roWSL/README.md` — overview and laboratory steps
- `09roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `09roWSL/docs/fisa_comenzi.md` — useful commands
- `09roWSL/src/` — Python code examples
- `09roWSL/homework/` — similar exercises


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
