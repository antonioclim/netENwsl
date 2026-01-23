# Project 18: Application de chat client-server using socket-uri TCP

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
https://github.com/[username]/retele-proiect-18
```

#### Required Repository Structure

```
retele-proiect-18/
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

**Format:** `NUME_Prenume_GGGG_P18_TT.zip`

| Field | Description | Example |
|------|-----------|---------|
| NUME | Family name (UPPERCASE, no diacritics) | POPESCU |
| Prenume | First name (first letter capitalised) | Ion |
| GGGG | Group number (4 digits) | 1098 |
| P18 | Project number | P18 |
| TT | Deliverable type (S1-S4 or SXX) | E1 |

**Examples for this project:**
- `POPESCU_Ion_1098_P18_E1.zip` — Stage 1
- `POPESCU_Ion_1098_P18_E2.zip` — Stage 2
- `POPESCU_Ion_1098_P18_S07.zip` — Verification săptămâna 7

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

Descriere: Proiectul propune dezvoltarea unei applications simple de tip chat (mesagerie în timp real) which funcționează pe arhitectura client-server using socket-uri de network. În esență, se va implementa un server which acceptă connections de la mai mulți clients and retransmite mesajele primite towards toți participanții (un chat în grup în linie de comandă). Clienții vor fi applications which se conectează la server through TCP and trimit/recepționează mesaje text. Scopul project is de a oferi studenților o experiență practică în programarea pe socket-uri and gestionarea comunicării concurente, ilustrând modules în which datele aplicative circulă through network and cum se can construi un service de comunicații în timp real. Proiectul pune accent pe conceptele de bază: conectarea la un server through address IP and port, schimbul de mesaje through intermediul fluxurilor TCP, tratarea evenimentelor de network (noutăți, deconectări) and închiderea corectă a conexiunilor.

### 🎯 Learning Objectives


### 📖 Key Concepts

