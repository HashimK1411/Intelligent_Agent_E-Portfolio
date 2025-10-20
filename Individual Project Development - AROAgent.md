# Academic Research Online Agent (AROAgent)

**Domain:** Academic Research  
**Type:** Multi‑agent pipeline — Discovery → Fetch/Retry → Extract/Normalise → Store/Present  


---

## 1) Overview

AROAgent aggregates scholarly metadata from **Crossref** and **DOAJ**, normalises heterogeneous records into a unified schema, **deduplicates** results, and outputs **JSON/CSV**. It includes a minimal Flask UI and a CLI. Design choices emphasise **API‑first**, **modular**, and **testable** components.

**Success criteria (from brief):**
1. Identify & retrieve data ✔  
2. Process data (normalise + deduplicate [+ optional facets/ranking]) ✔  
3. Store/present results (JSON/CSV + UI) ✔

---

## 2) Features

- **Discovery** — URL‑safe planning of Crossref/DOAJ API endpoints (≤25 results).  
- **Resilient fetch** — HTTPS, explicit timeouts, **exponential backoff**.  
- **Extraction/Normalisation** — Per‑source mappers → unified `Record` schema.  
- **Processing** — Dedup by **DOI → URL → Title** (lowercased). Optional: year facets & simple ranking.  
- **Storage/Presentation** — `results.json` (+ optional `results.csv`), Flask UI, CLI.  
- **Fixtures** — Offline JSON samples for reproducible demos/tests.

---

## 3) Architecture

```
Query
  → DiscoveryAgent (plan API URLs: Crossref, DOAJ)
  → FetchAgent + RetrySession (HTTPS, timeout, exponential backoff)
  → ExtractAgent (normalise to Record schema)
  → StorageAgent (dedup; export JSON/CSV)
  → Presentation (Flask UI + CLI)
```
**Unified `Record` schema:** `id, title, authors[], year, venue, source, license, url`

**Normalisation rules:**  
- Title: arrays → take the first entry  
- Year: Crossref `issued.date-parts[0][0]` (fallback `0`)  
- Authors: “Given Family” format

---

## 4) Installation

```bash
# Create & activate a virtual environment
python -m venv .venv
# Windows
.\.venv\Scriptsctivate
# macOS/Linux
source .venv/bin/activate

# Install runtime deps
pip install -r requirements.txt

# (Optional) Dev/test tools
pip install -r requirements-dev.txt
```

---

## 5) Usage

### A) Flask UI (online or fixtures)
```bash
python server.py
# open http://localhost:8000
```
- Enter a query (e.g., "intelligent agents").  
- Select **Crossref**, **DOAJ**, or both.  
- (Optional) Enable **Use Offline Fixtures** for a network‑free demo.

### B) CLI (online)
```bash
python -m aroagent.cli --query "intelligent agents" --sources crossref,doaj   --out-json results.json --out-csv results.csv
```

### C) CLI (offline fixtures)
```bash
python -m aroagent.cli --offline fixtures/crossref_sample.json fixtures/doaj_sample.json   --out-json results.json --out-csv results.csv
```

**Outputs:** `results.json` (UTF‑8, pretty) and optional `results.csv` (fixed headers).

---

## 6) Processing Details

### Deduplication (in `storage.py`)
- **Key order:** `id → url → title` (lowercased/stripped).  
- **Policy:** *last write wins* (newer record overwrites older).  
- **Rationale:** DOI is the strongest persistent identifier; URL next; title last.

### (Optional) Post‑processing (`processing.py`)
- **Year facets:** counts per year (ignore `0`).  
- **Simple ranking:** token match across title/venue/authors → score; sort by score desc, then year desc.

---

## 7) Error Handling & Retry
- HTTPS connections with explicit **timeouts**.  
- **Exponential backoff** between attempts (bounded retries).  
- Treat **2xx** responses as success; log/retry non‑2xx.

> Key decision comments are present in `retry.py` and `storage.py` to explain *why*.

---

## 8) Design → Implementation (traceability to Unit 6)
| Design (Unit 6) | Implementation (Unit 11) | Evidence |
|---|---|---|
| Discovery | `DiscoveryAgent.plan()` builds Crossref/DOAJ URLs | `01_discovery_plan.png` |
| Fetch/Resilience | `FetchAgent` + `RetrySession` (timeouts, backoff) | `10_retry_demo.png` |
| Extract/Normalise | `ExtractAgent` → `Record` schema | `08_results_mapped_fields.png` |
| Processing | `StorageAgent` dedup (+ optional facets/ranking) | `results.json`, `12_facets_json.png` |
| Store/Present | JSON/CSV + Flask UI/CLI | `03_outputs_folder.png`, `07_flask_ui_online.png` |

---
