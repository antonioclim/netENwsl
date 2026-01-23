# Project 17: Proiectarea unei networks locale cu NAT and DHCP în Cisco Packet Tracer

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
https://github.com/[username]/retele-proiect-17
```

#### Required Repository Structure

```
retele-proiect-17/
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

**Format:** `NUME_Prenume_GGGG_P17_TT.zip`

| Field | Description | Example |
|------|-----------|---------|
| NUME | Family name (UPPERCASE, no diacritics) | POPESCU |
| Prenume | First name (first letter capitalised) | Ion |
| GGGG | Group number (4 digits) | 1098 |
| P17 | Project number | P17 |
| TT | Deliverable type (S1-S4 or SXX) | E1 |

**Examples for this project:**
- `POPESCU_Ion_1098_P17_E1.zip` — Stage 1
- `POPESCU_Ion_1098_P17_E2.zip` — Stage 2
- `POPESCU_Ion_1098_P17_S07.zip` — Verification săptămâna 7

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

Descriere: This project urmărește crearea and configuration unei mici networks locale (LAN) într-un mediu simulat (Cisco Packet Tracer), punând accent pe mecanismele de adresare IP and acces la Internet through NAT. Studenții vor proiecta o topology ce include at least un router, un switch and un set de computers/clients. Router-ul va fi configurat să aloce addresses IP dintr-un domeniu privat using DHCP (Dynamic Host Configuration Protocol) and să realizeze NAT (Network Address Translation) for a permite dispozitivelor din network locală accesul towards o network externă (simulând Internetul). Se vor aplica concepte de subnetting for a configura adresele IP eficient. Proiectul has un caracter practic de network design and administrare, oferind studenților oportunitatea de a pune cap la cap componentele studiate (adresare IP, routing de bază, traducerea adreselor) într-un example realist de network de companie mică or domiciliu.

### 🎯 Learning Objectives


### 📖 Key Concepts

