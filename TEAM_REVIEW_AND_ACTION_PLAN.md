# KhojDoot Team Review & Action Plan v2.0 (Oct 4 – Oct 8)

**Target Hackathon Demo:** October 9–10, 2026  
**Problem Statement:** PS-29 — Regional-Language No-Code Website Creation Platform  
**Document Purpose:** Code audit against PRD v2.0 & TRD v2.0, contract reconciliation, beginner mistake prevention, and 5-day team execution checklist.

---

## 1. Executive Summary & Team Code Audit

This review updates the team action plan to align with **PRD v2.0** and **TRD v2.0**. The technical roles remain identical, but each role now includes responsibilities for **WebsiteSpec, Component Directory, Website Generator, Website Validation, and Conversational Editing**.

### Summary Matrix

| Team Member | Domain / TRD Role | Primary Target (PRD v2.0 / TRD v2.0) | Critical Task Before Oct 9 Demo |
|---|---|---|---|
| **Abhishek** | FastAPI Backend | Website creation APIs (`POST /website/generate`, `POST /website/edit`) | Reconcile `/ingest` contract and implement `WebsiteSpec` endpoints |
| **Shantanu** | Database & Persistence | `WebsiteSpec`, `WebsiteVersion`, `ValidationResult` persistence | Extend SQLite tables for `WebsiteSpec` and validation metrics |
| **Gayatri** | Web UI & Frontend | Website Preview, Component Directory, Conversational Editor | Build responsive website renderer (`/merchant/[slug]`) & edit controls |
| **Paksha** | AI Processing (Sarvam/Gemini) | Requirement understanding, `WebsiteSpec` generation, Skills | Build `app/ai/sarvam.py`, `app/ai/gemini.py` & Website Planner Skill |
| **Sakshi** | QA & Validation | Website Validator (Structural/Technical/Content/Mobile) | Build validation check suite (`8/8 checks passed`) & evidence matrix |

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
> 4. **Edit the Specification (WebsiteSpec), Not Arbitrary Code:**  
>    Do not allow LLMs to generate uncontrolled raw HTML/JS from scratch. Use `WebsiteSpec` JSON patches and a bounded `Component Directory` to ensure deterministic rendering.

---

## 3. Detailed Member Analysis & Learning Strategy (PRD v2.0 / TRD v2.0)

### 3.1 Abhishek — FastAPI Backend Owner

#### Key TRD v2.0 Deliverables
- **Endpoints:** Implement `POST /merchants/{id}/website/generate`, `GET /merchants/{id}/website`, `POST /merchants/{id}/website/edit`, `POST /merchants/{id}/website/validate`, `POST /merchants/{id}/publish`.
- **Integrations:** Connect Paksha's AI Website Planner, Shantanu's WebsiteSpec persistence, and Gayatri's editor.

#### 3-Tier Skill Strategy (2 Hours/Day)
* **Must Learn Manually (Do NOT rely on AI):**
  - FastAPI Request Lifecycle: Handling `Form()`, `File()`, and JSON body payloads.
  - Asynchronous background task dispatching (`BackgroundTasks`).
* **Learn Enough to Understand:**
  - Meta Cloud API HTTP payload formats and webhook challenge handshakes.
  - RESTful contract design for `WebsiteSpec` patches.
* **Delegate to AI:**
  - Writing boilerplate CRUD SQL queries and Pydantic model definitions.

#### Daily Checklist (Oct 4 – Oct 8)
- [ ] **Oct 4:** Reconcile `/ingest` route to accept `name`, `phone`, `city`, `slug`, and `photos` in one request.
- [ ] **Oct 5:** Build `POST /website/generate` endpoint consuming Paksha's AI `WebsiteSpec`.
- [ ] **Oct 6:** Build `POST /website/edit` endpoint applying natural-language `WebsiteSpec` patches.
- [ ] **Oct 7:** Connect Sakshi's Website Validator and Meta WhatsApp Webhook.
- [ ] **Oct 8:** End-to-end testing with Sakshi; verify backend runtime stability.

---

### 3.2 Shantanu — Database & Persistence Owner

#### Key TRD v2.0 Deliverables
- **Persistence Tables:** Add `website_specs`, `website_versions`, `validation_results`, and `generation_metrics` tables to SQLite (`schema.sql`).
- **Data Integrity:** Keep `InfoBin` as canonical business truth; ensure `WebsiteSpec` references `InfoBin` records without duplicate fields.

#### 3-Tier Skill Strategy (2 Hours/Day)
* **Must Learn Manually (Do NOT rely on AI):**
  - SQLite foreign key constraints (`FOREIGN KEY (shop_id) REFERENCES shops(id)`).
  - Basic SQL indexing (`CREATE INDEX idx_specs_shop ON website_specs(shop_id)`).
* **Learn Enough to Understand:**
  - SQLite JSON functions (`json_extract()`) and JSON column storage.
  - Context managers for database connections (`with sqlite3.connect(...) as conn:`).
* **Delegate to AI:**
  - Writing complex multi-join SQL queries or schema migration scripts.

