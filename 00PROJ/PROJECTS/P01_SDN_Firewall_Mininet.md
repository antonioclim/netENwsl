# Project 01: Firewall SDN în Mininet

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
https://github.com/[username]/retele-proiect-01
```

#### Required Repository Structure

```
retele-proiect-01/
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

**Format:** `NUME_Prenume_GGGG_P01_TT.zip`

| Field | Description | Example |
|------|-----------|---------|
| NUME | Family name (UPPERCASE, no diacritics) | POPESCU |
| Prenume | First name (first letter capitalised) | Ion |
| GGGG | Group number (4 digits) | 1098 |
| P01 | Project number | P01 |
| TT | Deliverable type (S1-S4 or SXX) | E1 |

**Examples for this project:**
- `POPESCU_Ion_1098_P01_E1.zip` — Stage 1
- `POPESCU_Ion_1098_P01_E2.zip` — Stage 2
- `POPESCU_Ion_1098_P01_S07.zip` — Verification săptămâna 7

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
This project urmărește realizarea unui firewall de network using paradigma Software-Defined Networking (SDN). În locul unui firewall tradițional bazat pe dispozitive hardware dedicate, se va implementa o application de firewall la nivel de controler SDN, which să filtreze traffic between nodurile unei networks virtuale. Platforma de emulare Mininet va fi utilizată for a crea o topology virtuală de network (computers and switch-uri OpenFlow), controlată de un controler SDN (precum POX or Ryu) programat în Python. Firewall-ul SDN va inspecta pachetele (for example, pe baza adreselor IP, porturilor TCP/UDP or tipului de protocol) and va aplica reguli de filtrare (permitere/blocare) în mod dinamic, through instalarea de fluxuri OpenFlow în switch-urile network.
Proiectul presupune parcurgerea etapelor de design al politicilor de security (de ex. ce tipuri de traffic has permise or blocate), configuration topologiei de network în Mininet and dezvoltarea logicii firewall-ului în controlerul SDN. Se va testa funcționalitatea firewall-ului trimițând traffic de test between host-urile din Mininet (de ex. ping, HTTP, etc.) and verificând că pachetele interzise has filtrate corect. This demers oferă o perspectivă practică asupra modului în which rețelele can fi programate and securizate dinamic using SDN, separând planul de control de dispozitivele de date[1][2]. Rezultatul final va fi o application firewall configurabilă, rulând într-o network virtuală, împreună cu un report ce descrie arhitectura soluției and teste de verification.

### 🎯 Learning Objectives


### 🛠️ Technologies and Tools

Însușirea conceptelor de firewall and liste de control al accesului (ACL) într-un mediu de network programabilă.
Dezvoltarea abilităților practice de a utiliza Mininet for emularea rețelelor and de a programa un controler SDN simple în Python.
Înțelegerea modului de monitorizare and filtrare a pachetelor la nivel de network, precum and assessment impactului regulilor de security asupra traficului.
Dezvoltarea abilităților critice privind security rețelelor and modules în which arhitectura SDN can simplifica implementation politicilor de security.

### 📖 Key Concepts

