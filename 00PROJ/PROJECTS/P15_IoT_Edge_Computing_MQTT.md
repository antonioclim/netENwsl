# Project 15: Simularea unei networks IoT cu procesare de tip Edge Computing

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
https://github.com/[username]/retele-proiect-15
```

#### Required Repository Structure

```
retele-proiect-15/
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

**Format:** `NUME_Prenume_GGGG_P15_TT.zip`

| Field | Description | Example |
|------|-----------|---------|
| NUME | Family name (UPPERCASE, no diacritics) | POPESCU |
| Prenume | First name (first letter capitalised) | Ion |
| GGGG | Group number (4 digits) | 1098 |
| P15 | Project number | P15 |
| TT | Deliverable type (S1-S4 or SXX) | E1 |

**Examples for this project:**
- `POPESCU_Ion_1098_P15_E1.zip` — Stage 1
- `POPESCU_Ion_1098_P15_E2.zip` — Stage 2
- `POPESCU_Ion_1098_P15_S07.zip` — Verification săptămâna 7

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

Descriere: This project explorează domeniul emergent al Internetului Lucrurilor (IoT) and al procesării la marginea network (Edge Computing) through realizarea unei simulări a unei networks de dispozitive inteligente conectate. Scopul is construirea unui mediu în which multiple “dispozitive” IoT (simulate software) colectează and transmit date towards un nod central de tip edge (gateway local), which realizează prelucrări primare ale datelor and le trimite mai departe towards un service de cloud (simulat) for stocare or analiză aprofundată. În termeni practici, studenții vor implementa un set de noduri senzori (for example, simulând citiri de temperatură, umiditate, mișcare or alți parametri) which se conectează through network la un broker de mesaje IoT (precum MQTT broker – for example Eclipse Mosquitto). Dispozitivele vor publica periodic datele colectate pe anumite topici MQTT, while nodul edge (un subsistem local, posibil un mini-server) va acționa ca abonat la these topici, agregând informațiile de la senzori. This edge server can efectua calcul local – for example, filtrarea datelor (eliminarea anomaliilor), combinarea valorilor de la mai mulți senzori or declanșarea unor alerte if valorile depășesc praguri – demonstrând avantajul edge computing: reducerea volumului de date trimis spre cloud and răspuns mai rapid la evenimente locale. Datele prelucrate sumar de edge vor fi then transmise towards un service central (cloud) for arhivare or analiza globală (în practică ar putea fi o bază de date centrală or un dashboard web; în simulare, can fi un alt proces which primește these date). Comunicarea among edge and cloud se can makes tot printr-un protocol standard (MQTT, HTTP REST API, etc.). Proiectul pune accent pe aspectele de network and protocols specifice IoT: comunicare publish-subscribe, gestionarea unui număr potențial mare de dispozitive, limitări de lățime de bandă and latență, formatele ușoare de mesaje (JSON, CBOR). Totodată, aspecte de security can fi abordate – autentificarea dispozitivelor la broker, transmisia criptată TLS (if timpul permite). Pedagogic, studenții vor înțelege modules în which IoT extinde conceptul de network la miliarde de dispozitive fizice and necesită arhitecturi diferite (de ex. edge computing) for a makes față volumului de date and constrângerilor de timp real. Simularea realizată va oferi oportunitatea de a observa comportamentul network IoT în diferite condiții: for example, ce se întâmplă if un senzor “cade” (nu mai transmite), if latența network crește or if brokerul se aglomerează cu mesaje. Studenții vor putea experimenta and optimizări precum reglarea frecvenței de eșantionare a senzorilor or folosirea unor mecanisme de buffering la edge.

### 🎯 Learning Objectives


### 📖 Key Concepts


### 🛠️ Technologies and Tools

