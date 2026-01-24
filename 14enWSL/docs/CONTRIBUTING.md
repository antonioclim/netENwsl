# 🤝 Contributing to Week 14 Lab Kit

> NETWORKING class — ASE, CSIE | Computer Networks Laboratory  
> by ing. dr. Antonio Clim

Mulțumim pentru interesul de a contribui la acest proiect educațional! Acest ghid descrie procesul și standardele pentru contribuții.

---

## 📋 Cuprins

1. [Cod de Conduită](#cod-de-conduită)
2. [Cum Pot Contribui](#cum-pot-contribui)
3. [Configurare Mediu de Dezvoltare](#configurare-mediu-de-dezvoltare)
4. [Standarde de Cod](#standarde-de-cod)
5. [Proces de Submisie](#proces-de-submisie)
6. [Structura Proiectului](#structura-proiectului)

---

## 📜 Cod de Conduită

### Principii

- **Respect** — Tratează toți colaboratorii cu respect
- **Constructivism** — Feedback-ul trebuie să fie constructiv și util
- **Includere** — Proiectul este deschis tuturor, indiferent de nivel
- **Educație** — Scopul principal este învățarea, nu perfecțiunea

### Comportament Inacceptabil

- Limbaj ofensator sau discriminatoriu
- Hărțuire de orice tip
- Publicarea informațiilor private ale altora
- Spam sau auto-promovare excesivă

---

## 🎯 Cum Pot Contribui

### Pentru Studenți

| Tip Contribuție | Descriere | Dificultate |
|-----------------|-----------|-------------|
| 🐛 Bug Reports | Raportează erori găsite | ⭐ Ușor |
| 📝 Documentație | Îmbunătățește README, adaugă exemple | ⭐ Ușor |
| 🧪 Teste | Adaugă teste pentru funcții existente | ⭐⭐ Mediu |
| ✨ Features | Propune și implementează funcții noi | ⭐⭐⭐ Avansat |

### Pentru Asistenți

- Revizuire Pull Requests
- Mentoring studenți contribuitori
- Actualizare materiale pentru noua sesiune
- Traducere documentație

### Pentru Instructori

- Validare conținut pedagogic
- Propunere exerciții noi
- Aliniere cu curriculum

---

## 🛠️ Configurare Mediu de Dezvoltare

### Cerințe

- Python 3.10+
- Docker & Docker Compose
- Git
- WSL2 (pe Windows)

### Pași Inițiali

```bash
# 1. Clone repository
git clone https://github.com/antonioclim/netENwsl.git
cd netENwsl/14enWSL

# 2. Creează virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/WSL
# sau: .venv\Scripts\activate  # Windows

# 3. Instalează dependențe
pip install -r setup/requirements.txt
pip install -e ".[dev]"  # Include dev dependencies

# 4. Instalează pre-commit hooks
pip install pre-commit
pre-commit install

# 5. Verifică setup
make validate
make test
```

### Verificare Rapidă

```bash
# Rulează toate verificările
make ci

# Sau individual:
make lint      # Verifică stilul codului
make test      # Rulează teste
make validate  # Validează structura kit-ului
```

---

## 📏 Standarde de Cod

### Python

Folosim **Ruff** pentru linting și formatting:

```bash
# Check style
ruff check src/ scripts/ tests/ formative/

# Auto-fix issues
ruff check --fix src/ scripts/ tests/ formative/

# Format code
ruff format src/ scripts/ tests/ formative/
```

### Reguli Obligatorii

1. **Type Hints** — Toate funcțiile publice trebuie să aibă type hints

```python
# ✅ Corect
def check_port(host: str, port: int, timeout: float = 5.0) -> bool:
    """Check if a port is open."""
    ...

# ❌ Greșit
def check_port(host, port, timeout=5.0):
    ...
```

2. **Docstrings** — Stil Google pentru toate modulele și funcțiile publice

```python
def send_request(url: str, method: str = "GET") -> Response:
    """Send HTTP request to specified URL.
    
    Args:
        url: Target URL for the request.
        method: HTTP method to use. Defaults to "GET".
        
    Returns:
        Response object containing status and body.
        
    Raises:
        ConnectionError: If connection cannot be established.
        
    Example:
        >>> response = send_request("http://localhost:8080/health")
        >>> print(response.status_code)
        200
    """
    ...
```

3. **Prediction Prompts** — Pentru exerciții și documentație

```python
# 💭 PREDICTION: Ce va afișa acest cod?
#    a) "Connected"
#    b) "Connection refused"
#    c) TimeoutError

result = check_connection("localhost", 8080)
print(result)

# ═══════════════════════════════════════════════════════════════
# Scroll pentru răspuns...
#
# Răspuns: a) "Connected" — dacă serviciul rulează pe port 8080
# ═══════════════════════════════════════════════════════════════
```

### Docker

- Folosește multi-stage builds când e posibil
- Evită `latest` tag — specifică versiuni exacte
- Nu rula containere ca root în producție
- Include health checks

### Documentație

- Markdown pentru toate documentele
- Include exemple practice
- Actualizează CHANGELOG.md pentru orice modificare
- Păstrează consistența cu stilul existent

---

## 📬 Proces de Submisie

### 1. Creează Issue (Opțional dar Recomandat)

Înainte de a începe lucrul pe o funcționalitate majoră:

```markdown
## Descriere
Ce dorești să adaugi/modifici

## Motivație
De ce este necesar

## Propunere Implementare
Cum plănuiești să implementezi
```

### 2. Fork și Branch

```bash
# Fork pe GitHub, apoi:
git clone https://github.com/YOUR_USERNAME/netENwsl.git
cd netENwsl/14enWSL

# Creează branch pentru feature
git checkout -b feature/add-new-exercise

# Sau pentru bugfix
git checkout -b fix/quiz-scoring-bug
```

### 3. Convenții Commit Messages

Format: `type(scope): description`

| Type | Folosire |
|------|----------|
| `feat` | Funcționalitate nouă |
| `fix` | Bug fix |
| `docs` | Documentație |
| `style` | Formatare (fără schimbare logică) |
| `refactor` | Refactorizare cod |
| `test` | Adăugare/modificare teste |
| `chore` | Mentenanță (deps, config) |

Exemple:
```
feat(quiz): add LO5 questions for verification strategies
fix(docker): correct network subnet overlap
docs(readme): update installation steps for Windows
test(smoke): add backend failover test
```

### 4. Pre-Push Checklist

```bash
# Verificări obligatorii înainte de push
make lint       # ✓ Fără erori de stil
make test       # ✓ Toate testele trec
make validate   # ✓ Kit valid

# Verificare opțională
make quiz       # Testează quiz-ul manual
```

### 5. Pull Request

Template PR:

```markdown
## Descriere
[Descriere clară a modificărilor]

## Tip Modificare
- [ ] Bug fix
- [ ] Funcționalitate nouă
- [ ] Documentație
- [ ] Refactorizare
- [ ] Alte (specifică)

## Checklist
- [ ] Am rulat `make ci` și toate verificările trec
- [ ] Am actualizat documentația relevantă
- [ ] Am adăugat teste pentru noile funcționalități
- [ ] Commit messages urmează convenția

## Screenshots (dacă e cazul)
[Adaugă screenshots pentru modificări UI]

## Notă pentru Reviewer
[Informații suplimentare pentru reviewer]
```

### 6. Review Process

1. **Automated Checks** — CI trebuie să treacă
2. **Code Review** — Minim 1 approve de la maintainer
3. **Educational Review** — Pentru conținut pedagogic, verificare de instructor
4. **Merge** — Squash merge în main

---

## 📁 Structura Proiectului

```
14enWSL/
├── 📄 README.md              # Documentație principală
├── 📄 CHANGELOG.md           # Istoric modificări
├── 📄 SECURITY.md            # Politică securitate
├── 📄 LICENSE                # Licență MIT
├── 📄 Makefile               # Comenzi orchestrator
├── 📄 pyproject.toml         # Configurare Python
├── 📄 ruff.toml              # Configurare linter
│
├── 📁 docker/                # Configurare Docker
│   ├── docker-compose.yml    # Definire servicii
│   └── Dockerfile            # Imagine container
│
├── 📁 docs/                  # Documentație extinsă
│   ├── theory_summary.md     # Teorie
│   ├── misconceptions.md     # Concepții greșite
│   ├── troubleshooting.md    # Depanare
│   ├── learning_objectives.md # Matrice LO
│   └── ...
│
├── 📁 formative/             # Evaluare formativă
│   ├── quiz_week14.yaml      # Quiz YAML
│   ├── quiz_week14.json      # Quiz JSON (Moodle)
│   └── run_quiz.py           # Runner interactiv
│
├── 📁 src/                   # Cod sursă
│   ├── apps/                 # Aplicații server
│   ├── exercises/            # Exerciții lab
│   └── utils/                # Utilități comune
│
├── 📁 homework/              # Teme pentru acasă
│   └── exercises/            # Template-uri teme
│
├── 📁 tests/                 # Teste automate
│   ├── smoke_test.py         # Smoke tests
│   ├── test_exercises.py     # Teste exerciții
│   └── expected_outputs.md   # Output-uri așteptate
│
├── 📁 scripts/               # Scripturi utilitar
│   ├── start_lab.py          # Pornire lab
│   ├── stop_lab.py           # Oprire lab
│   └── capture_traffic.py    # Captură trafic
│
└── 📁 setup/                 # Configurare
    ├── requirements.txt      # Dependențe Python
    └── verify_environment.py # Verificare mediu
```

---

## ❓ Întrebări Frecvente

### Q: Pot contribui dacă sunt începător?

**Da!** Contribuțiile de documentație și raportarea bug-urilor sunt perfecte pentru începători.

### Q: Cât de mare trebuie să fie o contribuție?

Orice contribuție e binevenită, de la corectarea unei greșeli de tipar până la funcționalități noi.

### Q: Ce se întâmplă dacă PR-ul meu nu e acceptat?

Vei primi feedback constructiv despre ce trebuie îmbunătățit. Nu te descuraja!

### Q: Cum pot contacta maintainerii?

- **Issues: Open an issue on GitHub
- **GitHub Issues:** Pentru discuții publice
- **Office Hours:** Vezi pagina cursului

---

## 🏆 Recunoaștere

Contribuitorii sunt recunoscuți în:

- `CONTRIBUTORS.md` — Lista tuturor contribuitorilor
- Release notes — Menționare în changelog
- Pagina cursului — Studenți exemplari

---

*Mulțumim că contribui la educația în rețelistică!* 🌐

*NETWORKING class — ASE, CSIE | Computer Networks Laboratory*
