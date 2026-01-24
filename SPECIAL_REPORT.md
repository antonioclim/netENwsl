# Materiale Didactice pentru Rețele de Calculatoare în Universități de Top
## O Analiză Comparativă Independentă

---

<div align="center">

**Studiu Comparativ: Curricula de Computer Networks**  
*Facultăți din Top 100 QS/THE/ARWU vs. Proiectul CLIM&TOMA/ASE-CSIE*

---

*„Dacă vrei să înveți cu adevărat ceva, încearcă să-l predai."*  
— Richard Feynman (probabil la o cafea, ca și noi)

</div>

---

## Disclaimer și Conflict de Interese

Prezentul raport a fost elaborat de autorii materialelor CLIM&TOMA/ASE-CSIE, ceea ce creează un evident conflict de interese. Recunoaștem cu onestitate că obiectivitatea absolută este un ideal către care tindem, nu o certitudine pe care o deținem. Cititorul este invitat să verifice independent sursele citate și să-și formeze propria opinie.

Cu alte cuvinte: da, ne lăudăm puțin, dar încercăm să fim corecți în acest proces.

---

## 1. Introducere și Metodologie

### 1.1. Contextul Cercetării

Proiectul **CLIM&TOMA/ASE-CSIE** (denumit în continuare *proiectul de referință*) a luat naștere din colaborarea dintre **ing. dr. Antonio CLIM** și **conf. dr. Andrei TOMA** de la Academia de Studii Economice din București, Facultatea de Cibernetică, Statistică și Informatică Economică (ASE-CSIE).

Ideea inițială, scripturile de bază și numeroase sesiuni de brainstorming (desfășurate preponderent la cafeneaua **The Dose**, București — un loc care merită credit pentru cantitatea de cofeină investită în acest proiect) au condus la dezvoltarea unui kit de laborator pentru disciplina *Rețele de Calculatoare* care încearcă să îmbine:

- Rigoarea academică cu accesibilitatea practică
- Tehnologiile moderne (Docker, WSL2) cu pedagogia bazată pe evidență
- Comprehensivitatea cu... păi, cu mai multă comprehensivitate

Conf. dr. Andrei TOMA aduce proiectului un talent rar: capacitatea de a reduce concepte complicate la esența lor reală — o abilitate care, în experiența noastră, valorează mai mult decât orice framework sofisticat.

### 1.2. Metodologie

Am analizat **peste 20 de cursuri de rețele** de la universități din Top 100 (conform QS World University Rankings, Times Higher Education și ARWU), concentrându-ne pe materialele disponibile public pe GitHub și platforme educaționale deschise.

**Criterii de evaluare:**

| Cod | Dimensiune | Descriere |
|:---:|:-----------|:----------|
| **C1** | Comprehensivitate | Număr de săptămâni, acoperire tematică |
| **C2** | Calitatea Codului | Type hints, docstrings, standarde |
| **C3** | Sofisticare Pedagogică | Metode bazate pe evidență (peer instruction, misconceptions) |
| **C4** | Infrastructură | Docker, virtualizare, verificare mediu |
| **C5** | Documentație | README, ghiduri, cheatsheets, glosare |
| **C6** | Proiecte | Varietate, scală, lucru în echipă |
| **C7** | Elemente Interactive | Prezentări HTML, quiz-uri, demo-uri |

---

## 2. Peisajul Academic: Cine Face Ce și Cum

### 2.1. Universități și Cursuri Analizate

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    GEOGRAFÍA CURSURILOR ANALIZATE                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   🇺🇸 SUA                          🇪🇺 Europa                           │
│   ├── Stanford CS144               ├── ETH Zürich (227-0120-00L)       │
│   ├── UC Berkeley CS168            ├── EPFL (COM-208)                  │
│   ├── CMU 15-441/641               ├── TU München                      │
│   ├── MIT 6.829                    ├── UCLouvain CNP3                  │
│   ├── Princeton COS 461            └── Imperial College                │
│   ├── U. Michigan EECS 489                                             │
│   ├── UIUC ECE 438                 🇦🇸 Asia                            │
│   ├── Georgia Tech CS 6250         ├── KAIST CS341                     │
│   ├── Johns Hopkins EN.601.414     ├── NUS CS2105                      │
│   └── UT Austin                    ├── Tsinghua                        │
│                                    ├── CUHK CSCI 4430                  │
│   🇷🇴 România                       └── Peking University               │
│   └── ASE-CSIE (CLIM&TOMA)                                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2. Tabelul Comparativ Principal