Legătura cu weeks and kiturile (WEEK1-14): Deși subiectul IoT nu apare explicit în programa primelor 13 weeks, project se bazează pe principiile generale de networks predate de-a lungul cursului and le aplică într-un context modern. În special, conceptul de arhitectură distribuită din săptămâna 12 (RPC and comunicarea inter-proces) is extins here sub altă formă (comunicare publish-subscribe). De asemenea, săptămâna 8 privind protocoalele la nivel de application (HTTP, arhitecturi client-server) oferă un contrast față de modelul pub-sub utilizat în MQTT – studenții vor putea compara cele două paradigme. Tematica de security din săptămâna 13 se leagă de project through discuțiile de security IoT (IoT aduce probleme speciale de security, cum ar fi dispozitive slab protejate, comunicații necriptate, etc., ce can fi amintite în project). Even and aspecte din săptămâna 5-6 (rutare, adresare) has relevante: într-o network IoT, alocarea adreselor IP (posibil IPv6 for număr mare de dispozitive) and rutarea eficientă (protocole specifice rețelelor de senzori, cum ar fi RPL) has subiecte de interes – acestea can fi menționate teoretic. Through urmare, project funcționează ca o sinteză and application practică integratoare, demonstrând aplicarea conceptelor de network într-un scenariu actual de IoT, even if nu a been detaliat la curs – abordarea being conformă cu obiectivele disciplinei de a conecta cunoștințele la tendințele recente.
Structura project în 4 stages: - Stage 1 (săptămâna 5): Definirea scenariului IoT and a arhitecturii de sistem. Echipa stabilește contextul: for example, “monitorizarea inteligentă a clădirilor” cu senzori de temperatură and mișcare pe each etaj or “agricultură smart” cu senzori de umiditate în sol and temperatură aer transmițând date la un nod edge aflat la fermă which decide irigarea, etc. Se delimitează clar ce tipuri de senzori vor fi simulați and ce fel de date vor transmite (inclusiv unități, interval de valori). Then se schițează arhitectura: câți senzori (procese) vor exista, ce broker se folosește, ce makes nodul edge cu datele, cum transmite mai departe la cloud. Se va alege protocol de comunicare – cel mai probabil MQTT for senzor->edge and tot MQTT or HTTP for edge->cloud. În this stage se pregătesc and mediile: instalarea broker-ului MQTT (Mosquitto) local or într-un container Docker, testing lui minimală (ex: se încearcă o subscriere and o publicare manual, cu utilitare mosquitto_pub and mosquitto_sub). Se documentează formatul mesajelor ce vor fi transmise (e.g., JSON: { sensor_id: "S1", value: 23.5, unit: "C" }). - Stage 2 (săptămâna 9): Implementarea prototipurilor for senzori and nodul edge – flux simple de date. Până la sfârșitul acestei stages, studenții vor realiza un prim sistem functional simplificat: for example, un singur senzor scriptat în Python which publică date fictive towards broker and nodul edge which primește these date and le afișează or loghează. Se testează comunicarea publish-subscribe end-to-end. Tot now se implementează and partea de trimitere towards “cloud” a datelor de la edge (even if initial cloud-ul can fi only un log pe disc). Accentul is pe a valida că all componentele can comunica: senzor -> broker (mesaj publicat corect and recepționat de edge) -> edge -> (eventual HTTP POST) -> cloud. If se folosesc multiple subiecte, se verifică că edge-ul se abonează la all cele necesare. Se can folosi date de test generate simple (ex: valori random for senzori) only for a exercita sistemul. La this stadiu, se can identifica and eventuale probleme de configuration (for example, mărimea maximă a mesajelor MQTT or time-out la client) and se rezolvă. - Stage 3 (săptămâna 13): Extinderea simulării la mai multe dispozitive, introducerea procesării edge and assessment performanței. Aceasta is stage de realizare integrală a scenariului. Se lansează multipli senzori – for example, se generalizează scriptul de senzor so that through parametri diferiți (or instanțe diferite) să reprezinte senzori diferiți (can even de tipuri diferite: temperatură, umiditate, etc.). Se configurează un interval de publicare realist (ex: la each 5 secunde un senzor trimite o valoare). Nodul edge devine mai inteligent: se implementează logica de agregare/filtrare – de pildă, calculul mediei temperaturilor din ultimele N citiri for a trimite la cloud only media la each minut (instead of each valoare individuală) or detectarea unei condiții de alertă (if 3 senzori de mișcare declanșează simultan, edge-ul trimite un eveniment “alarmă” towards cloud). Then se realizează teste de încărcare: for example, se crește numărul de senzori or frecvența cu which trimit date and se observă cum makes față sistemul (broker-ul MQTT has vreun delay, edge-ul consumă mult CPU?). Se can adăuga and testări de reziliență: se oprește temporar broker-ul or nodul cloud for a vedea ce se întâmplă cu mesajele (MQTT QoS1/2 can reține mesajele neconfirmate). If se implementează security, now e momentul: configuration autentificării pe broker (utilizatori and passwords for senzori), eventual activarea TLS (cerere de certificate – can complex, but teams avansate can demonstra unul-două noduri comunicând criptat). La finalul acestei stages, sistemul ar trebui să fie capabil să simuleze câteva zeci de dispozitive trimițând date and edge-ul să proceseze and să retransmită rezumate without pierderi notabile. - Stage 4 (prezentarea în săptămâna 14): Echipa va prezenta network IoT simulată printr-o demonstrație and o analiză a comportamentului sistemului. Demonstrația ar putea include rularea în direct a, să zicem, 5 senzori virtuali – se va vedea în consola edge-ului cum primește datele de la each and cum trimite mai departe un mesaj agregat la cloud (can cloud-ul e tot un script ce afișează ce primește). Optional, se can demonstra cum edge-ul reacționează la un eveniment: for example, se crește brusc valoarea simulatǎ a unui senzor (peste un prag) and se arată că edge-ul detectează condiția and trimite alertă imediat towards cloud. În prezentare, studenții vor discuta avantajele observate: for example, volumul de date trimis la cloud a scăzut datorită procesării locale – can cuantifica “without edge trimiteam X mesaje/oră, cu edge trimitem X/2 mesaje/oră” – and latența unei alerte locale is mult mai mică (ex: se declanșează instant local, pe când if s-ar aștepta decizia din cloud, ar fi întârziere mai mare). Vor menționa and limitările întâlnite: for example, complexitatea sincronizării a multor noduri, eventual dificultatea configurării securității. Un aspect important: studenții vor corela experiența lor cu principiile teoretice – de pildă, vor menționa că IoT implică comunicarea autonomă between objects fizice[5] and vor evidenția importanța protocoalelor ușoare precum MQTT for constrângeri de network. Concluziile vor sublinia că project le-a oferit o perspectivă practică asupra modului în which rețelele de computers evoluează for a integra dispozitive IoT and necesitatea edge computing for eficiență.