Software-Defined Networking (SDN) – separarea planului de control de cel de date, controler centralizat, protocol OpenFlow[2].
Firewall de network – filtrarea pachetelor pe baza regulilor (addresses IP sursă/destinație, ports, protocol).
Protocoale de nivel network and transport – IPv4/IPv6, TCP/UDP (utilizate for a identifica fluxurile de traffic ce vor fi filtrate).
Comutare and rutare OpenFlow – fluxuri în switch-urile virtuale which implementează regulile de firewall through acțiuni de drop or forward.
Securitatea rețelelor – noțiuni de acces permis/interzis, protecția segmentelor de network, politici de security distribuite.
Technologies Involved
Mininet – emulare de topologii de network virtuale (switch-uri OpenFlow and host-uri Linux).
Python – limbajul folosit for a programa logica firewall în controlerul SDN (ex. using POX, Ryu or alt framework SDN).
Protocolul OpenFlow – for definirea regulilor în switch (through intermediul controlerului).
Wireshark (optional) – for captură and inspecție de packets, în vederea verificării comportamentului firewall-ului.
Sisteme Linux – configuration mediului de dezvoltare (Mininet rulează pe Linux) and utilizarea utilitarelor de network (ping, iperf) for testing.
Connection to Weekly Course Topics
Week 9: Securitatea rețelelor – project aplică concepte de firewall and control al accesului (vezi materialul „Firewall and liste de acces” din arhiva WEEK9).
Week 10: Networks definite through software (SDN) – se folosiază arhitectura SDN and OpenFlow conform laboratorului din Week10 („Mininet – OpenFlow Basic”).
Week 12: Programare de network în Python – dezvoltarea controlerului OpenFlow în Python valorifică cunoștințele de socket programming and biblioteci SDN prezentate în cursul din Week12.
Etapele project

### 📋 Stage 1 (Week 5) – Analiză and design: Documentarea conceptelor SDN and OpenFlow; definirea politicii de security (ce tipuri de traffic vor fi blocate/permisive). Se va realiza o schiță a topologiei Mininet (ex: 2 switch-uri and 4 host-uri, cu firewall aplicat between segmente) and se va alege platforma de controler (ex. POX). Livrabil: report scurt cu specificațiile firewall-ului (listă de reguli intenționate), diagrama topologiei de network propuse and un plan de implementation. Se va iniția and un repository (ex. pe GitHub) cu structura de files a project (for example, un file README and un file-schelet for controlerul SDN).


### 🔨 Stage 2 (Week 9) – Prototip functional: Implementarea parțială a firewall-ului SDN. Se va construi topology în Mininet and se va dezvolta code Python al controlerului for a impune at least o regulă de filtrare (ex: blocarea ping-urilor or a traficului HTTP). Se testează prototipul through trimiterea traficului de test and se colectează rezultate (capturi Wireshark or log-uri din controler). Livrabil: code sursă al controlerului (actualizat în repository, bine structurat and comentat), un file de configuration/topology for Mininet (if e cazul) and un scurt report de testing which demonstrează o regulă de firewall în acțiune.


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


### ✅ Stage 3 (Week 13) – Versiunea final and teste extensive: Extinderea implementării for a acoperi întregul set de reguli de firewall planificate (de ex. filtrare pe multiple ports/protocols, eventual logging al pachetelor blocate). Se realizează teste extensive în diferite scenarii (traffic permis vs. blocat, simularea unui atac scanare ports, etc.) and se optimizează performanța or claritatea codului. Livrabil: project final – code complete (în repository, însoțit de instrucțiuni de rulare and eventual scripturi for reproducerea mediului), files de configuration, plus un report final which include arhitectura soluției, capturi de ecran/log-uri din teste and discuții asupra funcționalității and limitărilor.


### 📊 PEER INSTRUCTION - SDN ȘI OPENFLOW

Discutați cu colegii and alegeți împreună răspunsul corect:

Întrebarea 1: After ce controller-ul instalează o regulă OpenFlow cu actions=drop, ce se întâmplă cu pachetele which make match?

A) Are trimise înapoi la sursă cu ICMP Destination Unreachable
B) Are șterse silențios without nicio notificare ✓
C) Are redirecționate towards controller for logging
D) Are puse în coadă până expiră timeout-ul flow-ului

Explicație: Acțiunea drop elimină packet complete. For ICMP unreachable ar fi nevoie de o regulă explicită which să trimită this mesaj.

Întrebarea 2: Ce tip de mesaj OpenFlow trimite switch-ul towards controller când primește un packet for which nu există regulă?

A) FlowMod (modificare flux)
B) PacketIn (packet primit) ✓
C) PacketOut (trimite packet)
D) PortStatus (stare port)

Explicație: PacketIn = switch întreabă controller-ul ce să facă. FlowMod = controller instalează regulă în switch.