> **Legendă**: ✅ Complet implementat | ⚠️ Parțial/Comunitar | ❌ Absent/Nedocumentat

<table>
<thead>
<tr style="background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%); color: white;">
<th>Universitate</th>
<th>Curs</th>
<th>Săpt.</th>
<th>Docker</th>
<th>Prezent. Interactive</th>
<th>Pedagogie Explicită</th>
<th>Proiecte</th>
<th>Auto-test</th>
</tr>
</thead>
<tbody>
<tr style="background: #e8f5e9;">
<td><strong>🇷🇴 ASE-CSIE</strong></td>
<td><strong>CLIM&TOMA</strong></td>
<td><strong>14</strong></td>
<td>✅</td>
<td>✅ HTML/CSS</td>
<td>✅ Peer Instr., Misconc.</td>
<td><strong>15+ grup</strong></td>
<td>✅</td>
</tr>
<tr>
<td>🇺🇸 Stanford</td>
<td>CS144</td>
<td>10</td>
<td>⚠️</td>
<td>❌ PDF</td>
<td>⚠️ Lab hints</td>
<td>8 individ.</td>
<td>✅</td>
</tr>
<tr style="background: #f5f5f5;">
<td>🇨🇭 ETH Zürich</td>
<td>Comm. Networks</td>
<td>15</td>
<td>✅</td>
<td>❌ Tradițional</td>
<td>❌</td>
<td>2 grup</td>
<td>⚠️</td>
</tr>
<tr>
<td>🇺🇸 Michigan</td>
<td>EECS 489</td>
<td>14-15</td>
<td>⚠️</td>
<td>❌ PDF slides</td>
<td>⚠️ Quizzes</td>
<td>4 grup</td>
<td>✅</td>
</tr>
<tr style="background: #f5f5f5;">
<td>🇺🇸 CMU</td>
<td>15-441/641</td>
<td>~14</td>
<td>✅</td>
<td>❌</td>
<td>❌</td>
<td>3 multi-săpt.</td>
<td>✅</td>
</tr>
<tr>
<td>🇺🇸 Berkeley</td>
<td>CS168</td>
<td>17</td>
<td>⚠️</td>
<td>⚠️ Google Slides</td>
<td>❌</td>
<td>3 proiecte</td>
<td>✅</td>
</tr>
<tr style="background: #f5f5f5;">
<td>🇺🇸 Princeton</td>
<td>COS 461</td>
<td>12</td>
<td>⚠️</td>
<td>❌ Video flip.</td>
<td>❌</td>
<td>5 labs</td>
<td>✅</td>
</tr>
<tr>
<td>🇰🇷 KAIST</td>
<td>CS341 (KENSv3)</td>
<td>16</td>
<td>✅</td>
<td>❌</td>
<td>✅ PCAP/Wireshark</td>
<td>4 individ.</td>
<td>✅</td>
</tr>
<tr style="background: #f5f5f5;">
<td>🇧🇪 UCLouvain</td>
<td>CNP3</td>
<td>Var.</td>
<td>✅</td>
<td>❌ PPT/Keynote</td>
<td>✅ INGInious</td>
<td>Multiple</td>
<td>✅</td>
</tr>
<tr>
<td>🇺🇸 NPS</td>
<td>Labtainers</td>
<td>Modul.</td>
<td>✅</td>
<td>❌ PDF manuale</td>
<td>✅ Individualizat</td>
<td>50+ labs</td>
<td>✅</td>
</tr>
</tbody>
</table>

---

## 3. Analiza Detaliată pe Dimensiuni

### 3.1. Dimensiunea C1: Comprehensivitate

