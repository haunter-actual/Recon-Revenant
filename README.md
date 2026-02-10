# Recon Revenant

Privacy-safe, offline reconnaissance and post-enumeration reasoning tool  
for **Linux and Windows** penetration-testing labs.

Designed for **OSCP / PNPT / CRTO-style learning**.

---

# Core Philosophy

Recon Revenant trains **human reasoning**, not automation.

- Deterministic baseline reasoning
- Optional **local-only AI explanation layer**
- Strict privacy guarantees
- No exploit or payload generation

---

# Features

## Deterministic Engine
- Parses Nmap, LinPEAS, WinPEAS outputs
- Extracts **high-signal escalation indicators**
- Produces:
  - attack chain
  - missed enumeration hints
  - Mermaid diagram
  - exam takeaways

Works **fully offline** with **no AI required**.

---

## Local AI Reasoning (Optional)

AI is:

- **disabled by default**
- **local-model only** (e.g., Ollama)
- fed **sanitized abstract signals only**
- prevented from producing:
  - commands
  - exploits
  - payloads
  - sensitive data

### Enable AI

```bash
recon-revenant --nmap nmap.txt --enum linpeas.txt --ai
```

### Specify Model

```bash
recon-revenant --ai --model llama3
```

### Timeout control:
```bash
recon-revenant --ai-timeout 15
```

### Privacy Controls

* Privacy Guarantees
* No network communication
* No telemetry or analytics
* No cloud APIs
* Raw enumeration data never leaves memory
* AI sees signals only, never real data

Safe for:
* proprietary labs
* client engagements
* air-gapped systems

## Installation

```bash
pipx install git+https://github.com/haunter-actual/recon-revenant.git
```

## Usage

```bash
recon-revenant --nmap nmap.txt --enum linpeas.txt
```

## Usage

### Linux Target:

```bash
recon-revenant --nmap nmap.txt --enum linpeas.txt
```

### Windows Target:

```bash
recon-revenant --nmap nmap.txt --enum winpeas.txt

```

## Versioning
* v0.2.0 — deterministic reasoning engine
* v0.3.0 — optional privacy-safe local AI reasoning