### 📊 CERINȚĂ SUPLIMENTARĂ: ANALIZĂ COMPARATIVĂ

În raportul final, includeți o secțiune de 1-2 pagini cu:
1. Comparație cu at least 2 alternative tehnologice
2. Metrici de performanță măsurate (latență, throughput)
3. Limitări and posibile îmbunătățiri ale soluției


### 🎤 Stage 4 (Week 14) – Prezentare final: Echipa va susține o prezentare de ~15 minute în which descrie pe scurt conceptul de firewall SDN, modules de implementation and va demonstra live funcționarea pe un caz de test (de ex. două terminale – unul which încearcă să comunice and is blocat conform regulilor). Livrabil: diapozitivele prezentării and eventual un scurt videoclip demonstrativ (optional, if se dorește evidențierea scenariilor de test).

Extensii posibile for teams de 3 vs. 2/1 students
For o team de 3 students, se can extinde project implementând funcționalități avansate de firewall, cum ar fi filtrare dinamică (ex: încărcarea regulilor dintr-un file de configuration în timp real) or un firewall stateful simplificat (menținerea unei tabele de sesiuni active, permițând automat traffic de răspuns la connections inițiate). Totodată, s-ar putea integra o mică interfață (ex. linie de comandă or GUI elementar) for a adăuga/șterge reguli de filtrare la rulare.
For o team mai restrânsă (2 or 1 student), focusul can rămâne pe un firewall stateless de bază cu un set fix de reguli implementate direct în code. Complexitatea can fi redusă la filtrarea after criteria esențiale (ex: blocarea totului apart from traffic pe port X between două host-uri specifice). Even and în formă mai simple, project va atinge obiectivele educaționale, but cu un volum de lucru mai adecvat resurselor echipei.

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

Kreutz, D., Ramos, F. M. V., Veríssimo, P. E., Rothenberg, C. E., Azodolmolky, S., & Uhlig, S. (2015). Software-Defined Networking: A complete Survey. IEEE Communications Surveys & Tutorials, 17(1), 27-51. https://doi.org/10.1109/COMST.2014.2326417
Lantz, B., Heller, B., & McKeown, N. (2010). A network in a laptop: rapid prototyping for software-defined networks. Proceedings of the 9th ACM SIGCOMM Workshop on Hot Topics in Networks (HotNets-IX), 19. https://doi.org/10.1145/1868447.1868466
Hu, H., Han, W., Ahn, G.-J., & Zhao, Z. (2014). FlowGuard: Building solid firewalls for software-defined networks. In Proceedings of the ACM SIGCOMM Workshop on Hot Topics in SDN (HotSDN ’14) (pp. 97-102). ACM. https://doi.org/10.1145/2620728.2620749
Göransson, P., Black, C., & Culver, T. (2014). Software Defined Networks: A complete Approach. Morgan Kaufmann Publishers.
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


### 📁 `06roWSL/` — NAT/PAT, Protocoale de Suport and Networks Definite through Software

**What you'll find relevant:**
- Conceptele SDN and OpenFlow, controlere, flow tables

**Recommended files:**
- `06roWSL/README.md` — overview and laboratory steps
- `06roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `06roWSL/docs/fisa_comenzi.md` — useful commands
- `06roWSL/src/` — Python code examples
- `06roWSL/homework/` — similar exercises


### 📁 `07roWSL/` — Interceptarea and Filtrarea Pachetelor

**What you'll find relevant:**
- Wireshark, filtre de captură, analiza traficului

**Recommended files:**
- `07roWSL/README.md` — overview and laboratory steps
- `07roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `07roWSL/docs/fisa_comenzi.md` — useful commands
- `07roWSL/src/` — Python code examples
- `07roWSL/homework/` — similar exercises


### 📁 `02roWSL/` — Modele Arhitecturale and Programare Socket

**What you'll find relevant:**
- Fundamentele socket-urilor for comunicarea controller-switch

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
