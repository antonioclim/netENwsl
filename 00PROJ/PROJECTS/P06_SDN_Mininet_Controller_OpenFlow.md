# Project 06: Network definită through software (SDN) cu Mininet and controler OpenFlow

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
https://github.com/[username]/retele-proiect-06
```

#### Required Repository Structure

```
retele-proiect-06/
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

**Format:** `NUME_Prenume_GGGG_P06_TT.zip`

| Field | Description | Example |
|------|-----------|---------|
| NUME | Family name (UPPERCASE, no diacritics) | POPESCU |
| Prenume | First name (first letter capitalised) | Ion |
| GGGG | Group number (4 digits) | 1098 |
| P06 | Project number | P06 |
| TT | Deliverable type (S1-S4 or SXX) | E1 |

**Examples for this project:**
- `POPESCU_Ion_1098_P06_E1.zip` — Stage 1
- `POPESCU_Ion_1098_P06_E2.zip` — Stage 2
- `POPESCU_Ion_1098_P06_S07.zip` — Verification săptămâna 7

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

Descriere: This project abordează conceptul de Software-Defined Networking (SDN) through dezvoltarea unei networks simulate în Mininet controlată de un controller OpenFlow implementat de students. În esență, studenții vor crea o topology de network virtuală (ex. mai multe noduri and switch-uri virtuale) using Mininet and vor programa un controller SDN în Python which gestionează dinamic fluxurile de packets în network. Proiectul pune accent atât pe aspectele tehnice – cum ar fi configuration and administrarea unei networks SDN, scrierea de reguli OpenFlow for routare, comutare or filtrare – cât and pe cele educaționale, oferind o înțelegere aprofundată a separării planului de control de planul de date. Studenții vor experimenta modules în which un controller centralizat can dicta comportamentul întregii networks (for example, cum has direcționate pachetele between host-uri) and vor analiza avantajele SDN față de rețelele tradiționale (flexibilitate, programabilitate, administrare simplificată). Proiectul include teste comparative – cum se comportă network în diferite scenarii de traffic or la căderea unui nod – evidențiind modules în which SDN can reacționa rapid through reproiectarea rutelor. Totodată, se pune accent pe deprinderea utilizării unor unelte de analiză (ex. Wireshark) for a monitoriza traffic în network Mininet and pe dezvoltarea abilităților de depanare a unei applications de network complexe. Per ansamblu, project oferă o incursiune practică în arhitectura modernă a rețelelor programabile, consolidând atât cunoștințele teoretice about protocoalele de control al network, cât and competențele practice de configuration and scripting în medii de simulare de network.

### 🎯 Learning Objectives

- Să evalueze avantajele and dezavantajele soluției implementate comparativ cu alternative.
• Să compare performanța project cu soluții similare or benchmark-uri.

### 📖 Key Concepts

Technologies Involved: Python (for implementation logicii controller-ului SDN – ex. using POX or Ryu), Mininet (emulator de network for crearea topologiei virtuale), protocols OpenFlow (versiunea 1.3+ for comunicarea controller-switch), Wireshark/tcpdump (analiza traficului and debug), eventual biblioteci specifice SDN (ex. OpenFlow Python bindings). Totodată, se can folosi containere Docker for a emula host-uri din topology Mininet (optional, for teste extinse) and Git for versionarea codului sursă.
Legătura cu temele and kiturile săptămânilor 1–13: Proiectul valorifică major conținutul săptămânilor 5 and 6 din curs. În săptămâna 5 studenții have învățat about adresare IP, rutare and have been introduși în simulatoare de network – cunoștințe esențiale for a construi topology virtuală initial în Mininet (adresarea corectă a host-urilor, setarea legăturilor and înțelegerea rutelor). Week 6 a adus introducerea conceptului de Software-Defined Networking and a componentelor arhitecturale SDN, precum and familiarizarea cu Mininet and elementele unui switch virtual OpenFlow – acestea reprezintă baza teoretică and practică a project. Proiectul atinge aspecte din săptămâna 7 (interceptarea and filtrarea pachetelor) through faptul că un controller SDN can implementa funcționalități de firewall la nivel de network through reguli OpenFlow: studenții can aplica în controller concepte de filtrare învățate then. În săptămâna 8 s-have discutat services Internet and proxy-uri, iar studenții can folosi un mic server HTTP de test în network Mininet for a valida rutarea end-to-end through network definită software. Week 13 (Securitatea în networks) is and ea relevantă – ca extensie, studenții can implementa în controller mecanisme de detectare a traficului suspect (de ex. detectarea unui port scan or limitarea numărului de connections concomitente), aplicând practic noțiuni de security. Așadar, project consolidează cunoștințele acumulate pe parcursul disciplinei (adresare, rutare, SDN, filtrare, security), oferind totodată un cadru integrator în which acestea has puse în practică într-un mod progresiv.
Structură în 4 stages:

### 🔮 VERIFICARE ÎNȚELEGERE

Before de a rula comenzile, răspundeți:

1. Câte containere vor fi create conform docker-compose.yml?
 → Numărați serviciile definite în file.

2. Ce se întâmplă if port dorit is already ocupat?
 → Eroare: "port is already allocated". Verificați cu: ss -tlnp | grep :PORT

