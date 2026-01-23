# Project 07: Sistem de monitorizare a traficului and firewall software (IDS simple)

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
https://github.com/[username]/retele-proiect-07
```

#### Required Repository Structure

```
retele-proiect-07/
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

**Format:** `NUME_Prenume_GGGG_P07_TT.zip`

| Field | Description | Example |
|------|-----------|---------|
| NUME | Family name (UPPERCASE, no diacritics) | POPESCU |
| Prenume | First name (first letter capitalised) | Ion |
| GGGG | Group number (4 digits) | 1098 |
| P07 | Project number | P07 |
| TT | Deliverable type (S1-S4 or SXX) | E1 |

**Examples for this project:**
- `POPESCU_Ion_1098_P07_E1.zip` — Stage 1
- `POPESCU_Ion_1098_P07_E2.zip` — Stage 2
- `POPESCU_Ion_1098_P07_S07.zip` — Verification săptămâna 7

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

Descriere: This project își propune realizarea unui sistem personalizat de monitorizare and filtrare a traficului de network, combinând funcționalitățile unui sniffer (capturator de packets) cu cele ale unui firewall/IDS (Intrusion Detection System) simple. Studenții vor dezvolta o application (de regulă în Python) capabilă să intercepteze pachetele which tranzitează o interfață de network, să analizeze header-ele protocoalelor (Ethernet, IP, TCP/UDP etc.) and să aplice un set de reguli de filtrare or de detectare a activităților suspecte. Proiectul has două componente majore: (a) Monitorizarea pasivă a traficului, în which application loghează pachetele capturate (or at least statisticile relevante about ele) for a oferi vizibilitate asupra comunicațiilor din network; and (b) Filtrarea/alertarea activă, în which anumite packets ce corespund unor criteria prestabilite has fie blocate, fie declanșează alerte de security. Un example concret ar fi implementation unui modules de detectare a scanărilor de ports: application can identifica când un anumit host trimite packets SYN towards un număr mare de ports într-un interval scurt, interpretând this comportament ca port scan and generând o alertă or blocând temporar pachetele de la hostul respectiv. Totodată, se can defini filtre simple, precum blocarea tuturor pachetelor towards un anumit port (simulând un firewall which blochează for example port 23/Telnet) or capturarea only a traficului de un anumit tip (ex: only packets HTTP pe port 80) for inspecție detaliată. Pe lângă latura practică de programare a unui thus de instrument, project has and o puternică componentă educațională: studenții vor aprofunda cunoașterea formatului pachetelor de network, a modului în which funcționează protocoalele la nivel de bit/byte, precum and a metodelor through which atacurile can fi detectate through tipare de traffic. Ei vor învăța about limitările unui IDS bazat pe semnături simple versus importanța analizelor mai complexe (but which depășesc scopul acestui project introductiv) and vor conștientiza provocările în timp real ale procesării traficului (performanță, acuratețe, rate de alarme false). Proiectul permite testing soluției dezvoltate using instrumente cunoscute: for example, cu nmap se can simula un port scan asupra unei mașini din network for a verifica if sistemul implementat detectează and semnalează corespunzător evenimentul. Thus, studenții vor obține atât unelte practice (un mini-IDS pe which îl can extinde ulterior), cât and înțelegerea de bază a conceptelor de security activă în networks.

### 🎯 Learning Objectives


### 📖 Key Concepts

