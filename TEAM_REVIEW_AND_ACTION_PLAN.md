# KhojDoot Team Review & Action Plan (Oct 4 – Oct 8)

**Target Hackathon Demo:** October 9–10, 2026  
**Document Purpose:** Code audit against PRD/TRD specifications, contract reconciliation, beginner mistake prevention, and 5-day team execution checklist.

---

## 1. Executive Summary & Team Code Audit

This review analyzes the current branch contributions (`origin/abhishek`, `origin/Shantanu(Database)`, `origin/gayatri-deore`, `origin/sakshikhule`) against the **PRD v1.0** and **TRD v1.0** specifications.

### Summary Matrix

| Team Member | Domain / TRD Role | GitHub Status | Major Strength | Critical Fix Required Before Merge |
|---|---|---|---|---|
| **Abhishek** | FastAPI Backend & Webhook | Contributed | Clean FastAPI routing & structure | Align `POST /ingest` with Gayatri's form & Shantanu's DB schema |
| **Shantanu** | Database & Persistence | Contributed | Indexed SQLite schema design | Reconcile `shops` & `bins` table columns with Abhishek |
| **Gayatri** | Web UI & Frontend | Contributed | Client-side photo compression & 3-step UX | Parameterize `API_BASE` URL and support multi-part form contract |
| **Paksha** | AI Processing (Sarvam/Jev/Gemini) | **NO COMMITS FLAGGED** | N/A | Must build TRD AI services (`sarvam.py`, `gemini.py`) |
| **Sakshi** | QA & Multilingual Testing | Contributed | High-quality 10 SME seed records | Expand test matrix across Marathi voice notes & edge cases |

---

## 2. Universal Beginner Mistakes & Post-Mortem Guidelines

Every team member must read these rules derived from our technical post-mortem:

> [!IMPORTANT]
> 1. **Do Not Run Servers in Ephemeral AI Background Runners:**  
>    Always run `uvicorn app.main:app --reload` directly in your native terminal (`powershell`). Background AI runner tasks get recycled and break Meta Webhook URLs.
> 2. **Fix Windows Unicode Encoding Errors:**  
>    Windows terminals default to `cp1252` encoding. When logging Marathi Devanagari text (`नमस्कार`, `टिफिन`), Python will crash with `UnicodeEncodeError`. Ensure `sys.stdout.reconfigure(encoding="utf-8")` is included at app startup.
> 3. **Never Swallow Exceptions Silently:**  
>    Avoid empty `try: ... except: pass` blocks. Always log errors explicitly so bugs are caught immediately during testing.
> 4. **No Hardcoded Base URLs:**  
>    Replace hardcoded `http://localhost:8000` strings with configurable environment variables or relative paths.

---

## 3. Detailed Member Analysis & Learning Strategy

### 3.1 Abhishek — FastAPI & Backend Runtime

#### Current Code vs TRD Audit
- **Good:** Abhishek built clean FastAPI endpoints (`POST /smes`, `POST /ingest`, `GET /b/{slug}.json`).
- **Conflict:** Abhishek's `/ingest` endpoint expects a 2-step flow (create shop via `/smes` first, then upload photos via `/ingest`). Gayatri's frontend sends everything in a single request.
- **Contract Fix:** Update `/ingest` to auto-create the shop if `name`, `phone`, and `city` are provided in the `FormData`.

#### 3-Tier Skill Strategy (2 Hours/Day)
* **Must Learn Manually (Do NOT rely on AI):**
  - FastAPI Request Lifecycle: How `Form()`, `File()`, and `Header()` params parse incoming HTTP bodies.
  - Python `async/await` syntax and background tasks (`BackgroundTasks`).
* **Learn Enough to Understand:**
  - Meta Cloud API HTTP payload formats and webhook challenge handshakes.
  - Pydantic schema validation errors (`422 Unprocessable Entity`).
* **Delegate to AI:**
  - Writing boilerplate CRUD SQL queries and Pydantic model definitions.

