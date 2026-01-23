# Project 14: Securitatea rețelelor – simularea unui sistem de detecție a intruziunilor (IDS/IPS)

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
https://github.com/[username]/retele-proiect-14
```

#### Required Repository Structure

```
retele-proiect-14/
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

**Format:** `NUME_Prenume_GGGG_P14_TT.zip`

| Field | Description | Example |
|------|-----------|---------|
| NUME | Family name (UPPERCASE, no diacritics) | POPESCU |
| Prenume | First name (first letter capitalised) | Ion |
| GGGG | Group number (4 digits) | 1098 |
| P14 | Project number | P14 |
| TT | Deliverable type (S1-S4 or SXX) | E1 |

**Examples for this project:**
- `POPESCU_Ion_1098_P14_E1.zip` — Stage 1
- `POPESCU_Ion_1098_P14_E2.zip` — Stage 2
- `POPESCU_Ion_1098_P14_S07.zip` — Verification săptămâna 7

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

Descriere: Proiectul abordează o temă critică din security rețelelor: detectarea and prevenirea intruziunilor. Studenții vor proiecta and implementa un mediu de network virtual (using instrumente precum mașini virtuale, containere Docker or even Mininet) în which vor configura un Sistem de Detecție a Intruziunilor (IDS) de tip network, for example Snort or Suricata and vor simula diverse atacuri cibernetice for a testa capacitatea sistemului de a le detecta and, optional, bloca. Network de test ar putea consta într-un segment protejat (o mașină victimă which găzduiește un service vulnerabil – for example un server web intenționat neactualizat) and un segment extern de pe which se lansează atacurile (o mașină attackera). IDS-ul va fi plasat fie ca sondă de monitorizare a traficului (conectat la un port mirroring al unui switch virtual or în modules inline if se dorește and prevenție). Scenariile de atac simulate can include: scanări de ports (using nmap), atacuri de tip DoS simple (ping flood), încercări de exploatare a unor vulnerabilități cunoscute (ex: un SQL injection or un buffer overflow for which există semnături Snort) or acces neautorizat (bruteforce pe SSH, etc.). Studenții vor configura regulile IDS so that acesta să alerteze la detectarea acestor activități suspecte. De example, can fi folosite seturile de reguli default (Emerging Threats) and/or can scrie reguli personalizate Snort for anumite tipare de traffic. For partea de prevenție (IPS), if is abordată, se can activa modules inline al Snort/Suguri which blochează pachetele malițioase (or, mai simple, scripturi which adaugă dynamic firewall rules – iptables – când IDS semnalează un atac). Proiectul has o componentă aplicativă very puternică: studenții vor învăța practic cum se instalează and configurează un IDS open-source, cum se interpretează alertele generate and cum se can corela these alerte cu acțiunile unui atacator. Se pune accent and pe metodologie – for example, rularea unor teste controlate for a “înscrie” amprenta unui atac în traffic and a verifica if sistemul o recunoaște. Din point de vedere pedagogic, project consolidează cunoștințele de security network through experimentare directă, evidențiind atât beneficiile utilizării IDS (vizibilitate sporită asupra traficului and atacurilor) cât and limitările acestora (alerte fals pozitive, incapacitatea de a detecta atacuri necunoscute etc.). La final, team va prezenta rezultatele sub forma unui report de security ce sumarizează atacurile încercate and modules în which have been (or nu) detectate and blocate.

### 🎯 Learning Objectives


### 📖 Key Concepts