3. Cum comunică containerele between ele în aceeași network Docker?
 → Through numele serviciului (DNS intern Docker), nu through localhost.


📊 PEER INSTRUCTION

Discutați cu colegii and alegeți răspunsul corect:

Întrebarea: Containerele web and db has în aceeași network Docker. Cum se conectează web la db?

A) localhost:5432 
B) db:5432 ✓
C) 172.17.0.1:5432
D) host.docker.internal:5432

Explicație: Docker DNS rezolvă automat numele serviciilor din Compose.

Extensii for teams de 3 vs. teams de 2/1: Proiectul is dimensionat so that o team de 2 students or even un singur student să poată implementa requirements de bază (topology simple, controller which realizează forwardare fundamentală pe bază de addresses MAC/IP, eventual o function suplimentară). However, for echipele de 3 se așteaptă o complexitate sporită and componente adiționale. De example, o team de 3 can configura o topology SDN mai amplă (cu 3-4 switch-uri interconectate ierarhic, simulând o network de campus) and can implementa un set mai bogat de politici în controller: rutare pe multiple căi cu echilibrarea traficului between ele, mecanisme de security (firewalling, filtrare pe criteria variate – address IP, port TCP/UDP, tip de traffic), precum and un modules de monitorizare a traficului în timp real (for example, afișarea într-o consolă a numărului de packets procesate de each switch). Totodată, echipele mai mari ar putea integra and o interfață minimală (CLI or web simple) for controller, which să permită vizualizarea and modificarea unor reguli de rutare dinamic. În contrast, o team mai restrânsă (2 or 1 student) can limita scenariul la un singur switch central and câțiva host-uri and la funcționalitățile esențiale (ex. forwardare tip learning switch and un singur example de filtrare). Important is ca toți studenții, indiferent de mărimea echipei, să demonstreze înțelegerea principiilor SDN and să livreze o network functional; complexitatea and numărul de extensii vor diferenția however proiectele excepționale realizate de teams mai numeroase.

### ❓ ÎNTREBĂRI FRECVENTE - SDN/MININET

Q: Mininet won't start and afișează "Error creating interface"
A: Rulați cu sudo and curățați sesiunile anterioare:
 sudo mn -c
 sudo mn --topo single,3 --controller remote

Q: Controller-ul nu primește mesaje PacketIn
A: Verificați că switch-ul e conectat la controller:
 - dpctl show
 - Asigurați-vă că IP-ul controller-ului e corect în topology

Q: Cum testez că firewall-ul funcționează corect?
A: Folosiți comenzi de test în Mininet CLI:
 - h1 ping h2 (for traffic which ar trebui blocat)
 - h1 curl h2:80 (for traffic which ar trebui permis)
 - Verificați log-urile controller-ului for decizii


### 📚 Bibliografie

Kreutz, D., Ramos, F. M. V., Veríssimo, P. E., Rothenberg, C. E., Azodolmolky, S., & Uhlig, S. (2015). Software-Defined Networking: A complete Survey. Proceedings of the IEEE, 103(1), 14-76. https://doi.org/10.1109/JPROC.2014.2371999
Lantz, B., Heller, B., & McKeown, N. (2010). A network in a laptop: rapid prototyping for software-defined networks. În Proceedings of the 9th ACM SIGCOMM Workshop on Hot Topics in Networks (HotNets IX). ACM. https://doi.org/10.1145/1868447.1868466
McKeown, N., Anderson, T., Balakrishnan, H., Parulkar, G., Peterson, L., Rexford, J., … & Turner, J. (2008). OpenFlow: enabling innovation in campus networks. ACM SIGCOMM Computer Communication Review, 38(2), 69-74. https://doi.org/10.1145/1355734.1355746
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

## ❓ Frequently Asked Questions — SDN/Mininet

**Q: Mininet won't start - eroare "cannot create interface"** 
A: Run with sudo and clean previous sessions:
```bash
sudo mn -c
sudo mn --topo single,3 --controller remote
```

**Q: Controller-ul nu primește PacketIn** 
A: Check the connection switch-controller cu `dpctl show`

**Q: Cum testez că firewall-ul funcționează?** 
A: Folosește `h1 ping h2` for traffic blocat and `h1 curl h2:80` for traffic permis


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

---

## 📚 RELEVANT LABORATORY MATERIALS

Consultă these resurse din arhiva **netROwsl** for conceptele necesare:


### 📁 `06roWSL/` — NAT/PAT and SDN

**What you'll find relevant:**
- OpenFlow, POX/Ryu controller, flow rules

**Recommended files:**
- `06roWSL/README.md` — overview and laboratory steps
- `06roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `06roWSL/docs/fisa_comenzi.md` — useful commands
- `06roWSL/src/` — Python code examples
- `06roWSL/homework/` — similar exercises


### 📁 `07roWSL/` — Interceptarea Pachetelor

**What you'll find relevant:**
- Analiza traficului for decizii de rutare

**Recommended files:**
- `07roWSL/README.md` — overview and laboratory steps
- `07roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `07roWSL/docs/fisa_comenzi.md` — useful commands
- `07roWSL/src/` — Python code examples
- `07roWSL/homework/` — similar exercises


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