Technologies Involved: Cisco Packet Tracer (instrument de simulare a rețelelor), echipamente Cisco simulate (Router Cisco, Switch Cisco, PC-uri), protocol DHCP, protocol NAT (implementat pe router conform standardelor RFC)[3], protocols ICMP (for ping), TCP/UDP (for testing traficului through NAT), eventual configurări de routing (statis or dinamice de bază). Nu is necesar hardware real, toată implementation având loc în mediu virtual.
Legătura cu weeks and kiturile: Proiectul se leagă direct de materialul din săptămâna 5 (adresare IP, subnetting IPv4/IPv6) and săptămâna 6 (configurații de network – NAT, DHCP, protocols de configuration and management). Kiturile de laborator relevante includ scheletul de network LAN and exercițiile de configuration a routerelor din weeks 5-6 (for example, un file Packet Tracer de bază cu dispozitive preplasate or examples de configurări de DHCP/NAT). Studenții vor porni de la these examples practice, extinzându-le în project actual. Thus, project consolidează cunoștințele acumulate în prima jumătate a cursului, oferind o perspectivă practică unitară asupra construirii unei networks funcționale.
Structura pe 4 stages: 1. Stage 1: Proiectarea network and stabilirea parametrilor. Se începe cu definirea cerințelor network: numărul de subnets and de host-uri necesare, spațiul de addresses IP disponibil. Echipa realizează un design logic al topologiei (ex: o subnet LAN for stații, un router conectat la Internet simulat). Se calculează un plan de subnetting (for example, dintr-o address de class C privată se determină subrețeaua potrivită). Se documentează adresele IP ce vor fi atribuite (network, gateway, DHCP pool etc.) and se pregătește diagrama topologică. 2. Stage 2: Configuration în Cisco Packet Tracer – partea de bază. Using Packet Tracer, se realizează practic topology propusă: se plasează router-ul, switch-ul and PC-urile and se conectează cu cabluri adecvate. Se configurează interfețele router-ului (for example, interfata LAN cu address statică din subnetul local and interfata WAN cu o address simulând o network publică). Then, se activează and configurează service DHCP pe router (specificând network, masca, gateway-ul, DNS eventual). PC-urile has setate să obțină IP dinamic. After aceea, se configurează NAT pe router: se stabilește which interfață is „inside” and which „outside”, se definește o listă de acces or se folosește comanda simplificată for NAT masquat (PAT) and se verifică traducerile (for example cu show ip nat translations). This stage asigură că network locală has configurate all elementele for conectivitate internă. 3. Stage 3: Testing and ajustări. În this stage, se testează funcționalitatea network. Se pornește each PC, which ar trebui să primească automat o address IP de la DHCP – se verifică în Packet Tracer configuration IP a fiecărui PC. Then, se testează connection towards exterior (for example, routerul can have ca „Internet” un cloud PT conectat or un alt router simulând ISP-ul). Se folosește comanda ping de pe un PC towards o address externă (for example, interfata WAN a routerului ISP) and se observă if există răspuns. If testul e pozitiv, înseamnă că DHCP and NAT funcționează corect. Se can realiza and teste suplimentare: for example, trimiterea unui ping din exterior towards un PC din LAN (which ar trebui blocat implicit de NAT, evidențiind faptul că LAN-ul nu is direct accesibil din afară). Echipa va depana eventualele probleme (de ex., if PC-urile nu obțin IP, se verifică setările DHCP; if nu funcționează NAT, se verifică if interfețele inside/outside have been corect desemnate). Se finalizează configurările adăugând eventual un server DNS simulativ or alte elemente if has necesare for test (optional). 4. Stage 4: Documentare and optimizare. În ultima stage, se realizează documentation project. Aceasta include diagrama network, tabele cu adresele IP alocate, configurațiile relevante extrase de pe router (ex. output de la show run filtrat for DHCP and NAT). Totodată, se descrie modules în which s-a realizat configuration pas cu pas and se explică de ce setările alese has corecte. Se analizează funcționalitatea: team argumentează cum DHCP ușurează administrarea (față de configuration manuală) and cum NAT permite reutilizarea adreselor private and oferă un nivel de izolare a network interne. If have existat provocări or optimizări (ex. ajustarea mărimii pool-ului DHCP, rezervarea unor addresses fixe, implementation de liste de acces for security rudimentară), acestea has discutate. Documentația se încheie cu concluzii about experiența practică dobândită în configuration unei networks reale la scară mică.
Extensii for teams de 3/2/1: - Teams de 3 persons: Se va extinde project la o topology puțin mai complexă. De example, în locul unei singure networks LAN, se can configura două subnets LAN distincte (departamente diferite) interconectate through router, necesitând rutare statică or even un protocol de rutare dinamică de bază (ex. OSPF pe intern). Each subnet va have propriul pool DHCP. Routerul va fi configurat cu NAT for ambele subnets towards Internet. Echipa can integra and IPv6 în project (configurând dual-stack cu DHCPv6 or SLAAC for experiență suplimentară). These extinderi aduc provocări suplimentare de configuration and oferă ocazia de a demonstra cunoștințe mai avansate (ex. operarea unui protocol de rutare). - Teams de 2 persons: Vor implementa scenariul de bază prezentat, cu o singură network LAN deservită de DHCP and acces la Internet through NAT. All requirements principale (DHCP functional, NAT functional, conectivitate verificată) must realizate. Extensiile complexe precum a doua subnet or IPv6 nu has necesare, however team can opta for mici îmbunătățiri, for example definirea unui DNS server local în configuration DHCP or testing funcției de Port Forwarding (NAT static) for a înțelege cum ar expune un server intern towards Internet. - Teams de 1 person: Un singur student va realiza o versiune simplificată a project. De example, if configuration DHCP and NAT simultan is prea complexă de gestionat individual, se can limita la DHCP + NAT pe o singură network cu un număr redus de host-uri. Studentul can folosi configurații mai simple (ex. un singur PC client în LAN) for a demonstra conceptul. Optional, se can permite configuration manuală a IP-urilor pe PC-uri instead of DHCP, if se dorește reducerea complexității – accentul rămânând pe înțelegerea NAT. Important is ca studentul să explice în report configurațiile făcute and să demonstreze că a obținut conectivitate la Internet din LAN. Extensiile opționale nu has necesare în cazul proiectelor individuale, but o discuție about cum s-ar putea extinde network pe viitor can fi apreciată.

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

Ambiyar, A., Yondri, S., Irfan, D., Putri, M. D., Zaus, M. A., & Islami, S. (2019). Evaluation of Packet Tracer Application Effectiveness in Computer Design Networking Subject. International Journal on Advanced Science, Engineering and Information Technology, 9(1), 78–85. DOI: 10.18517/ijaseit.9.1.5931
Srisuresh, P., & Egevang, K. (2001). Traditional IP Network Address Translator (Traditional NAT). RFC 3022, IETF. DOI: 10.17487/RFC3022
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


---

## 📚 RELEVANT LABORATORY MATERIALS

Consultă these resurse din arhiva **netROwsl** for conceptele necesare:


### 📁 `06roWSL/` — NAT/PAT

**What you'll find relevant:**
- Configuration NAT, port forwarding

**Recommended files:**
- `06roWSL/README.md` — overview and laboratory steps
- `06roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `06roWSL/docs/fisa_comenzi.md` — useful commands
- `06roWSL/src/` — Python code examples
- `06roWSL/homework/` — similar exercises


### 📁 `05roWSL/` — Adresare IP

**What you'll find relevant:**
- DHCP, alocare dinamică addresses

**Recommended files:**
- `05roWSL/README.md` — overview and laboratory steps
- `05roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `05roWSL/docs/fisa_comenzi.md` — useful commands
- `05roWSL/src/` — Python code examples
- `05roWSL/homework/` — similar exercises


### 📁 `01roWSL/` — Fundamentele Rețelelor

**What you'll find relevant:**
- Topologii LAN, adresare

**Recommended files:**
- `01roWSL/README.md` — overview and laboratory steps
- `01roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `01roWSL/docs/fisa_comenzi.md` — useful commands
- `01roWSL/src/` — Python code examples
- `01roWSL/homework/` — similar exercises


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
