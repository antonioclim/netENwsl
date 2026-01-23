# Project 05: Implementarea unui protocol de rutare personalizat în Python

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
https://github.com/[username]/retele-proiect-05
```

#### Required Repository Structure

```
retele-proiect-05/
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

**Format:** `NUME_Prenume_GGGG_P05_TT.zip`

| Field | Description | Example |
|------|-----------|---------|
| NUME | Family name (UPPERCASE, no diacritics) | POPESCU |
| Prenume | First name (first letter capitalised) | Ion |
| GGGG | Group number (4 digits) | 1098 |
| P05 | Project number | P05 |
| TT | Deliverable type (S1-S4 or SXX) | E1 |

**Examples for this project:**
- `POPESCU_Ion_1098_P05_E1.zip` — Stage 1
- `POPESCU_Ion_1098_P05_E2.zip` — Stage 2
- `POPESCU_Ion_1098_P05_S07.zip` — Verification săptămâna 7

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
This project has ca obiectiv simularea and implementation unui protocol de rutare la scară mică, for a înțelege modules în which calculatoarele and routerele își distribuie informații de rutare într-o network. Studenții vor crea o application (or un set de applications) în Python which rulează pe mai multe noduri (for example, pe instanțe Mininet or pe mai multe mașini virtuale) and which comunică between ele for a makes schimb de tabele de rutare. Se can alege fie modelarea unui protocol de rutare vectorial la distanță (în stilul RIP, cu schimb de vectori de distanță periodic), fie a unui protocol de rutare de stare a legăturii (în stilul OSPF, cu schimb de metrici and calcul global de drumuri).
Un scenariu posibil: se vor emula 3-5 noduri (ca and cum ar fi routere) interconectate într-o anumită topology (ex: un cerc or o topology generală). Each nod va rula o instanță a programului de rutare dezvoltat. Nodurile vor comunica through socket-uri UDP or TCP, trimițând mesaje de actualizare de rută la intervale regulate or la detectarea unei modificări. De example, într-o abordare de tip Distance Vector, each nod își va trimite lista curentă de destinații cunoscute and costuri towards vecinii săi; aceștia vor actualiza tabelele lor using algoritmul Bellman-Ford (or varianta simplificată specifică RIP). În abordarea Link State, each nod va transmite vecinilor săi packets de stare a legăturilor (LSA) conținând costurile spre vecinii direcți; eventual, each nod va have thus cunoștința întregului graf and va calcula local rutele using un algoritm ca Dijkstra.
Proiectul implică and tratarea unor probleme clasice de rutare, precum convergența (asigurarea că toți ajung la tabele consistente), gestionarea topologiilor dinamice (if un nod/point de legătură cade, protocol ar trebui să actualizeze rutele) and prevenirea problemelor ca bucla de rutare (ex: în Distance Vector se can experimenta situații de count-to-infinity, which can fi abordate through limite or split horizon, etc., if timpul permite). Rezultatul final va fi un demo al protocolului: se va putea porni instanțele pe noduri, acestea vor realiza schimbul de mesaje de rutare and, after o perioadă, each nod își afișează tabelul de rutare stabilizat (cu destinații and next-hop/cost). Optional, se can demonstra adaptarea: if se deconectează un nod or se schimbă costul unei legături, noile rute has recalculate and propagate.

### 🎯 Learning Objectives

Aprofundarea principiilor algoritmilor de rutare dinamică (vectorii de distanță and starea legăturii) într-un mod practic, văzând cum se traduc în mesaje and actualizări.

### 🛠️ Technologies and Tools

Învățarea importanței conceptelor de convergență and stabilitate într-o network: cum mici diferențe (timpi or pierderi de packets) can afecta momentul în which all nodurile have informații corecte.
Exersarea depanării de network la nivel logic – studenții vor trebui să verifice conținutul mesajelor de rutare and evoluția tabelelor de rutare, eventual using log-uri or mesaje de debug, similar cu modules în which s-ar inspecta pachetele într-un protocol real.
Înțelegerea limitărilor protocoalelor reale (RIP, OSPF) through comparare cu implementation lor simplificată – for example, de ce RIP has metrică limitată la 15 or cum OSPF evită inundațiile excesive. This project can oferi un context practic acestor discuții teoretice.

### 📖 Key Concepts