#### Daily Checklist (Oct 4 – Oct 8)
- [ ] **Oct 4:** Reconcile `/ingest` route to accept `name`, `phone`, `city`, `slug`, and `photos` in one request.
- [ ] **Oct 5:** Connect Shantanu's database helper functions into `main.py`.
- [ ] **Oct 6:** Integrate Paksha's Gemini & Sarvam AI extractors into the backend processing flow.
- [ ] **Oct 7:** Build Meta WhatsApp Webhook endpoint (`GET` handshake + `POST` inbound receiver).
- [ ] **Oct 8:** End-to-end testing with Sakshi; verify P0 backend runtime stability.

---

### 3.2 Shantanu — Database & InfoBin Persistence

#### Current Code vs TRD Audit
- **Good:** Shantanu defined `schema.sql` with indexed tables (`shops`, `bins`, `photos`).
- **Conflict:** `shops` table is missing `sme_id` in Abhishek's backend code. `bins` table in `schema.sql` uses `bin_type` for multi-row bins, whereas Abhishek's backend stores a single JSON blob (`UNIQUE(shop_id)`).
- **Contract Fix:** Unify `bins` schema to support both single-blob InfoBin storage (`data`) and `bin_type` indexing.

#### 3-Tier Skill Strategy (2 Hours/Day)
* **Must Learn Manually (Do NOT rely on AI):**
  - SQLite foreign key constraints (`FOREIGN KEY (shop_id) REFERENCES shops(id)`).
  - Basic SQL indexing (`CREATE INDEX idx_shops_slug ON shops(slug)`).
* **Learn Enough to Understand:**
  - SQLite JSON functions (`json_extract()`) and JSON column storage.
  - Context managers for database connections (`with sqlite3.connect(...) as conn:`).
* **Delegate to AI:**
  - Writing complex multi-join SQL queries or schema migration scripts.

#### Daily Checklist (Oct 4 – Oct 8)
- [ ] **Oct 4:** Merge `schema.sql` with Abhishek's backend database initialization script (`connection.py`).
- [ ] **Oct 5:** Build `save_infobin()` and `get_infobin()` Python helper functions.
- [ ] **Oct 6:** Implement `provenance` table to track extraction channels (`WhatsApp`, `Web`, `Voice`).
- [ ] **Oct 7:** Populate SQLite database with Sakshi's 10 SME seed profiles from `shops.json`.
- [ ] **Oct 8:** Run load/query benchmark tests to ensure instant $O(1)$ slug lookups.

---

### 3.3 Gayatri — Frontend & Web Interface

#### Current Code vs TRD Audit
- **Good:** Gayatri created a high-quality 3-step onboarding UI (`Add Your Shop.html`) with client-side canvas photo compression and `?demo=1` mode.
- **Conflict:** Hardcoded `API_BASE = "http://localhost:8000"`. Needs dynamic fallback when hosted on public domains.
- **Contract Fix:** Update JS submit logic to handle response JSON structure cleanly and parameterize `API_BASE`.

#### 3-Tier Skill Strategy (2 Hours/Day)
* **Must Learn Manually (Do NOT rely on AI):**
  - Native JavaScript `fetch()` API and `FormData` construction.
  - DOM Event Listeners (`addEventListener`) and step navigation state management.
* **Learn Enough to Understand:**
  - HTML5 Canvas image resizing (`createImageBitmap`) and Blob creation.
  - CORS (Cross-Origin Resource Sharing) headers and how browsers enforce them.
* **Delegate to AI:**
  - Writing CSS animations, layout styling, and HTML layout scaffolding.

#### Daily Checklist (Oct 4 – Oct 8)
- [ ] **Oct 4:** Parameterize `API_BASE` in `Add Your Shop.html` to support window location origins.
- [ ] **Oct 5:** Connect web form submission to Abhishek's updated `/ingest` API endpoint.
- [ ] **Oct 6:** Build the dynamic Khoj Card HTML template (`/b/{slug}`) displaying approved merchant facts.
- [ ] **Oct 7:** Build KhojDoot Labs telemetry view (`/labs`) showing live 6-stage pipeline status.
- [ ] **Oct 8:** Verify mobile responsiveness across phone browsers for the demo.