Technologies Involved: Python cu biblioteci de network de nivel jos – în special Scapy (o bibliotecă Python puternică for manipularea pachetelor, which permite atât captură cât and creare de packets) or socket (modulul standard Python, using socket.AF_PACKET în Linux for captură brută). Alternativ, se can folosi libpcap în C/C++ or PyShark (un wrapper for TShark/Wireshark). For testing se vor utiliza nmap (scanner de ports) and eventual generatoare de traffic (scripturi Python, hping3 etc.). Linux va fi mediul preferat (dat being accesul facil la raw sockets and la utilitare ca iptables for comparație). Totodată, Wireshark can fi utilizat for a valida capturile efectuate de application implementată. Optional, Docker can fi folosit for a lansa containere which să joace rolul de surse de traffic malițios or victime, facilitând scenarii de test controlate.
Legătura cu temele and kiturile săptămânilor 1–13: Proiectul has o legătură directă cu weeks din curs which tratează analiza and security traficului. În mod specific, săptămâna 7 (“Interceptarea pachetelor TCP & UDP; implementation unui filtru de packets; scanarea porturilor”) constituie fundamentul teoretic al acestui project. În acea week, studenții have văzut cum can fi capturate pachetele cu unelte ca Wireshark or tshark and have discutat about scanările de ports and filtrarea traficului – cunoștințe puse now în practică, because project îi pune să construiască propriul “Wireshark light” and “Snort light”. Totodată, noțiunile din săptămâna 13 (Securitatea rețelelor de computers) has aprofundate: concepte precum IDS, detectarea intruziunilor and tipuri de atacuri comune has aplicate în componenta de alertare a project. Even and materialul din primele weeks is pertinent: de pildă, înțelegerea formatului pachetelor Ethernet and IP (prezentată în introducerea cursului, weeks 1-2) is esențială for a putea scrie un analizator de packets corect. Săptămânile about programarea pe socket-uri (3 and 4) has and ele relevante – în those laboratoare studenții have dobândit abilități de a folosi API-ul de socket-uri, abilități which now has extinse towards programarea de raw sockets for captură. În rezumat, project capitalizează pe întreg parcursul de învățare al disciplinei: începe cu elemente de network de nivel jos (structura pachetelor, socket-uri) and culminează cu aspecte de security (firewall, IDS), oferind un context integrator ce reflectă obiectivele disciplinei de a pregăti studenții în a asigura funcționarea and protecția rețelelor.
Structură în 4 stages:
Extensii for teams de 3 vs. teams de 2/1: O team mai mare (3 members) is așteptată să abordeze project într-un mod mai cuprinzător, implementând reguli and functions suplimentare față de minimul necesar. De example, echipele de 3 ar putea implementa o interfață grafică simple for IDS (un tablou de bord web or cu biblioteci Python precum Tkinter) unde să afișeze în timp real alertele and statisticile de traffic – this lucru ar adăuga o dimensiune practică deosebită, permițând administratorului să vizualizeze ușor starea network. Totodată, ar putea suporta un file de configuration extern for reguli, so that noile filtre (ex. “blocare port X”) să poată fi adăugate without a modifica code sursă, simulând modules de lucru al unui firewall real. În plus, ar fi de dorit ca echipele mari să testeze sistemul într-un mediu mai complex, can într-o network reală de laborator or using containere multiple ce generează traffic simultan, for a demonstra scalabilitatea (ex. using Docker Compose for a lansa 5 containere client which trimit traffic spre 2 servers and un container dedicat IDS-ului). For echipele mai mici (2 or 1 member), requirements minime – captură, o mână de filtre simple and detectarea unui tip de atac – has suficiente, but complexitatea can fi ajustată: for example, un student singur s-ar putea concentra only pe detectarea port scan-urilor and pe blocarea unui singur port per configuration, without interfață or alte extrase. Important is ca each team să acopere partea esențială (captură + filtrare + alertare) and să demonstreze că soluția funcționează. Extensiile menționate (interfață, configurabilitate sporită, suport extins for multiple tipuri de atacuri – ex. detectarea unui atac de tip DoS through analiză de traffic agregat) vor diferenția proiectele excelente, realizate de teams cu resurse mai numeroase, de proiectele corecte realizate de teams mai mici.

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

Joseph, G., Osamor, J., & Olajide, F. (2024). A Systematic Review of Network Packet Sniffing Tools for Enhancing Cybersecurity in Business Applications. International Journal of Intelligent Computing Research, 15(1), 1292-1307. https://doi.org/10.20533/ijicr.2042.4655.2024.0157
Abu Bakar, R., & Kijsirikul, B. (2023). Enhancing Network Visibility and Security with Advanced Port Scanning Techniques. Sensors, 23(17), 7541. https://doi.org/10.3390/s23177541
Grossi, M., Alfonsi, F., Prandini, M., & Gabrielli, A. (2023). A Highly Configurable Packet Sniffer Based on Field-Programmable Gate Arrays for Network Security Applications. Electronics, 12(21), 4412. https://doi.org/10.3390/electronics12214412
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


### 📁 `07roWSL/` — Interceptarea and Filtrarea Pachetelor

**What you'll find relevant:**
- iptables, reguli de filtrare

**Recommended files:**
- `07roWSL/README.md` — overview and laboratory steps
- `07roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `07roWSL/docs/fisa_comenzi.md` — useful commands
- `07roWSL/src/` — Python code examples
- `07roWSL/homework/` — similar exercises


### 📁 `13roWSL/` — Security

**What you'll find relevant:**
- Detectarea atacurilor, logging

**Recommended files:**
- `13roWSL/README.md` — overview and laboratory steps
- `13roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `13roWSL/docs/fisa_comenzi.md` — useful commands
- `13roWSL/src/` — Python code examples
- `13roWSL/homework/` — similar exercises


### 📁 `06roWSL/` — NAT/PAT

**What you'll find relevant:**
- Firewall rules, NAT traversal

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
