# Project 04: Application de mesagerie securizată client-server

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
https://github.com/[username]/retele-proiect-04
```

#### Required Repository Structure

```
retele-proiect-04/
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

**Format:** `NUME_Prenume_GGGG_P04_TT.zip`

| Field | Description | Example |
|------|-----------|---------|
| NUME | Family name (UPPERCASE, no diacritics) | POPESCU |
| Prenume | First name (first letter capitalised) | Ion |
| GGGG | Group number (4 digits) | 1098 |
| P04 | Project number | P04 |
| TT | Deliverable type (S1-S4 or SXX) | E1 |

**Examples for this project:**
- `POPESCU_Ion_1098_P04_E1.zip` — Stage 1
- `POPESCU_Ion_1098_P04_E2.zip` — Stage 2
- `POPESCU_Ion_1098_P04_S07.zip` — Verification săptămâna 7

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
În this project, studenții vor dezvolta o application de chat client-server criptată, punând accent pe securizarea comunicațiilor în network. Practic, se va implementa un server de mesagerie multi-client and un client de chat, using Python (or alt limbaj de nivel înalt), which comunică peste TCP. Spre deosebire de aplicațiile de chat simple, project de față va integra mecanisme de encryption end-to-end or pe canal, asigurând confidențialitatea mesajelor transmise. Initial, application can funcționa în mod text (consolă) – utilizatorii se conectează la server and can trimite mesaje text which has distribuite celorlalți (chat în grup simple) or direct towards un alt utilizator (chat privat), depending on specificațiile echipei.
For security, se can folosi fie criptografie simetrică (ex: algoritmul AES cu o cheie pre-partajată between client and server) fie o abordare cu criptografie asimetrică (ex: server has o cheie publică/privată RSA; clienții negociază o cheie de sesiune, similar cu un handshake TLS simplificat). Un design fezabil is implementation unui protocol simple de tip SSL: la conectare, client preia certificatul public al serverului (auto-semnat, generat în prealabil) and îl folosește for a trimite în siguranță o cheie simetrică random (cheia de sesiune). Ulterior, all mesajele client-server has criptate simetric cu acea cheie. Serverul, având cheia privată for a descifra cheia de sesiune, can then citi mesajele and le can retransmite altor clients, eventual recriptând pe canalul cu each destinatar. Alternativ, for simplitate, toți participanții can folosi aceeași cheie simetrică (pre-definită în code) – mai puțin sigur, but mai ușor de implementat, adecvat for a demonstra conceptul.
Proiectul implică așadar atât dezvoltarea funcționalităților de bază ale unui chat (gestionarea conexiunilor multiple, transmiterea and afișarea mesajelor în timp real), cât and integrarea bibliotecilor de criptografie (cum ar fi ssl din Python or biblioteci precum PyCryptodome) for a asigura că mesajele has inteligibile only for părțile autorizate. Se vor realiza teste într-o network locală (or pe același calculator, cu mai multe instanțe de client) for a verifica că mesajele interceptate (for example, cu Wireshark) apar criptate and nu în clar. This project oferă o introducere practică în protocoalele de security and evidențiază importanța criptării datelor transmise peste network.

### 🎯 Learning Objectives

Consolidarea cunoștințelor de programare a socket-urilor în model client-server, gestionând concomitent comunicarea cu mai mulți clients (ex. using fire de execuție or mecanisme de multiplexare I/O).
Însușirea principiilor de bază ale criptografiei aplicate în networks: encryption simetrică vs. asimetrică, schimb de chei, certificate and modules de integrare a acestora într-un protocol de comunicație.
Înțelegerea noțiunilor de confidențialitate and integritate a datelor transmise through network and a riscurilor then când acestea lipsesc (ex: interceptarea traficului în clar).
Dezvoltarea unei mici convenții de protocol personalizat (stabilirea formatului mesajelor, eventual comenzi precum "/login", "/list" for listarea utilizatorilor, etc.) and respectarea acestei specificații în implementation.

### 🛠️ Technologies and Tools


### 📖 Key Concepts