---

### 3.4 Paksha — AI Processing & Speech Extraction (FLAGGED)

> [!WARNING]
> **Action Required:** Paksha currently has **zero commits** on GitHub. As per TRD Section 7, Paksha must take ownership of the AI processing pipeline immediately.

#### Tasks to Claim from TRD
- **Sarvam Saaras ASR (`app/ai/sarvam.py`):** Transcribe Marathi `.ogg` voice notes.
- **Gemini 3.6 Flash (`app/ai/gemini.py`):** Extract structured business facts into InfoBin schema.
- **Jev Intent Classifier (`app/ai/jev.py`):** Classify merchant onboarding intent.

#### 3-Tier Skill Strategy (2 Hours/Day)
* **Must Learn Manually (Do NOT rely on AI):**
  - How to pass `Authorization: Bearer <KEY>` headers in HTTP API calls (`httpx` / `requests`).
  - Parsing JSON strings safely (`json.loads()`) with fallback defaults when AI outputs markdown blocks.
* **Learn Enough to Understand:**
  - Audio MIME types (`audio/ogg`, `audio/wav`) and multipart audio form uploads for Sarvam ASR.
  - Gemini System Prompts and `response_mime_type="application/json"` configuration.
* **Delegate to AI:**
  - Writing prompt engineering text variations and test fixtures.

#### Daily Checklist (Oct 4 – Oct 8)
- [ ] **Oct 4:** Create `app/ai/sarvam.py` using Sarvam Saaras API (`language_code="mr-IN"`).
- [ ] **Oct 5:** Create `app/ai/gemini.py` using `gemini-3.6-flash` with InfoBin JSON schema prompt.
- [ ] **Oct 6:** Build fallback mechanism: if Gemini fails or is rate-limited, return clean default Marathi dictionary.
- [ ] **Oct 7:** Connect AI extraction functions to Abhishek's backend processing pipeline.
- [ ] **Oct 8:** Test voice transcription + Gemini extraction end-to-end on Sakshi's test audio files.

---

### 3.5 Sakshi — QA, Validation & Test Matrix

#### Current Code vs TRD Audit
- **Good:** Sakshi provided 10 realistic SME seed profiles (`shops.json`), `FIELD-MAPPING.md`, and `DEMO-CHECKLIST.md`.
- **Next Step:** Expand testing into active API validation scripts and edge case verification.

#### 3-Tier Skill Strategy (2 Hours/Day)
* **Must Learn Manually (Do NOT rely on AI):**
  - How to write basic Python `pytest` or `unittest` test functions.
  - Validating JSON schemas against expected keys (`name`, `menu`, `location`).
* **Learn Enough to Understand:**
  - HTTP response status codes (`200 OK`, `400 Bad Request`, `422 Unprocessable`).
  - Terminal cURL / Python HTTP client testing.
* **Delegate to AI:**
  - Generating sample test datasets and synthetic voice audio scripts.

#### Daily Checklist (Oct 4 – Oct 8)
- [ ] **Oct 4:** Create `tests/test_schema.py` to validate `shops.json` against InfoBin schema rules.
- [ ] **Oct 5:** Create test cases for multilingual inputs (Marathi text, English text, mixed transliterated text).
- [ ] **Oct 6:** Test photo upload edge cases (large images, unsupported file extensions, missing fields).
- [ ] **Oct 7:** Perform end-to-end verification of WhatsApp flow and Web form flow.
- [ ] **Oct 8:** Final execution of `DEMO-CHECKLIST.md` with full team ahead of Oct 9 presentation.

---

## 4. Summary Rule for Oct 4 – Oct 8

```text
Each Team Member: 2 Hours / Day
        │
        ├── 30 mins: Learn core concept manually (no AI)
        ├── 60 mins: Write component code & test
        └── 30 mins: Reconcile contract with teammate & commit to GitHub
```

By following this daily action plan, every P0 requirement in the PRD and TRD will be fully implemented and verified for the October 9–10 demo.