Algoritmi de rutare – Distance Vector (Bellman-Ford) and Link State (Dijkstra), actualizarea tabelelor de rută, metrici (costuri) ale legăturilor.
Protocoale de rutare inter-routere – mecanisme de anunțare a rutelor (mesaje periodic vs. evenimential), formate de packets (ex: un mesaj DV conține perechi destinație-cost; un mesaj LS conține identificator de nod and lista de vecini cu costuri).
Topologii de network and grafuri – reprezentarea network ca graf de noduri and legături; noțiunea de cost al drumului and calculul celui mai scurt drum.
Convergență and stabilitate – propagarea schimbărilor, detectarea link-urilor căzute (ex: through time-out if nu mai primim anunțuri de la un vecin), probleme ca routing loops and soluții (split horizon, hold-down timers – can fi menționate or implementate if se alege).
Adrese IP and rutare – în implementation putem folosi IP reale ale mașinilor/VM-urilor for a simula adresele rețelelor destinație; conceptul de next hop and de mască can fi menționat (deși se can simplifica considerând each nod identificat de un ID or IP distinct without subnets multiple).
Technologies Involved
Python – limbaj for implementation, ușor for manipularea pachetelor. Se vor folosi socket-uri (probabil UDP, dat being că multe protocols de rutare reale folosesc UDP for anunțuri, ex RIP pe port 520). TCP ar putea fi folosit, but UDP reflectă mai bine natura “connectionless” a anunțurilor de rutare.
Biblioteci Python – eventual struct for a construi packets binare (if se dorește simularea la nivel de byte), deși e acceptabil să se trimită mesaje JSON or pickled (Python objects) for simplitate. Threading or asyncio can fi util for a asculta and trimite mesaje simultan.
Mediu de test – se can folosi Mininet for a crea noduri virtuale and legături cu latențe or costuri (costul can fi asimilat timpului de ping or lățimii de bandă invers proporțional or setat static). Alternativ, mai multe procese pe un singur PC, diferențiate through ports UDP, can simula nodurile de network (costurile configurate manual în code).
Instrumente de monitorizare – Wireshark for a vedea mesajele UDP de rutare (if has în format clar or se can defini un dissector custom rudimentar, deși nu e mandatory), logging intern în files for a înregistra starea tabelelor de rutare after each iterație, facilitând debug-ul.
Configurație – un file de configuration (ex: .json or text) which descrie topology (ce noduri has vecine cu costurile respective) ar fi util; application îl can citi la pornire so that network simulată e clar definită.
Connection to Weekly Course Topics
Week 5: Adresarea IP and subnets – un protocol de rutare has ca scop propagarea informației about ce addresses IP has accesibile printr-un anumit nod. Cunoștințele about addresses and prefixe din sapt. 5 has temelia pe which se construiește înțelegerea rutării.
Week 6: Protocoale de rutare – this project is practic aplicarea subiectelor discutate în săptămâna 6 (unde, conform fișei, probabil s-have acoperit algoritmi de rutare, RIP, OSPF, etc.). Proiectul vine ca o extensie practică a laboratorului Week6 („Simulare algoritmi de rutare” din arhivă), through implementation reală.
Week 3: Echipamente de network – studenții vor simula comportamentul unor routere, so se leagă de cunoștințele about rolul routerelor and interconectarea rețelelor din sapt. 3.
Week 12: Programare de network – se folosesc socket-uri and programare concurentă, abilități exersate în cursul de programare a network. În special, lucrul cu UDP (nelivrat, posibil pierdere de packets) is legat and de discuțiile about transport vs. network.
Etapele project

### 📋 Stage 1 (Week 5) – Definirea topologiei and a protocolului de rutare: Se va alege tipul de protocol (Distance Vector simple or Link State simple) and se va defini o topology de test (numărul de noduri and cum has conectate). De example, se decide: “Vom implementa un protocol de rutare vectorial la distanță în stil RIP, metrică = număr de hopuri, topology: nodurile A-B-C formează un lanț, plus legătură A-C directă etc.”. Se va redacta and un pseudo-code al algoritmului de actualizare (Bellman-Ford): cum procesează un nod informațiile primite de la vecin. Totodată, se definește formatul mesajelor de rutare: de ex., “mesaj DV = [ (destinație, cost), (destinație, cost), ... ], trimis UDP pe port X ”. Livrabil: un document de design which include diagrama topologiei (cu costuri inițiale pe each legătură), specificația protocolului (algoritm + format mesaje) and planul de test (ce situații se vor verifica – ex: calculul initial, then deconectarea unui nod etc.).