```
Număr de Săptămâni de Curs

Berkeley CS168     ████████████████████████████████░░  17 săpt.
KAIST CS341        ███████████████████████████████░░░  16 săpt.
ETH Zürich         █████████████████████████████░░░░░  15 săpt.
Michigan EECS 489  ████████████████████████████░░░░░░  14-15 săpt.
CLIM&TOMA/ASE-CSIE ███████████████████████████░░░░░░░  14 săpt.  ◄── Proiect referință
CMU 15-441         ███████████████████████████░░░░░░░  ~14 săpt.
Princeton COS 461  ███████████████████████░░░░░░░░░░░  12 săpt.
Stanford CS144     ████████████████████░░░░░░░░░░░░░░  10 săpt. (trimestru)
```

**Observație**: Berkeley CS168 conduce la capitolul amploare (17 săptămâni), însă formatul trimestrial de la Stanford (10 săptămâni) compensează prin densitate. Cursul CLIM&TOMA/ASE-CSIE se poziționează în intervalul superior, alături de Michigan și CMU.

**Acoperire tematică comparativă:**

| Topic | Stanford | ETH | Michigan | Berkeley | CLIM&TOMA |
|:------|:--------:|:---:|:--------:|:--------:|:---------:|
| Fundamente TCP/IP | ✅ | ✅ | ✅ | ✅ | ✅ |
| Socket Programming | ✅ | ✅ | ✅ | ✅ | ✅ |
| HTTP/REST | ✅ | ⚠️ | ✅ | ✅ | ✅ |
| DNS Deep Dive | ⚠️ | ✅ | ✅ | ✅ | ✅ |
| Routing (OSPF, BGP) | ⚠️ | ✅ | ✅ | ✅ | ✅ |
| SDN/OpenFlow | ❌ | ⚠️ | ✅ | ✅ | ✅ |
| Load Balancing | ❌ | ⚠️ | ⚠️ | ✅ | ✅ |
| IoT/MQTT | ❌ | ❌ | ❌ | ❌ | ✅ |
| gRPC/RPC Modern | ❌ | ❌ | ⚠️ | ⚠️ | ✅ |
| Security (TLS, VPN) | ⚠️ | ✅ | ⚠️ | ✅ | ✅ |

### 3.2. Dimensiunea C2: Calitatea Codului

Aici trebuie să fim onești: **Stanford CS144** stabilește standardul pentru cod C++ cu:
- Clang-tidy linting
- ASan/UBSan sanitizers  
- CMake modern
- Coding style guide explicit

**Michigan EECS 489** oferă cel mai consistent cod Python (85.6% din repo).

Proiectul **CLIM&TOMA** folosește Python cu:
- Type hints (parțial)
- Docstrings extinse
- Structură modulară standardizată pe săptămâni

> *Auto-critică*: Am învățat de la Stanford că linting-ul automat nu e un lux, ci o necesitate. Încă lucrăm la integrarea completă.

### 3.3. Dimensiunea C3: Sofisticare Pedagogică (ZONA CRITICĂ)

Aceasta este dimensiunea unde diferențele devin cele mai vizibile:

```
┌──────────────────────────────────────────────────────────────────────────┐
│           ELEMENTE PEDAGOGICE BAZATE PE EVIDENȚĂ                        │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Element                        Prezent în cursuri universitare?         │
│  ─────────────────────────────────────────────────────────────────       │
│                                                                          │
│  Peer Instruction Questions     CLIM&TOMA ✅ | Restul ❌                 │
│  (Mazur-style, 5 steps)                                                  │
│                                                                          │
│  Documented Misconceptions      CLIM&TOMA ✅ | Restul ❌                 │
│  (per topic, with corrections)                                           │
│                                                                          │
│  Prediction Prompts             CLIM&TOMA ✅ | Restul ❌                 │
│  (Brown & Wilson Principle 4)                                            │
│                                                                          │
│  Parsons Problems               CLIM&TOMA ✅ | Restul ❌                 │
│  (code arrangement exercises)                                            │
│                                                                          │
│  Code Tracing Exercises         CLIM&TOMA ✅ | KAIST ⚠️ | Restul ❌     │
│  (step-by-step execution)                                                │
│                                                                          │
│  Pair Programming Guides        CLIM&TOMA ✅ | Restul ❌                 │
│  (Driver/Navigator rotation)                                             │
│                                                                          │
│  Concept Analogies Doc          CLIM&TOMA ✅ | Restul ❌                 │
│  (networking concepts mapped                                             │
│   to everyday experiences)                                               │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

**Cele mai apropiate alternative:**
- **UCLouvain CNP3**: Platforma INGInious pentru exerciții auto-evaluate
- **KAIST KENSv3**: Generare PCAP pentru analiză Wireshark
- **Labtainers (NPS)**: Parametri individualizați per student

> *Notă*: Absența aproape totală a metodelor pedagogice explicite în curricula de elită ne-a surprins. Sau poate nu ar fi trebuit să ne surprindă — există o diferență între a fi un cercetător excelent în networking și a fi un pedagog informat de cercetarea educațională.

### 3.4. Dimensiunea C4: Infrastructură Docker

```
                        MATURITATEA INFRASTRUCTURII

          Nimic    VM basic    Mininet    Docker    Full Stack
            │         │          │          │           │
Stanford ───┼─────────┼──────────┼────⚫─────┼───────────┤  (community images)
            │         │          │          │           │
ETH Zürich ─┼─────────┼──────────┼──────────┼─────────⚫─┤  (mini-Internet!)
            │         │          │          │           │
Michigan ───┼─────────┼────⚫─────┼──────────┼───────────┤  (Mininet focus)
            │         │          │          │           │
CMU ────────┼─────────┼──────────┼──────────┼────⚫──────┤  (official Dockerfiles)
            │         │          │          │           │
Berkeley ───┼─────────┼────⚫─────┼──────────┼───────────┤  (limited)
            │         │          │          │           │
CLIM&TOMA ──┼─────────┼──────────┼──────────┼────⚫──────┤  (per-week compose)
            │         │          │          │           │
Labtainers ─┼─────────┼──────────┼──────────┼─────────⚫─┤  (50+ lab containers)
            │         │          │          │           │
```

**ETH Zürich mini-Internet** merită mențiune specială:
- Fiecare grup de studenți operează un Sistem Autonom (AS)
- FRRouting pentru BGP/OSPF real
- Suport MPLS și RPKI
- 219 ⭐ pe GitHub

**Proiectul CLIM&TOMA** oferă:
- `docker-compose.yml` standardizat per săptămână
- Portainer (port 9000) pentru management vizual
- Scheme IP consistente (172.20.X.0/24)
- Scripturi `start_lab.py` / `stop_lab.py` / `cleanup.py`

### 3.5. Dimensiunea C5: Documentație

| Element | Stanford | Berkeley | Michigan | UCLouvain | CLIM&TOMA |
|:--------|:--------:|:--------:|:--------:|:---------:|:---------:|
| README comprehensiv | ✅ | ✅ | ✅ | ✅ | ✅ |
| Troubleshooting Guide | ⚠️ | ⚠️ | ⚠️ | ✅ | ✅ |
| Commands Cheatsheet | ❌ | ❌ | ❌ | ❌ | ✅ |
| Glossar termeni | ❌ | ✅* | ❌ | ✅* | ✅ |
| Ghid instructor | ❌ | ❌ | ❌ | ✅ | ✅ |
| Further Reading | ⚠️ | ✅ | ⚠️ | ✅ | ✅ |

*\* În cadrul textbook-ului*

**Berkeley CS168** câștigă la capitolul **manual deschis** — un textbook complet disponibil gratuit sub CC BY-SA 4.0 la `textbook.cs168.io`. Acesta este probabil cea mai valoroasă resursă de networking open-source pentru auto-didacți.

### 3.6. Dimensiunea C6: Proiecte

```
Numărul și Tipul Proiectelor

CLIM&TOMA/ASE-CSIE  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  15+ proiecte grup
                    ▒▒▒▒▒▒▒▒▒▒                        + 5 rezervă individ.