Modelul Client-Server – connection TCP persistentă, rolul serverului de releu between clients, concurență (threads or async) for a servi mai multe connections simultan.
Protocoale criptografice – schimbul de chei, encryption simetrică (ex: AES CBC/GCM), encryption asimetrică (RSA) and utilizarea lor combinată (precum în TLS).
Managementul cheilor – generarea and distribuția cheii de encryption, stocarea în siguranță a cheilor private, eventual folosirea certificatelor digitale.
Integritatea mesajelor – optional, se can discuta/adăuga calculul unui MAC (HMAC) for each mesaj, for a asigura integritatea and autenticitatea (but if se folosește un mod autenticat de encryption precum AES-GCM, integritatea e asigurată implicit).
Aplicații de nivel transport – cum se delimitează mesajele într-un flux TCP (folosirea unui protocol text cu terminator de linie or a unui protocol binar cu length-prefix), gestiunea erorilor de network, reconectarea clienților etc.
Technologies Involved
Python – limbaj ideal for prototipare rapidă: utilizarea modulului socket for comunicații TCP, modulelor threading or asyncio for concurență and biblioteca ssl or PyCryptodome for functions criptografice.
Biblioteci de criptografie – for example ssl (can fi folosit for a îmbrăca un socket existent într-un context SSL simplificat) or PyCryptodome for implementation manuală a algoritmilor (AES, RSA).
OpenSSL – se can folosi for a genera cheia privată and certificatul autosigiliat al serverului (folosit if se implementează varianta cu RSA). De example, comanda openssl genrsa and openssl req -x509 for a obține un certificat .pem pe which server îl încarcă.
Wireshark – for testing securității: through capturarea pachetelor se va verifica if textul mesajelor nu apare în clar. If se configurează Wireshark cu cheia privată a serverului (în variantă RSA), se can tenta decriptarea traficului for a confirma că numai cu cheia corespunzătoare se can citi conținutul.
Protocol propriu – definirea unui format, for example JSON peste TCP (each mesaj JSON conține câmpuri "user", "msg", "timestamp", criptate ca text) or un protocol text simple (linie de text per mesaj, criptată la nivel de flux).
Connection to Weekly Course Topics
Week 7: Protocolul TCP – application de chat folosește TCP for transport fiabil; cunoștințele about connections, ports, segmentare and reasamblare (din curs) has aplicate direct.
Week 8: Protocoale de application – se leagă de subiectul protocoalelor de nivel înalt: here definim practic un mini-protocol de chat. Totodată, conceptul de protocol securizat (similar relației HTTP-HTTPS, here chat vs. chat securizat) extinde discuția din curs privind securizarea protocolelor de application.
Week 9: Security – project is o application practică a criptografiei în network, completând teoria din curs (ex: if în Week9 s-a discutat about TLS/SSL, certificate, criptografie, project exemplifică these lucruri).
Week 12: Programare de network – baza codului de chat necriptat is direct inspirată din exemplele de socket programming din laboratorul săptămânii 12 (vezi „Chat server Python” din arhiva WEEK12), peste which se adaugă partea de encryption.
Etapele project

### 📋 Stage 1 (Week 5) – Proiectarea protocolului and a funcționalităților: Stabilirea caracteristicilor aplicației: va fi chat de grup or privat? Cum se vor identifica utilizatorii (ex: printr-un nume de utilizator trimis la conectare)? Ce algoritmi de encryption se vor folosi and cum vor fi gestionați cheile? Se va întocmi un mini-schelet de protocol descriind pașii de inițializare (ex: Client -> Server: salut + nume user; Server -> Client: confirmare + certificatul public; Client -> Server: cheie de sesiune criptată etc.) and formatul mesajelor ulterioare. Livrabil: un document de design which include diagrama de flux a protocolului de comunicare (atât partea de authentication/cripto initial, cât and fluxul de mesaje de chat), plus detalii about alegerea algoritmilor (for example, “vom folosi AES-256-CBC cu o cheie simetrică de 32 bytes generată aleator de client la each sesiune” or alt plan). Se vor alege librăriile and se va pregăti mediul (instalarea PyCryptodome if e necesar). Optional, se can livra and generarea cheilor/certificatelor necesare (un file PEM cu cheia privată a serverului and certificatul public autosemis).