### 🔨 Stage 2 (Week 9) – Implementation initial and test pe convergență statică: Se implementează application de rutare conform design-ului. În prima versiune, se can presupune că topology rămâne fixă pe durata testului (without căderi de noduri). Each instanță pornită pe un nod citește configurația (cine îi has vecinii and costurile towards ei), pornește un listener UDP and începe să trimită periodic mesaje de rutare. Se instrumentează code so that each nod să afișeze periodic tabela sa de rutare (destinație -> cost, next hop). Se rulează toți demonii de rutare and se observă if, after un anumit timp, tabelele se stabilizează conținând drumurile corecte (cele mai scurte). Livrabil: code sursă (în repository) and un log/rezultat al rulării pe un caz de test, which să arate evoluția tabelelor de la start (când each cunoaște only pe sine and vecinii) până la convergență (când toți cunosc rutele optime). De example, se can prezenta capturi în which la început nodul A știe only B cu cost 1, iar after convergență știe and de C cu cost 2 through B, etc.


### 🔮 VERIFICARE ÎNȚELEGERE - CONCEPTE REȚEA

Before de configuration, verificați că înțelegeți:

1. Ce tip de address is 192.168.1.50?
 → Address privată (RFC 1918), nu can fi rutată direct pe Internet

2. Câte addresses IP utilizabile has într-o network /24?
 → 254 addresses (256 total minus 1 for network minus 1 for broadcast)

3. Ce rol has NAT în network voastră?
 → Traduce adresele IP private în address publică for acces Internet


### ✅ Stage 3 (Week 13) – Implementation evenimente dinamice and optimizări: În this stage se introduce capacitatea protocolului de a reacționa la schimbări: for example, se deconectează un nod (nu mai trimite mesaje; vecinii ar trebui after un timeout să îl considere inactiv and să-and actualizeze tabelele). Or se modifică costul unei legături (if se can simula, de ex. in Mininet through schimbarea delay-ului) and se observă adaptarea. Se can adăuga mecanisme suplimentare for solidețe, precum un timer de invalidare (if într-un interval nu se primește nicio actualizare de la un vecin, rutele through that vecin has marcate inaccesibile – similar cu "timeout" din RIP). If team dorește, can implementa and prevenirea buclelor through “split horizon” (nu anunță unei rute înapoi pe interfața de unde have venit). Livrabil: code final (which include tratarea evenimentelor de cădere) and un set de experimente documentate: ex. un scenariu în which nodul X cade and cum tabelele se modifică (se așteaptă câteva intervale, se scot rutele ce duceau la X). Alt scenariu: creșterea costului pe o legătură cauzează recalcularea drumului alternativ (if există) cu cost mai mic. Rezultatele can fi prezentate sub formă de loguri before/after eveniment, evidențiind reacția corectă a algoritmului.


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


### 🎤 Stage 4 (Week 14) – Prezentare final: Echipa va prezenta conceptul protocolului implementat, comparându-l cu echivalentul real (if DV, then cu RIP; if LS, cu OSPF). Vor arăta vizual topology de test and, posibil, vor ilustra pe slide-uri cum se propagă informația de rutare (ex: “Pasul 1: A știe only 0 pt A and inf pt restul; Pasul 2: A primește de la B distanțele ...” etc.). Demo-ul practic can consta în rularea aplicației cu 3 noduri în consolă, arătând cum pornesc cu rute locale and ajung să cunoască întreaga network. Optional, se can demonstra un caz de failover: se oprește unul din procese (simulând căderea unui nod) and se vede cum celelalte actualizează că destinațiile through that nod nu mai has accesibile. Livrabil: prezentarea (cu diagrame and eventual pseudocod) and demonstrația live or pre-înregistrată a funcționării protocolului.

Extensii posibile for teams de 3 vs. 2/1 students
Teams de 3 students: can încerca implementation ambelor tipuri de algoritmi (DV and LS) and compararea lor. De example, can realiza modulul main comun iar algoritmul de actualizare să fie plug-in: rulat fie ca DV, fie ca LS and să demonstreze ambele metode în topologii similare. Echipa lărgită can extinde project spre vizualizarea network – for example, generarea unui grafic (using Graphviz) al topologiei cunoscute de each nod, for a vedea diferențe. O altă extindere ambițioasă: integrarea project cu configuration reală a rutării pe un router software (ex: using Quagga through API – but asta ar fi destul de complex, so only ca experiment).
Teams 1-2 students: can simplifica project reducând numărul de noduri and situațiile gestionate. De example, for 2 students, o topology triunghiulară statică (3 noduri complete interconectate) is suficientă for a demonstra conceptul, without să mai trateze căderi de nod (each cunoaște tot oricum într-un triunghi complete). Totodată, can evita implementation optimizărilor de buclă and can presupune metrici fixe (without recalcularea costurilor la runtime). Thus, ei se concentrează pe implementation de bază a algoritmului and pe convergența initial, ceea ce acoperă oricum o bună parte din obiectivele de învățare.

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