Labtainers (NPS)    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  50+ labs
                    (modulare, focus security)

Stanford CS144      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                  8 checkpoints
                    (progressive TCP/IP stack)

KAIST KENSv3        ▓▓▓▓▓▓▓▓                          4 proiecte TCP
                    (implementare completă)

Michigan EECS 489   ▓▓▓▓▓▓▓▓                          4 assignments
                    (sockets → datacenter)

CMU 15-441          ▓▓▓▓▓▓                            3 proiecte mari
                    (multi-week each)
```

**Stanford CS144** câștigă la coerența narativă — cele 8 checkpoint-uri construiesc incremental un stack TCP/IP complet, culminând cu conectivitate end-to-end reală prin servere relay.

**Proiectul CLIM&TOMA** pune accent pe varietate și lucrul în echipă (SDN, microservicii, IDS/IPS, IoT, etc.).

### 3.7. Dimensiunea C7: Elemente Interactive

Aceasta este probabil cea mai clară diferențiere:

```
┌─────────────────────────────────────────────────────────────────────┐
│              PREZENTĂRI INTERACTIVE HTML/CSS/JS                      │
│                                                                      │
│    ┌─────────────────────────────────────────────────────────┐      │
│    │                                                         │      │
│    │   ╔═══════════════════════════════════════════════╗     │      │
│    │   ║  Progress Bar  ████████████░░░░░  Slide 7/14  ║     │      │
│    │   ╠═══════════════════════════════════════════════╣     │      │
│    │   ║                                               ║     │      │
│    │   ║    Week 3: TCP Tunneling                      ║     │      │
│    │   ║                                               ║     │      │
│    │   ║    [Interactive Diagram]  [Quiz Button]       ║     │      │
│    │   ║                                               ║     │      │
│    │   ║    ◄ Prev    [ToC]    [⛶ Fullscreen]   Next ► ║     │      │
│    │   ╚═══════════════════════════════════════════════╝     │      │
│    │                                                         │      │
│    │   Features: copy-to-clipboard, keyboard nav,            │      │
│    │   reveal animations, responsive design                  │      │
│    │                                                         │      │
│    └─────────────────────────────────────────────────────────┘      │
│                                                                      │
│    Cursuri care oferă acest lucru:  CLIM&TOMA/ASE-CSIE              │
│    Cursuri care NU oferă:           Toate celelalte analizate       │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

> *Nu e o glumă*: Am căutat în peste 20 de repository-uri și site-uri de curs. PDF-uri, PowerPoint-uri, Google Slides, înregistrări video — dar prezentări HTML interactive cu quiz-uri, animații și navigare keyboard? Zero.

---

## 4. Studii de Caz: Ce Fac Bine Ceilalți

Pentru a nu părea că doar ne lăudăm, iată ce am învățat de la alții:

### 4.1. Stanford CS144: Maestrul Implementării

**Ce fac excelent:**
- Progresia pedagogică perfectă: de la ByteStream → TCPReceiver → TCPSender → Router
- Teste automate cu `make check_labN`
- Documentație de înaltă calitate pentru fiecare lab
- Video lectures disponibile public

**Ce le lipsește:**
- Infrastructură Docker oficială (doar imagini comunitare)
- Metodologie pedagogică explicită
- Proiecte de grup

**Lecție învățată**: Coerența narativă în proiecte contează enorm.

### 4.2. ETH Zürich: Regele Infrastructurii

**Ce fac excelent:**
- mini-Internet project: simulare la scară Internet
- Docker orchestration profesional
- Studenții operează Sisteme Autonome reale
- RPKI, MPLS, BGP — tehnologii actuale

**Ce le lipsește:**
- Materialele pedagogice explicite
- Prezentări interactive
- Varietate în tipuri de proiecte

**Lecție învățată**: Scala contează — a opera un AS e diferit de a scrie un socket client.

### 4.3. Berkeley CS168: Textbook-ul Deschis

**Ce fac excelent:**
- Textbook gratuit, profesional editat, CC BY-SA 4.0
- 17 săptămâni de conținut
- Acoperire modernă (datacenter networking, ML collective ops)
- Glosar comprehensiv