Technologies Involved: Un limbaj de programare suportând socket-uri – Python (recomandat, datorită simplității, using modulul socket and eventual threading/asyncio) or alternativ Java, C#, C etc. Biblioteci standard de network. Eventual bibliotecă de threading or async a limbajului. Wireshark or utilitare de network for testing (optional, for a vizualiza traffic). Mediul de dezvoltare la alegere (PyCharm, Eclipse, etc.). Protocolul TCP/IP va fi folosit la nivel de transport, iar application definește un protocol simple la nivel de conținut al mesajelor.
Legătura cu weeks and kiturile: This project se bazează pe cunoștințele acumulate în săptămâna 3 (Introducere în programarea de network – conceptul de socket) and săptămâna 8 (Nivelul transport – TCP/UDP, which oferă fundamentele teoretice about connections and ports). În laborator, seminariile 2 and 3 have acoperit programarea de bază pe socket-uri (inclusiv un server concurent TCP and comunicarea cu mai mulți clients). Kitul de pornire oferit la laborator (example de code de server and client simple) va fi punctul de plecare în realizarea project. Studenții vor extinde those examples for a implementa funcționalitatea de chat multi-client. Proiectul is thus o continuare practică a exercițiilor de laborator, demonstrând într-un mod integrat cunoștințele about socket-uri and programare concurentă în network.
Structura pe 4 stages: 1. Stage 1: Proiectarea aplicației and setarea mediului de dezvoltare. Echipa definește requirements aplicației de chat: formatul mesajelor, funcționalitățile dorite (for example, toți utilizatorii văd mesajele tuturor, posibil un prefix cu numele expeditorului). Se stabilește limbajul de programare ce va fi folosit and se configurează mediul (crearea project, check bibliotecilor de socket disponibile, eventual realizarea unui plan de class/modules). Totodată, se decide protocol textual simple (for example, mesajele trimise de server towards clients vor fi prefixate cu “[User]: mesaj”). La finalul acestei stages, se realizează o diagramă or pseudo-code which explică fluxul: client se conectează, server acceptă and pornește un fir de execuție dedicat, then any mesaj de la un client is recepționat de server and retransmis tuturor. 2. Stage 2: Implementarea serverului de chat. În this stage se scrie code for server. Serverul va crea un socket, îl va lega la un port (configurat implicit, for example 5000) and va asculta (listen) connections. Se implementează bucla de acceptare: când un client se conectează, server lansează un thread nou or o sarcină asincronă which se ocupă de comunicarea cu that client. Each thread va primi mesajele de la client asociat and le va pune la dispoziția serverului central for difuzare. Must menținută o listă înregistrată a tuturor conexiunilor clienților activi. Se acordă atenție sincronizării accesului la this listă if se folosesc thread-uri multiple. Se implementează funcționalitatea de broadcast: then când se primește un mesaj de la un client, server îl trimite tuturor celorlalți clients (or tuturor, inclusiv expeditorul, depending on decizie). Se tratează and cazul special al deconectării unui client (thread-ul asociat detectează EOF pe socket, anunță server central să elimine client din listă and se închide). 3. Stage 3: Implementarea clientului and testing comunicării. În paralel or after server, se implementează application client. Clientul va crea un socket and se va conecta (connect) la server (IP-ul serverului and port cunoscut). After conectare, client can have două componente: una de citire (which ascultă mesaje venite de la server and le afișează utilizatorului) and una de scriere (preia input de la utilizator de la consolă and trimite mesaje serverului). These componente can fi implementate fie cu thread-uri separate (un thread for recepția de mesaje, unul for trimiterea lor, for a putea funcționa concurent) fie using mecanisme non-blocante. Se testează application rulând un server and then mai mulți clients (for example, în console separate) and verificând că mesajele trimise de un client apar la ceilalți. Se vor realiza teste cu diferite scenarii: clients which trimit mesaje simultan, clients which se conectează and deconectează pe parcurs, etc., for a se asigura că server rămâne stabil and distribuie corect mesajele. 4. Stage 4: Îmbunătățiri, security and documentare. Ultima stage is dedicată eventualelor extensii opționale and întocmirii documentației. Extensiile can include implementation unor comenzi speciale (de ex. un client can trimite /exit for a ieși, iar server gestionează this eveniment) or adăugarea unui mecanism simple de login/alias so that utilizatorii să aibă nume în chat. Optional, se can discuta about security minimală a aplicației – for example, conștientizarea că mesajele circulă în clar and că application nu has authentication, menționând posibile remedieri (encryption cu TLS, passwords). Documentația va descrie structura aplicației (modules în which server and client have been implementați, eventuala diagramă de classes), protocol de comunicare text (inclusiv examples de mesaje brute) and instrucțiuni de utilizare (cum se pornește server, cum se pornesc clienții, ce rezultate se obțin). Se vor include capturi de ecran or loguri for example de la o sesiune de chat în which se văd mesajele transmise. Lucrarea se încheie cu concluzii privind experiența de programare de network dobândită and legătura between teorie (socket/TCP) and practică.
Extensii for teams de 3/2/1: - Teams de 3 persons: Se recomandă implementation unor funcționalități suplimentare which să aducă un plus de complexitate project. De example: suport for mesaje private (adresate de un client towards un anumit alt client, identificat printr-un nume or ID), o interfață grafică simple for client (using o bibliotecă GUI, if timpul permite, în locul consolei) or implementation unui protocol rudimentar de encryption a mesajelor (de tip XOR or alt algoritm simple, only for a ilustra securizarea). Any thus de extensie which implică design and code suplimentar va evidenția capacitatea echipei de a coordona o application mai complexă. Echipa de 3 can scrie teste mai ample, măsurând for example performanța serverului (câți clients can deservi, latența medie la trimiterea mesajelor) and include these observații în documentation. - Teams de 2 persons: Vor implementa versiunea standard a aplicației de chat, conform descrierii de bază: comunicare multi-client through server, interfață în consolă, distribuția tuturor mesajelor towards toți clienții. Sarcinile can fi împărțite between members (unul se ocupă preponderent de server, altul de client, then teste în comun). Extensiile complicate nu has necesare, but can fi incluse mici îmbunătățiri cum ar fi afișarea orei mesajului or curățarea elegantă a resurselor la închiderea aplicației. Se va pune accent pe solideză: de ex., tratarea eventualelor erori de network without ca application să se oprească abrupt. - Teams de 1 person: Un project individual va realiza o application de chat functional, however posibil cu limitări față de requirements complete. De example, studentul can implementa initial un chat unul-la-unu (un singur client and un server which comunică) for a stăpâni bazele, then can extinde la mai mulți clients if timpul permite. If implementation multi-client is dificilă, se can accepta o versiune cu doi clients and server (fire separate) for demonstrarea conceptului. Important is ca studentul să demonstreze că știe să folosească socket-urile and să explice în report cum ar extinde application for mai mulți utilizatori. În documentation, can fi menționate and elemente neimplementate din lipsă de timp (for example, “cum ar fi putut fi adăugat un thread suplimentar for al treilea client” etc.), arătând thus înțelegerea conceptului even if implementation practică is limitată.

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

Rhodes, B., & Goerzen, J. (2014). Foundations of Python Network Programming (Third Edition). Apress. DOI: 10.1007/978-1-4302-5855-1
Postel, J. (1981). Transmission Control Protocol – DARPA Internet Program Protocol Specification. RFC 793, IETF. DOI: 10.17487/RFC0793
---

## 🔮 Verification înțelegere — Socket-uri TCP

Before de a rula server:

1. **Ce se întâmplă if port e ocupat?**
 - Eroare: "Address already in use"
 - Soluție: `SO_REUSEADDR` or alt port

2. **Câte connections can accepta server?**
 - Depinde de `listen()` and threading

3. **Ce se întâmplă când un client se deconectează brusc?**
 - `recv()` returnează 0 bytes or excepție `ConnectionResetError`


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
- TCP sockets, server concurent

**Recommended files:**
- `02roWSL/README.md` — overview and laboratory steps
- `02roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `02roWSL/docs/fisa_comenzi.md` — useful commands
- `02roWSL/src/` — Python code examples
- `02roWSL/homework/` — similar exercises


### 📁 `03roWSL/` — Broadcast

**What you'll find relevant:**
- Mesaje towards toți utilizatorii

**Recommended files:**
- `03roWSL/README.md` — overview and laboratory steps
- `03roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `03roWSL/docs/fisa_comenzi.md` — useful commands
- `03roWSL/src/` — Python code examples
- `03roWSL/homework/` — similar exercises


### 📁 `09roWSL/` — Nivelul Sesiune

**What you'll find relevant:**
- Gestionarea sesiunilor utilizator

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