Technologies Involved: Distribuții Linux (ex: Ubuntu) for instalarea instrumentelor de security; Snort 2.x or 3.x (or Suricata) ca motor IDS – cu actualizarea regulilor de la comunitatea Emerging Threats; Wireshark for analiza detaliată a traficului la nivel de packet; Nmap for scanări de ports and recunoaștere; eventual Metasploit or exploit-uri dedicate for a genera traffic malițios (if se dorește simularea unui atac specific); Scapy (bibliotecă Python) or hping3 for a fabrica packets custom, utile în testing anumitor semnături; Docker or Mașini Virtuale (VirtualBox/VMware) for a crea medii izolate (for example un container rulând Snort which monitorizează network host-ului, etc.); scripturi Bash/Python for automatizarea testelor (ex: trimiterea unui val de packets and observarea reacției IDS). Se can utiliza and Mininet for a construi rapid o topology virtuală (de ex. host1 = atacator, host2 = server, cu un switch central and IDS conectat pasiv la switch through port mirroring – Mininet suportă thus de configurări).
Legătura cu weeks and kiturile (WEEK1-14): Proiectul is ancorat în materia din săptămâna 13, dedicată securității rețelelor, unde have been discutate concepte de scanare de ports, vulnerabilități and unelte de security. Kitul practic al săptămânii 13 probabil conține exerciții introductive cu nmap and can examples de output de la Snort, oferind studenților punctul de plecare for propriile experimente. Proiectul se bazează pe cunoștințe din săptămâna 7 (interceptarea pachetelor, implementation unui filtru de packets) – which oferă fundamentele privind structurarea pachetelor and modules de filtrare, elemente direct relevante for definirea regulilor IDS. Noțiunile din primele weeks referitoare la protocoalele de network (IP, TCP, UDP – weeks 3-5) has indispensabile for a înțelege vectorii de atac (for example, ce înseamnă un TCP SYN flood or un scan FIN). Proiectul vine ca o încununare a acestor cunoștințe, aplicându-le într-un context practic de security and pregătește studenții să coreleze aspectele teoretice de network cu probleme reale din industrie (securizarea infrastructurii).
Structura project în 4 stages: - Stage 1 (săptămâna 5): Proiectarea mediului de test and pregătirea infrastructurii. Echipa va decide ce topology de network and ce scenarii de atac să abordeze. Se stabilește, for example: un server victimă (ce service rulează, pe ce ports), tipurile de atacuri ce vor fi simulate and unde va fi plasat IDS-ul. Totodată, se alege platforma: VM-uri separate (ex: o VM Kali Linux ca atacator, o VM Ubuntu ca server+IDS) or containere pe aceeași mașină. În this stage, studenții instalează efectiv software-ul necesar – for example, instalarea Snort and a dependențelor sale, obținerea fișierelor de reguli default. Se realizează un test initial al IDS-ului într-un mediu simplificat: rularea Snort în modules sniffer for a vedea că can capta traffic or rularea unei comenzi snort -T for a verifica sintaxa configurației. Tot now, se documentează planul de atac: ce comenzi vor fi folosite for port scan, ce exploit (if e cazul) va fi încercat etc., asigurându-se că has disponibile instrumentele respective (instalare nmap, etc.). - Stage 2 (săptămâna 9): Executarea primelor teste de intruziune and calibrarea sistemului IDS. Până la this moment, team va fi configurat IDS-ul în network de test and va începe să lanseze atacuri simple for a genera alerte. De example, se can porni Snort în modules IDS cu un set de reguli de bază and se lansează un scan de ports intens de pe mașina atacator (nmap -T4 -p- VictimIP). Se observă if Snort generează alertă (“Nmap scan detected” or similar). If nu, studenții analizează de ce – can regula nu era activă or traffic nu ajungea la Snort – and make ajustări (activează all regulile relevante, se asigură că Snort ascultă pe interfața corectă). Se continuă cu alte atacuri de bază: un ping flood (using ping -f or hping3) for DoS and eventual un mic atac web (if server victimă e un web server, se can trimite cereri conținând cunoscute string-uri de atac XSS/SQLi). La each pas, se vor colecta alertele and se va verifica corelația lor cu acțiunile întreprinse. Stage 2 has rolul de tunare: team va ajusta sensibilitatea sistemului (eliminarea unor reguli which provoacă false pozitive irelevante for test, modificarea priorităților etc.) so that mediul de test să fie pregătit for scenariile complexe. - Stage 3 (săptămâna 13): Scenarii avansate de atac and implementation contramăsurilor. În this stage final de dezvoltare, se derulează testele complexe planificate. De pildă, se can simula un atac de tip Brute Force asupra serviciului SSH al victimei (using un tool ca hydra or medusa for a încerca multiple passwords) – Snort ar trebui să emită alerte de tip “Multiple login failures” if has regula corespunzătoare. Un alt scenariu ar fi utilizarea unui exploit real: if victima has un service vulnerabil cunoscut (ex. DVWA – Damn Vulnerable Web App or un vsftpd backdoor), se lansează exploit-ul and se vede if IDS-ul îl detectează (multe IDS have semnături for exploit-uri populare). For prevenție, se can activa Snort în modules inline (if topology permite) or, mai simple, team can crea un script integrat cu log-urile Snort: for example, un script Python/Bash which rulează continuu, parsează file de alerte and când vede o alertă critică (ex: “ATTACK DETECTED from X”) adaugă imediat o regulă iptables de blocare a IP-ului sursă X. Thus, se demonstrează acțiunea de IPS. All these scenarii has rulate de câteva ori for a aduna date: log-urile Snort (alerte declanșate, timestamp-uri), comportamentul sistemului (ex: server a blocat efectiv atacatorul after declanșarea IPS). Studenții vor aduna and statistici agregate, for example număr de alerte per tip de atac, rata de succes a detecției. Totodată, vor verifica if have existat atacuri “scăpate” nedetectate and vor nota posibile motive (can lipsa unei semnături or traffic criptat pe which Snort nu îl can inspecta). - Stage 4 (prezentarea în săptămâna 14): Prezentarea final va have forma unui report de security and a unei demonstrații practice. În report, team va descrie pe scurt configuration mediului (topology, versiunea de Snort/Suricata, tipuri de reguli activate, eventuale personalizări făcute) and va lista scenariile de atac testate, împreună cu capturi de ecran or extrase din log-uri which arată detecția. De example, for un port scan se can include alerta Snort generată (cu ID-ul semnăturii), for un exploit web se can arăta log-ul cu payload-ul detectat. Se va discuta eficacitatea: which atacuri have been imediat detectate, which have necesitat ajustări, if have existat alarme false (for example, Snort ar putea marca un traffic legitim ca suspect – studenții vor menționa if have întâlnit thus de situații and cum le-have mitigat). În cadrul demonstrației live, team can relua unul among atacurile emblematice (de pildă un portscan or un DoS mic) and arăta audienței cum apare alerta în consola IDS or cum IP-ul atacator is blocat automat de firewall (if have IPS). Prezentarea se va încheia cu concluzii privind utilitatea practicii: studenții vor reflecta asupra faptului că un IDS oferă un nivel crucial de vizibilitate în network[4], but că administrarea lui necesită finețe (tunarea regulilor, actualizarea constantă a semnăturilor). Ei can sugera and lucrări viitoare, for example integrarea cu un sistem SIEM or testing pe traffic criptat (TLS), arătând thus o înțelegere matură a subiectului.