**Ce le lipsește:**
- Infrastructură de laborator
- Exerciții practice cu cod
- Prezentări interactive

**Lecție învățată**: Un textbook bun valorează cât o mie de slide-uri PowerPoint.

### 4.4. KAIST KENSv3: Framework-ul Educațional

**Ce fac excelent:**
- Framework custom pentru implementare TCP
- PCAP logging pentru debugging cu Wireshark
- Binare de referință pentru testare incrementală
- API compatibil POSIX

**Ce le lipsește:**
- Documentație pedagogică
- Varietate tematică
- Prezentări interactive

**Lecție învățată**: Un framework educațional dedicat poate fi mai valoros decât tooling-ul industrial.

---

## 5. Sinteza Concluziilor

### 5.1. Matricea Finală de Evaluare

<table>
<thead>
<tr style="background: #1a237e; color: white;">
<th>Curs</th>
<th>C1<br/>Compr.</th>
<th>C2<br/>Cod</th>
<th>C3<br/>Pedag.</th>
<th>C4<br/>Docker</th>
<th>C5<br/>Docs</th>
<th>C6<br/>Proj.</th>
<th>C7<br/>Interact.</th>
<th>TOTAL</th>
</tr>
</thead>
<tbody>
<tr style="background: #c8e6c9; font-weight: bold;">
<td>CLIM&TOMA/ASE-CSIE</td>
<td>8</td>
<td>7</td>
<td>10</td>
<td>8</td>
<td>9</td>
<td>9</td>
<td>10</td>
<td>61/70</td>
</tr>
<tr>
<td>Stanford CS144</td>
<td>7</td>
<td>10</td>
<td>4</td>
<td>5</td>
<td>8</td>
<td>9</td>
<td>2</td>
<td>45/70</td>
</tr>
<tr style="background: #f5f5f5;">
<td>ETH Zürich</td>
<td>9</td>
<td>7</td>
<td>3</td>
<td>10</td>
<td>7</td>
<td>6</td>
<td>2</td>
<td>44/70</td>
</tr>
<tr>
<td>Berkeley CS168</td>
<td>10</td>
<td>5</td>
<td>3</td>
<td>4</td>
<td>10</td>
<td>5</td>
<td>3</td>
<td>40/70</td>
</tr>
<tr style="background: #f5f5f5;">
<td>Michigan EECS 489</td>
<td>8</td>
<td>8</td>
<td>4</td>
<td>5</td>
<td>8</td>
<td>7</td>
<td>2</td>
<td>42/70</td>
</tr>
<tr>
<td>CMU 15-441</td>
<td>8</td>
<td>8</td>
<td>2</td>
<td>8</td>
<td>6</td>
<td>7</td>
<td>2</td>
<td>41/70</td>
</tr>
<tr style="background: #f5f5f5;">
<td>KAIST KENSv3</td>
<td>9</td>
<td>6</td>
<td>6</td>
<td>8</td>
<td>5</td>
<td>6</td>
<td>2</td>
<td>42/70</td>
</tr>
<tr>
<td>Labtainers (NPS)</td>
<td>7</td>
<td>5</td>
<td>7</td>
<td>10</td>
<td>8</td>
<td>10</td>
<td>2</td>
<td>49/70</td>
</tr>
</tbody>
</table>

*Scor 1-10 per dimensiune, evaluat subiectiv de autori (cu toate bias-urile aferente)*

### 5.2. Concluzii Principale

1. **Golul Pedagogic**: Metodele de predare bazate pe evidență (peer instruction, misconceptions, Parsons problems) sunt practic absente din curricula universitară de elită disponibilă public. Aceasta este oportunitatea principală pe care proiectul CLIM&TOMA încearcă să o exploateze.

2. **Fragmentarea Excelenței**: Niciun curs nu excelează la toate dimensiunile. Stanford domină la implementare, ETH la infrastructură, Berkeley la documentație, KAIST la framework educațional. Proiectul nostru încearcă să integreze punctele forte din fiecare.