### 🔮 VERIFICARE ÎNȚELEGERE - IoT ȘI MQTT

Before de a testa sistemul IoT, răspundeți:

1. If senzorul publică pe topic-ul casa/living/temperatura, cine primește mesajul?
 → Toți clienții abonați la this topic or la casa/living/# or casa/#

2. Ce se întâmplă if broker-ul MQTT nu is pornit când senzorul încearcă să publice?
 → Eroare: Connection refused. Senzorul must să implementeze retry logic.

3. Ce nivel QoS ar trebui folosit for date critice (ex: alarmă incendiu)?
 → QoS 2 (Exactly once) for a garanta livrarea mesajului


### 📊 PEER INSTRUCTION - DOCKER ȘI REȚELE CONTAINERE

Discutați cu colegii and alegeți împreună răspunsul corect:

Întrebarea 1: Containerele web and db has în aceeași network Docker bridge. Cum can web să se conecteze la port 5432 al db?

A) localhost:5432 - containerele partajează același localhost
B) db:5432 - Docker DNS rezolvă automat numele serviciului ✓
C) 172.17.0.1:5432 - address gateway-ului bridge
D) host.docker.internal:5432 - referință la mașina host

Explicație: Docker Compose creează DNS intern. Containerele se găsesc through numele serviciului, nu through localhost (which e izolat per container).

Întrebarea 2: Un container expune port 8080:80. Ce înseamnă this configuration?

A) Containerul ascultă pe 8080, host-ul expune pe 80
B) Host-ul ascultă pe 8080, containerul intern pe 80 ✓
C) Ambele ports has echivalente
D) Portul 8080 is blocat de firewall

Explicație: Formatul is HOST_PORT:CONTAINER_PORT. Accesați service din browser la http://localhost:8080