### 🔮 VERIFICARE ÎNȚELEGERE - CONCEPTE REȚEA

Before de configuration, verificați că înțelegeți:

1. Ce tip de address is 192.168.1.50?
 → Address privată (RFC 1918), nu can fi rutată direct pe Internet

2. Câte addresses IP utilizabile has într-o network /24?
 → 254 addresses (256 total minus 1 for network minus 1 for broadcast)

3. Ce rol has NAT în network voastră?
 → Traduce adresele IP private în address publică for acces Internet


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


### Extensii for teams de 3 vs. 2/1 members: O team de 3 students can explora în profunzime aspecte suplimentare de security. De example, can implementa un sistem hibrid IDS (network + host-based): pe lângă Snort, să configureze and OSSEC or Wazuh (IDS la nivel de gazdă) pe server victimă, corelând alertele ambelor sisteme for o imagine mai cuprinzătoare. Or can configura Suricata în paralel cu Snort for a compara detecția (analizând diferențele de alerte generate de cele două motoare pe același traffic). În plus, echipele mai mari can extinde gama atacurilor testate – for example includerea unui atac de tip Man-in-the-Middle (cu ARP poisoning în Mininet, for example) or un malware beaconing (simulat) for a vedea if IDS-ul detectează comunicații anormale. For echipele de 2 students, setul de atacuri can fi mai restrâns (se can concentra pe 2-3 tipuri principale, cum ar fi portscan, DoS, exploit). Configurațiile can fi simplificate, de pildă rulând totul pe o singură mașină cu Snort ascultând pe interfața loopback (limitat but suficient for a demonstra conceptul). Even and only cu Snort and without partea de IPS, studenții în team mică can obține un project reușit if demonstrează câteva detecții corecte and prezintă o înțelegere solidă a motivelor tehnice. For un singur student, project ar putea fi limitat la folosirea exclusiv a setului de reguli predefinite and simularea unor atacuri very clare (ex: folosirea traficului din kitul de laborator or PCAP-uri cunoscute instead of generarea manuală). Indiferent de mărimea echipei, se va aprecia calitatea interpretării rezultatelor and modules sistematic în which have been abordați pașii de testing.


═══════════════════════════════════════════════════════════════════════════════
📊 CERINȚĂ SUPLIMENTARĂ: ANALIZĂ COMPARATIVĂ
═══════════════════════════════════════════════════════════════════════════════
Pe lângă implementation tehnică, includeți în raportul final o secțiune de analiză comparativă (1-2 pagini) which să conțină:

1. COMPARAȚIE CU ALTERNATIVE
 • Identificați at least 2 tehnologii/abordări alternative for problema rezolvată
 • Argumentați de ce ați ales abordarea actuală

2. METRICI DE PERFORMANȚĂ
 Măsurați and raportați at least 2 metrici relevante:
 • Latență (timp de răspuns) or Throughput
 • Timp de convergență or Utilizare resurse

3. LIMITĂRI ȘI ÎMBUNĂTĂȚIRI
 • Ce limitări conștiente has soluția voastră?
 • Cum ar putea fi extinsă or îmbunătățită?
═══════════════════════════════════════════════════════════════════════════════


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


### 📁 `13roWSL/` — Security

**What you'll find relevant:**
- Snort/Suricata, reguli de detecție

**Recommended files:**
- `13roWSL/README.md` — overview and laboratory steps
- `13roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `13roWSL/docs/fisa_comenzi.md` — useful commands
- `13roWSL/src/` — Python code examples
- `13roWSL/homework/` — similar exercises


### 📁 `07roWSL/` — Interceptare Pachete

**What you'll find relevant:**
- Captură traffic, analiza pattern-urilor

**Recommended files:**
- `07roWSL/README.md` — overview and laboratory steps
- `07roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `07roWSL/docs/fisa_comenzi.md` — useful commands
- `07roWSL/src/` — Python code examples
- `07roWSL/homework/` — similar exercises


### 📁 `04roWSL/` — Protocoale Custom

**What you'll find relevant:**
- Parsarea payload-urilor for detecție

**Recommended files:**
- `04roWSL/README.md` — overview and laboratory steps
- `04roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `04roWSL/docs/fisa_comenzi.md` — useful commands
- `04roWSL/src/` — Python code examples
- `04roWSL/homework/` — similar exercises


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