3. **Absența Prezentărilor Interactive**: Cu excepția proiectului de referință, toate cursurile analizate folosesc formate statice (PDF, PPT, video). Aceasta este o nișă neexplorată surprinzător de mare.

4. **Docker ca Standard Emergent**: Containerizarea devine norma, dar implementarea variază enorm — de la imagini comunitare (Stanford) la orchestrații sofisticate (ETH, Labtainers).

### 5.3. Limitări ale Acestei Analize

- **Bias al autorilor**: Evident, ne evaluăm propriul proiect.
- **Materialele private**: Multe universități nu publică toate materialele; am analizat doar ce e disponibil public.
- **Snapshot temporal**: Curricula evoluează; analiza reflectă starea din ianuarie 2025.
- **Subiectivitate în scoruri**: Ponderile și scorurile reflectă prioritățile noastre.

---

## 6. Recomandări și Direcții Viitoare

### 6.1. Ce Am Învățat pentru Proiectul CLIM&TOMA

| De la | Să adoptăm |
|:------|:-----------|
| Stanford | Coerența narativă în proiecte; C++ coding standards |
| ETH Zürich | Scala infrastructurii (mini-Internet) |
| Berkeley | Open textbook ca resursă paralelă |
| KAIST | Framework educațional dedicat |
| Labtainers | Parametrizare per-student |

### 6.2. Roadmap Propus

```
2025 Q1  ─────► Integrare linting automat (flake8, mypy strict)
              │
2025 Q2  ─────► Traducere materiale RO ↔ EN completă
              │
2025 Q3  ─────► Mini-proiect SDN la scară (inspirat ETH)
              │
2025 Q4  ─────► Open textbook companion (inspirat Berkeley)
              │
2026+    ─────► Framework KENS-style pentru TCP implementation
```

---

## 7. Mulțumiri

Acest proiect nu ar fi existat fără:

- **conf. dr. Andrei TOMA** — pentru ideile inițiale, scripturile de bază, și nesfârșitele discuții la The Dose care au transformat concepte vagi în arhitectură concretă
- **The Dose, București** — pentru cafeaua care a alimentat acest proiect (literal)
- **Comunitatea Open Source** — pentru toate resursele pe care le-am studiat și din care am învățat
- **Studenții ASE-CSIE** — pentru răbdarea de a fi cobai pentru versiunile timpurii

---

## Referințe și Resurse

### Cursuri Analizate (în ordinea citării)

| # | Universitate | Curs | URL |
|:-:|:-------------|:-----|:----|
| 1 | Stanford | CS144 | `cs144.github.io` / `github.com/CS144` |
| 2 | ETH Zürich | 227-0120-00L | `comm-net.ethz.ch` |
| 3 | U. Michigan | EECS 489 | `github.com/mosharaf/eecs489` |
| 4 | CMU | 15-441/641 | `computer-networks.github.io` |
| 5 | UC Berkeley | CS168 | `textbook.cs168.io` |
| 6 | Princeton | COS 461 | `cs.princeton.edu/courses/archive/fall21/cos461` |
| 7 | KAIST | CS341 | `anlab-kaist.github.io/KENSv3` |
| 8 | UCLouvain | CNP3 | `inl.info.ucl.ac.be/CNP3` |
| 9 | NPS | Labtainers | `nps.edu/web/c3o/labtainers` |
| 10 | Johns Hopkins | EN.601.414 | `github.com/xinjin/course-net` |
| 11 | CUHK | CSCI 4430 | `github.com/henryhxu/CSCI4430` |

### Metodologie Pedagogică

- Brown, N. C. C. & Wilson, G. (2018). *Ten Quick Tips for Teaching Programming*
- Mazur, E. (1997). *Peer Instruction: A User's Manual*
- Parsons, D. & Haden, P. (2006). *Parson's Programming Puzzles*

---

<div align="center">

**CLIM&TOMA/ASE-CSIE Networking Project**  
*Academia de Studii Economice București*  
*Facultatea de Cibernetică, Statistică și Informatică Economică*

---

*Ultima actualizare: Ianuarie 2025*  
*Versiune document: 1.0*

</div>