#### Daily Checklist (Oct 4 – Oct 8)
- [ ] **Oct 4:** Merge `schema.sql` with Abhishek's backend database initialization script (`connection.py`).
- [ ] **Oct 5:** Build `save_website_spec()` and `get_website_spec()` Python helper functions.
- [ ] **Oct 6:** Implement `validation_results` persistence for storing test evidence (`8/8 passed`).
- [ ] **Oct 7:** Populate SQLite database with Sakshi's 10 SME seed profiles from `shops.json`.
- [ ] **Oct 8:** Run load/query benchmark tests to ensure instant $O(1)$ slug lookups.

---

### 3.3 Gayatri — Frontend & Website Interface Owner

#### Key TRD v2.0 Deliverables
- **Component Directory:** Build reusable Bounded Components (`Hero`, `About`, `Services`, `Products`, `Gallery`, `Location`, `Contact`, `Footer`).
- **Interfaces:** Dynamic website renderer (`/merchant/[slug]`), Website Preview, Conversational Editor UI, and KhojDoot Labs telemetry (`/labs`).

#### 3-Tier Skill Strategy (2 Hours/Day)
* **Must Learn Manually (Do NOT rely on AI):**
  - Native JavaScript `fetch()` API and `FormData` construction.
  - DOM Event Listeners (`addEventListener`) and step navigation state management.
* **Learn Enough to Understand:**
  - HTML5 Canvas image resizing (`createImageBitmap`) and Blob creation.
  - Dynamic component tree rendering driven by `WebsiteSpec` JSON.
* **Delegate to AI:**
  - Writing CSS animations, Tailwind styling, and HTML layout scaffolding.

#### Daily Checklist (Oct 4 – Oct 8)
- [ ] **Oct 4:** Parameterize `API_BASE` in `Add Your Shop.html` to support window location origins.
- [ ] **Oct 5:** Build Bounded Component Directory (`Hero`, `Products`, `Location`, `Contact`, `Footer`).
- [ ] **Oct 6:** Build dynamic website renderer (`/merchant/[slug]`) consuming `WebsiteSpec`.
- [ ] **Oct 7:** Build Conversational Editor UI ("Remove testimonials", "Make menu prominent") & KhojDoot Labs dashboard (`/labs`).
- [ ] **Oct 8:** Verify mobile responsiveness across phone browsers for the demo.

---

### 3.4 Paksha — AI Processing & Skills Owner (FLAGGED)

> [!WARNING]
> **Action Required:** Paksha currently has **zero commits** on GitHub. As per TRD v2.0 Section 7, Paksha must take ownership of the AI processing and requirement understanding pipeline immediately.

#### Key TRD v2.0 Deliverables
- **Sarvam Saaras ASR (`app/ai/sarvam.py`):** Transcribe Marathi `.ogg` voice notes (`mr-IN`).
- **Gemini 3.6 Flash (`app/ai/gemini.py`):** Extract structured business facts into `InfoBin` schema.
- **AI Website Planner (`app/ai/planner.py`):** Convert regional-language requirement into `WebsiteSpec` JSON.

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
- [ ] **Oct 5:** Create `app/ai/gemini.py` using `gemini-3.6-flash` with InfoBin & WebsiteSpec JSON prompts.
- [ ] **Oct 6:** Build natural-language edit parser: translate user edits ("Add phone number") into `WebsiteSpec` JSON patches.
- [ ] **Oct 7:** Connect AI extraction & planning functions to Abhishek's backend processing pipeline.
- [ ] **Oct 8:** Test voice transcription + Gemini extraction end-to-end on Sakshi's test audio files.

---

### 3.5 Sakshi — QA, Website Validation & Test Matrix Owner

#### Key TRD v2.0 Deliverables
- **Website Validator (`app/website/validator.py`):** Implement structural, technical, content, mobile, and accessibility validation checks (`8/8 checks passed`).
- **Evidence Matrix:** Maintain measurable validation evidence for competition decision support.

#### 3-Tier Skill Strategy (2 Hours/Day)
* **Must Learn Manually (Do NOT rely on AI):**
  - How to write basic Python `pytest` or `unittest` test functions.
  - Validating `WebsiteSpec` JSON structures against expected component trees.
* **Learn Enough to Understand:**
  - HTTP response status codes (`200 OK`, `400 Bad Request`, `422 Unprocessable`).
  - Automated HTML assertion checks (checking if business name, phone, and menu items appear in rendered HTML).
* **Delegate to AI:**
  - Generating sample test datasets and synthetic voice audio scripts.

#### Daily Checklist (Oct 4 – Oct 8)
- [ ] **Oct 4:** Create `tests/test_schema.py` to validate `shops.json` against InfoBin & WebsiteSpec schema rules.
- [ ] **Oct 5:** Build `WebsiteValidator` suite checking required sections, contact fields, and link integrity.
- [ ] **Oct 6:** Build edit-revalidation test suite: verify that natural-language edits produce valid updated sites.
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

By following this daily action plan, every P0 requirement in PRD v2.0 and TRD v2.0 will be fully implemented and verified for the October 9–10 demo.