### 🔨 Stage 2 (Week 9) – Implementation bază (chat necriptat): Ca prim pas, se implementează chat-ul propriu-zis without encryption, for a asigura că logica de network funcționează corect. Serverul must să accepte connections multiple (thread pe connection or un mecanism asincron) and să retransmită mesajele primite de la un client towards toți ceilalți (or towards destinatarii vizați, if se suportă mesaje private). Clientul must să citească de la tastatură mesaje and să le trimită serverului, afișând at the same time mesajele primite de la alții. Livrabil: code sursă al serverului and al clientului (posibil într-o formă simple, ex. rulare în consolă) which permite already comunicarea tip chat. Se vor furniza capturi de ecran or log-uri ce demonstrează 2-3 clients trimițând mesaje unii altora through intermediul serverului. În this stage, mesajele has în clar, so e util for testing să se confirme că toată lumea primește corect mesajele.


### 🔮 VERIFICARE ÎNȚELEGERE - SOCKET-URI TCP

Before de a rula server, răspundeți:

1. Ce se întâmplă if port specificat is already ocupat?
 → Eroare: Address already in use
 → Soluție: folosiți SO_REUSEADDR or alegeți alt port

2. Câte connections can gestiona server simultan?
 → Depinde de parametrul backlog din listen() and de implementation cu thread-uri

3. Ce se întâmplă când un client se deconectează brusc?
 → Serverul primește 0 bytes la recv() or excepție ConnectionResetError


### ✅ Stage 3 (Week 13) – Implementation security and testing complete: Se integrează mecanismele de encryption proiectate în Stage 1. For varianta cu cheie simetrică comună, asta înseamnă că atât server cât and clienții includ acea cheie and o folosesc for a cifra/decifra mesajele. For varianta mai complexă cu chei publice, se implementează pasul de handshake: server încarcă cheia sa privată and trimite clienților cheia publică (or certificatul); client generează o cheie simetrică random, o criptează cu cheia publică a serverului and o trimite; server o decodifică cu cheia privată. After this schimb, se folosește respectiva cheie simetrică de sesiune for a cifra tot traffic ulterior. Se vor folosi moduri de encryption sigure (ex: AES-GCM which oferă and integritate). Odată criptarea adăugată, se retestează scenariile: clienții must să poată comunica ca before, transparent (criptarea/decriptarea being internă). Se verifică cu Wireshark că datele brute pe network nu mai has lizibile. Livrabil: code final al aplicației (server and client) documentat, plus un manual scurt de utilizare (cum se generează cheile, cum se pornește server, cum se pornesc clienții, ce dependențe has necesare). Totodată, un report final ce include capturi Wireshark (or alt output) demonstrând că un mesaj “Hello” trimis de un client apare ca text cifrat pe network and only application de pe celălalt capăt îl afișează corect în clar. Raportul va discuta and nivelul de security obținut (ex: if s-a folosit cheie comună hardcodată, se va menționa că nu e recomandat în producție, etc.).


### 📊 PEER INSTRUCTION - CONCEPTE REȚEA

Discutați cu colegii and alegeți împreună răspunsul corect:

Întrebarea 1: Un dispozitiv has address IP 192.168.1.50. Ce tip de address is aceasta?

A) Address publică, rutabilă pe Internet
B) Address privată conform RFC 1918 ✓
C) Address de loopback
D) Address broadcast

Explicație: Range-uri private: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16. Acestea necesită NAT for acces Internet.

Întrebarea 2: Într-o network cu masca /24, câte addresses IP has disponibile for dispozitive?

A) 256 addresses
B) 254 addresses ✓
C) 255 addresses
D) 252 addresses

Explicație: /24 = 256 addresses totale. Scădem: 1 address de network (ex: .0) and 1 broadcast (ex: .255) = 254 utilizabile.


### 🎤 Stage 4 (Week 14) – Prezentare final: Se prezintă arhitectura aplicației (modules în which client and server interacționează, eventual un example de mesaj criptat vs decriptat). Demonstrația live can consta în rularea unui server and a doi clients: se trimit mesaje between clients, arătând că acestea apar criptate într-un output Wireshark. Optional, se can demonstra ce se întâmplă if un client neautorizat (which nu cunoaște cheia) încearcă să se alăture – ideal, nu can comunica inteligibil. Se evidențiază thus importanța distribuției de chei. Livrabil: slide-uri and demonstrația practică, cu explicații about implementation and about cum s-ar putea extinde (ex: for authentication de utilizator, for interfață grafică etc.).