### Extensii for teams de 3 vs. 2/1 members: O team de 3 students can ambiționa un scenariu IoT de scară mai mare or mai complex. De example, can simula 20-30 de senzori and să realizeze scripturi de orchestrare which pornesc automat these entități (posibil even using Docker Compose for a porni multe containere-senzor). Totodată, can diversifica tipurile de device-uri: senzori and and actuatori – de pildă, să includă în simulare un “dispozitiv” actuator (cum ar fi un sistem de udat plantele) which se activează only când primește de la edge comanda (publish pe un topic special) – asta ar implica o buclă închisă de control. Pe zona de cloud, can realiza un mic dashboard web (cu Python/Flask or Node.js) which afișează în timp real datele primite de la edge, ceea ce ar îmbogăți prezentarea vizual. Implementarea securității MQTT (TLS, authentication) ar fi and ea o extensie potrivită for o team numeroasă, având în vedere configuration mai laborioasă. For echipele de 2 students, project can fi ținut la nivelul de bază: ~5-10 senzori, without elemente de actuatori, accent pe funcționalitatea main publish-subscribe and agregare edge. Se can limita la security simple (can only authentication cu password pe broker, without TLS). În cazul unui student individual, se can reduce and mai mult complexitatea – for example 3 senzori trimițând direct la cloud without edge distinct (practic only demonstrând MQTT pub-sub) or un singur senzor which trimite la edge and edge la cloud, for a proba lanțul complete cu minimum de componente. Important is ca and varianta simplificată să respecte paradigmă IoT (senzor, network, consumator date) and studentul să explice cum s-ar extinde la scară mai mare. În all cazurile, assessment va ține cont de nivelul de dificultate asumat voluntar de team and de gradul de realizare a funcționalităților propuse.


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

[1] Kreutz, D., Ramos, F.M.V., Esteves Verissimo, P., Esteve Rothenberg, C., Azodolmolky, S. and Uhlig, S. (2015) Software-Defined Networking A complete Survey. Proceedings of the IEEE, 103, 14-76. - References - Scientific Research Publishing
https://www.scirp.org/reference/referencespapers?referenceid=3911400
[2] Defense-in-Depth Methods in Microservices Access Control
https://trepo.tuni.fi/bitstream/123456789/27172/4/suomalainen.pdf
[3] Remote procedure call - Wikipedia
https://en.wikipedia.org/wiki/Remote_procedure_call
[4] usenix.org
https://www.usenix.org/legacy/event/lisa99/full_papers/roesch/roesch.pdf
[5] A Review on Internet of Things -Protocols, Issues - Academia.edu
https://www.academia.edu/32025103/A_Review_on_Internet_of_Things_Protocols_Issues
---

## 🔮 Verification înțelegere — IoT and MQTT

Before de testing:

1. **Cine primește mesajul publicat pe "casa/living/temp"?**
 - Toți clienții abonați la this topic or "casa/living/#"

2. **Ce se întâmplă if broker-ul MQTT nu rulează?**
 - Eroare: Connection refused

3. **Ce QoS folosim for date critice?**
 - QoS 2 (Exactly once)


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


### 💡 For MQTT and IoT

MQTT e similar cu WebSockets pe which le-ai folosit can în TW:

```python
# WebSocket (TW) vs MQTT (Rețele)

# WebSocket: conexiune bidirecțională client-server
# MQTT: publish/subscribe prin broker

import paho.mqtt.client as mqtt

# Similar cu socket.on('message', callback) din Socket.IO
def on_message(client, userdata, msg):
 print(f"Topic: {msg.topic}, Message: {msg.payload.decode()}")

client = mqtt.Client()
client.on_message = on_message

# Similar cu socket.emit() dar prin broker
client.connect("localhost", 1883)
client.subscribe("casa/living/temp") # Similar cu socket.join('room')
client.publish("casa/living/temp", "22.5") # Similar cu io.to('room').emit()
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


### 📁 `13roWSL/` — IoT and Security

**What you'll find relevant:**
- MQTT, Mosquitto broker, senzori

**Recommended files:**
- `13roWSL/README.md` — overview and laboratory steps
- `13roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `13roWSL/docs/fisa_comenzi.md` — useful commands
- `13roWSL/src/` — Python code examples
- `13roWSL/homework/` — similar exercises


### 📁 `03roWSL/` — Broadcast and Multicast

**What you'll find relevant:**
- Publish/subscribe pattern

**Recommended files:**
- `03roWSL/README.md` — overview and laboratory steps
- `03roWSL/docs/rezumat_teoretic.md` — theoretical concepts
- `03roWSL/docs/fisa_comenzi.md` — useful commands
- `03roWSL/src/` — Python code examples
- `03roWSL/homework/` — similar exercises


### 📁 `10roWSL/` — REST

**What you'll find relevant:**
- Edge gateway, API-uri for senzori

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