Tanenbaum, A. S., Feamster, N., & Wetherall, D. (2021). Computer Networks (6th ed.). Pearson. (Capitolele about algoritmii de rutare and protocoalele RIP/OSPF – oferă fundalul teoretic necesar)
Kurose, J. F., & Ross, K. W. (2021). Computer Networking: A Top-Down Approach (8th ed.). Pearson. (Vezi capitolul privind rutarea: descrie conceptele de vector distanță and stare legătură, utile for orientare în implementation)
Hedrick, C. (1988). RFC 1058: Routing Information Protocol. IETF. (Standardul for RIP v1 – conține detalii about formatul mesajelor and algoritm, which can fi parcurse for inspirație, deși project implementat is o versiune simplificată)
Moy, J. (1998). RFC 2328: OSPF Version 2. IETF. (Descrierea oficială a OSPF – utilă for înțelegerea conceptului de link-state, flooding de packets LSA, even if nu se implementează în detaliu, oferă perspectivă asupra cerințelor unui protocol real)
Grime, S. (2019). Networking Algorithms: An Applied Approach. TechPress. (Include studii de caz de implementation simple a algoritmilor de rutare în code – can servi ca example suplimentar de structurare a aplicației de rutare)
(Grade: Proiectele 6–20 vor continua în același format detaliat, acoperind restul de subiecte avansate and moderate, conform cerințelor.)
... (documentul continuă cu proiectele 6–15 – avansate and 16–20 – cu dificultate ușor redusă, structurate similar ca mai sus) ...
Tabel de planificare a etapelor pe weeks
[1] Static Equivalence Checking for OpenFlow Networks - MDPI
https://www.mdpi.com/2079-9292/10/18/2207
[2] Mininet - Washington
https://courses.cs.washington.edu/courses/cse461/22au/assignments/mininet.html
[3] Containernet | Use Docker containers as hosts in Mininet emulations.
https://containernet.github.io/
---

## 🔮 Verification înțelegere — Networks

Before de configuration:

1. **Ce tip de address is 192.168.1.50?**
 - Address privată (RFC 1918)

2. **Câte addresses IP utilizabile has într-o network /24?**
 - 254 (256 - 1 network - 1 broadcast)

3. **Ce makes NAT?**
 - Traduce addresses private în publice for acces Internet

---

## 📊 Peer Instruction — Networks

**Întrebare:** Un dispozitiv has IP 192.168.1.50. Ce tip de address is?

- A) Address publică
- B) Address privată (RFC 1918) ✓
- C) Address loopback
- D) Address broadcast


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

---

## 📚 RELEVANT LABORATORY MATERIALS

Consultă these resurse din arhiva **netROwsl** for conceptele necesare:


### 📁 `05roWSL/` — Adresare IPv4/IPv6, Subrețele and VLSM

**What you'll find relevant:**
- Calculul rutelor, tabele de rutare

**Recommended files:**
- `05roWSL/README.md` — overview and laboratory steps
- `05roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `05roWSL/docs/fisa_comenzi.md` — useful commands
- `05roWSL/src/` — Python code examples
- `05roWSL/homework/` — similar exercises


### 📁 `04roWSL/` — Protocoale Personalizate

**What you'll find relevant:**
- Definirea and implementation protocolului

**Recommended files:**
- `04roWSL/README.md` — overview and laboratory steps
- `04roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `04roWSL/docs/fisa_comenzi.md` — useful commands
- `04roWSL/src/` — Python code examples
- `04roWSL/homework/` — similar exercises


### 📁 `06roWSL/` — NAT/PAT and SDN

**What you'll find relevant:**
- Routing decisions, forwarding

**Recommended files:**
- `06roWSL/README.md` — overview and laboratory steps
- `06roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `06roWSL/docs/fisa_comenzi.md` — useful commands
- `06roWSL/src/` — Python code examples
- `06roWSL/homework/` — similar exercises


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