Extensii posibile for teams de 3 vs. 2/1 students
Echipele de 3 students can aborda facilități suplimentare ce adaugă complexitate: for example, implementation unei autentificări a utilizatorilor cu password (server verifică passwords and transmite cheia de encryption numai after authentication, oferind confidențialitate only utilizatorilor legitimi) or adăugarea unei interfețe grafice (using Tkinter or PyQt for a makes application mai user-friendly decât consola). O altă extindere ar fi suportul for mesaje offline or stocarea în siguranță a mesajelor (criptate) pe server. Echipa extinsă ar putea implementa nu only confidențialitate, ci and integritate and authentication end-to-end – adică each mesaj să fie semnat digital de expeditor (using chei private per client) so that destinatarii să poată verifica sursa.
Echipele mai mici (2 or 1 student) can simplifica project through alegerea unor metode mai ușoare de encryption: de pildă, can folosi direct modulul ssl din Python for a crea un wrap SSL în jurul socket-urilor, evitând implementation manuală a schimbului de chei (practic, using biblioteca for a makes un tunel TLS – deși mai puțin didactic, e mai simple din point de vedere al codului). If and asta e dificil, can opta for o cheie simetrică fixă cunoscută de ambele părți, concentrându-se pe implementation criptării/decriptării mesajelor cu acea cheie. În plus, team mică can limita funcționalitatea la chat de grup (without mesaje private or alte comenzi speciale) for a reduce volumul de code de gestionare a logicii aplicației.

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

Paar, C., & Pelzl, J. (2010). Understanding Cryptography: A Textbook for Students and Practitioners. Springer. (Capitolele about AES and RSA oferă fundamentele teoretice folosite în project)
Nagpal, D. (2018). Building Network Security Tools. Packt Publishing. (Include studii de caz practice privind crearea de applications sigure de network în Python, cu examples de chat securizat and utilizare a PyCryptodome)
Rescorla, E. (2001). SSL and TLS: Designing and Building Secure Systems. Addison-Wesley. (Deși dedicată TLS, cartea explică pașii unui handshake and componentele securității unui canal de comunicare – sursă de inspirație for protocol project)
PyCryptodome Documentation – PyCryptodome Library Documentation. (2022). Disponibil la: https://pycryptodome.readthedocs.io (Manualul oficial al bibliotecii de criptografie în Python, cu examples de utilizare a algoritmilor simetrici and asimetrici)
Stallings, W. (2017). Cryptography and Network Security: Principles and Practice (7th ed.). Pearson. (Oferă context academic about protocoalele de security and algoritmi; util for înțelegerea de ansamblu a soluției implementate)
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


### 💡 For Security and Encryption

Din TW ai folosit HTTPS and can crypto în Node.js:

```python
# Node.js crypto → Python cryptography

# Criptare simetrică (AES)
from cryptography.fernet import Fernet
key = Fernet.generate_key()
cipher = Fernet(key)
encrypted = cipher.encrypt(b"mesaj secret")

# Hash (similar cu crypto.createHash în Node)
import hashlib
hash_obj = hashlib.sha256(b"password")
hash_hex = hash_obj.hexdigest()

# În Express aveai middleware pentru autentificare
# În Python implementezi manual sau folosești biblioteci
```

---

## 📚 RELEVANT LABORATORY MATERIALS

Consultă these resurse din arhiva **netROwsl** for conceptele necesare:


### 📁 `02roWSL/` — Programare Socket

**What you'll find relevant:**
- TCP sockets, client-server concurent

**Recommended files:**
- `02roWSL/README.md` — overview and laboratory steps
- `02roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `02roWSL/docs/fisa_comenzi.md` — useful commands
- `02roWSL/src/` — Python code examples
- `02roWSL/homework/` — similar exercises


### 📁 `09roWSL/` — Nivelul Sesiune and Prezentare

**What you'll find relevant:**
- Encryption, authentication, sesiuni

**Recommended files:**
- `09roWSL/README.md` — overview and laboratory steps
- `09roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `09roWSL/docs/fisa_comenzi.md` — useful commands
- `09roWSL/src/` — Python code examples
- `09roWSL/homework/` — similar exercises


### 📁 `03roWSL/` — Broadcast and Multicast

**What you'll find relevant:**
- Grupuri de utilizatori, mesaje de grup

**Recommended files:**
- `03roWSL/README.md` — overview and laboratory steps
- `03roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `03roWSL/docs/fisa_comenzi.md` — useful commands
- `03roWSL/src/` — Python code examples
- `03roWSL/homework/` — similar exercises


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
