# JobMaster — Technical Architecture

> **Document type:** Technical Architecture  
> **Version:** 0.1  
> **Date:** March 18, 2026  
> **Audience:** Founders, technical co-founders, senior engineers  

---

## 1. Guiding Principles

1. **The moat is the data layer, not the LLM call.** Every architectural decision prioritizes the integrity and richness of the Master Career Database over clever prompting.
2. **No hallucinations ship to the user.** Every AI-generated claim must be traceable to a specific record in the Master DB before it reaches the PDF.
3. **Zero formatting overhead.** The user's job ends at content approval. The system handles all rendering.
4. **Show the architecture.** This system is itself a portfolio artifact. The design should be defensible in a system design interview.

---

## 2. High-Level System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND (Next.js)                    │
│  ┌─────────────┐  ┌──────────────────┐  ┌───────────────┐  │
│  │  Master DB   │  │  JD Input / URL  │  │  Analytics    │  │
│  │  Editor UI  │  │  Parser UI       │  │  Dashboard    │  │
│  └─────┬───────┘  └────────┬─────────┘  └───────┬───────┘  │
└────────┼────────────────────┼────────────────────┼──────────┘
         │ REST / tRPC        │                    │
┌────────▼────────────────────▼────────────────────▼──────────┐
│                        BACKEND API                           │
│            (Node.js / Python — FastAPI or Express)          │
│                                                              │
│  ┌──────────────┐  ┌─────────────────┐  ┌───────────────┐  │
│  │  DB Service  │  │  RAG Pipeline   │  │  Agent        │  │
│  │  (CRUD +     │  │  (Embed + Query │  │  Orchestrator │  │
│  │  Validation) │  │   Vector Store) │  │               │  │
│  └──────┬───────┘  └────────┬────────┘  └───────┬───────┘  │
│         │                   │                    │           │
│  ┌──────▼───────────────────▼────────────────────▼───────┐  │
│  │              LLM Gateway (Gemini 1.5 Pro / GPT-4o)    │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────┐   ┌──────────────────────────┐   │
│  │  PDF Renderer        │   │  Integration Layer       │   │
│  │  (LaTeX / Puppeteer) │   │  (GitHub API, Jira API)  │   │
│  └──────────────────────┘   └──────────────────────────┘   │
└──────────────────────────────────────┬──────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────┐
│                        DATA LAYER                            │
│  ┌─────────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  PostgreSQL      │  │  Vector DB   │  │  File Storage │  │
│  │  (Supabase)      │  │  (pgvector / │  │  (generated   │  │
│  │  Master DB +     │  │   Pinecone)  │  │   PDFs)       │  │
│  │  Analytics       │  │              │  │               │  │
│  └─────────────────┘  └──────────────┘  └───────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Tech Stack

| Layer | Technology | Rationale |
|---|---|---|
| Frontend | Next.js (App Router) | SSR for landing/marketing pages; React for dashboard UI |
| Backend | Node.js (Express) or Python (FastAPI) | FastAPI preferred if the RAG pipeline is Python-heavy; Express if the team is TS-first |
| LLM | Gemini 1.5 Pro (primary) / GPT-4o (fallback) | Gemini 1.5 Pro's 1M token context window handles large Master DBs without chunking |
| Relational DB | PostgreSQL via Supabase | Handles Master DB schema, user accounts, analytics. Supabase provides auth out of the box |
| Vector DB | pgvector (extension on Supabase) or Pinecone | pgvector keeps the stack simple initially; migrate to Pinecone at scale |
| PDF Rendering | LaTeX (via pdflatex) or Puppeteer (HTML→PDF) | LaTeX produces superior typographic output; Puppeteer is the easier fallback |
| File Storage | Supabase Storage or S3-compatible bucket | Store generated PDFs per application record |
| Auth | Supabase Auth (email + GitHub OAuth) | GitHub OAuth enables frictionless repo connection for the integration layer |

---

## 4. Master Career Database Schema

The schema models a career as a collection of **Experiences** (roles/projects), each containing **Accomplishments** (atomic, verifiable achievements), tagged with **Skills** and **Metrics**.

### 4.1 Core Tables

```sql
-- Users
CREATE TABLE users (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email         TEXT UNIQUE NOT NULL,
  github_handle TEXT,
  created_at    TIMESTAMPTZ DEFAULT NOW()
);

-- Top-level career experiences: jobs, projects, freelance work, open source
CREATE TABLE experiences (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
  title           TEXT NOT NULL,          -- e.g. "Senior Backend Engineer"
  company         TEXT NOT NULL,          -- e.g. "Acme Corp"
  start_date      DATE NOT NULL,
  end_date        DATE,                   -- NULL = current role
  employment_type TEXT,                   -- full-time, contract, freelance, oss
  raw_notes       TEXT,                   -- free-text stream-of-consciousness dump
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Atomic achievement bullet points — the core unit of the DB
CREATE TABLE accomplishments (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  experience_id   UUID REFERENCES experiences(id) ON DELETE CASCADE,
  user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
  raw_text        TEXT NOT NULL,    -- The user's original, unpolished description
  verified        BOOLEAN DEFAULT FALSE,  -- User has confirmed this is accurate
  source_type     TEXT,             -- 'manual' | 'github_commit' | 'jira_ticket'
  source_ref      TEXT,             -- GitHub SHA or Jira ticket ID for traceability
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Skills taxonomy
CREATE TABLE skills (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name        TEXT UNIQUE NOT NULL,  -- e.g. "PostgreSQL", "Kubernetes", "RAG"
  category    TEXT                   -- e.g. "Database", "Infrastructure", "AI/ML"
);

-- Many-to-many: accomplishments ↔ skills
CREATE TABLE accomplishment_skills (
  accomplishment_id UUID REFERENCES accomplishments(id) ON DELETE CASCADE,
  skill_id          UUID REFERENCES skills(id) ON DELETE CASCADE,
  PRIMARY KEY (accomplishment_id, skill_id)
);

-- Quantitative metrics linked to accomplishments
CREATE TABLE metrics (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  accomplishment_id UUID REFERENCES accomplishments(id) ON DELETE CASCADE,
  description       TEXT NOT NULL,  -- e.g. "Reduced API latency"
  value             TEXT NOT NULL,  -- e.g. "30%"
  verified          BOOLEAN DEFAULT FALSE
);
```

### 4.2 Analytics Tables

```sql
-- One record per job application
CREATE TABLE applications (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       UUID REFERENCES users(id) ON DELETE CASCADE,
  job_url       TEXT,
  company_name  TEXT,
  role_title    TEXT,
  applied_at    TIMESTAMPTZ DEFAULT NOW(),
  outcome       TEXT  -- 'no_response' | 'rejected' | 'interview' | 'offer'
);

-- One record per generated resume (multiple versions possible per application)
CREATE TABLE resume_versions (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  application_id  UUID REFERENCES applications(id) ON DELETE CASCADE,
  jd_snapshot     TEXT,       -- full JD text at time of generation
  pdf_url         TEXT,       -- link to stored PDF
  agent_log       JSONB,      -- full Writer/Fact-Checker/ATS agent trace
  created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 5. RAG Pipeline

The RAG pipeline is the core technical differentiator. It enables semantic retrieval from the full Master DB rather than keyword matching.

### 5.1 Indexing (runs on DB write)
1. On every `accomplishment` INSERT or UPDATE, the backend generates a text embedding of `raw_text` using the LLM provider's embedding API (e.g., `text-embedding-004`).
2. The embedding vector is stored in pgvector alongside the accomplishment record.
3. A composite embedding is also generated for each `experience` (aggregating all its accomplishments) for coarse-grained retrieval.

### 5.2 Query (runs on JD submission)
1. User pastes a JD or provides a URL (URL → scraped via backend).
2. The JD is parsed by the LLM to extract: required skills, preferred skills, seniority signals, domain keywords, and stated pain points.
3. An embedding is generated for the parsed JD.
4. A vector similarity search (cosine distance) retrieves the top-N accomplishments from the user's database.
5. The retrieved accomplishments, plus the full JD analysis, are passed to the Agent Orchestrator.

```
JD Input → Parse & Embed → Vector Search over user's accomplishments →
Top-N relevant records → Agent Orchestrator
```

---

## 6. Multi-Agent Orchestration

Three agents run sequentially. Each agent's output is the next agent's input.

### Agent 1 — The Writer
**Input:** Parsed JD requirements + Top-N retrieved accomplishments from Master DB  
**Task:** Draft a 1-page resume using only the provided accomplishments. Rephrase bullet points using JD keywords where semantically accurate.  
**Constraint (system prompt):** *"You are a truthful career consultant. Do not invent skills, metrics, or roles. Every bullet point must be directly derivable from the provided accomplishments data. Use the exact keyword from the JD (e.g., 'PostgreSQL') if the accomplishment references that technology — even if the user wrote 'SQL'."*  
**Output:** Draft resume as structured JSON.

### Agent 2 — The Fact-Checker
**Input:** Draft resume JSON + original accomplishment records from Master DB  
**Task:** Cross-reference every claim in the draft against the source records. Flag any invented metric, unverifiable skill, or inflated title.  
**Constraint (system prompt):** *"You are a compliance auditor. Accept a claim ONLY if you can point to the specific accomplishment_id in the provided data that supports it. Reject and rewrite any claim that exceeds what the source data supports."*  
**Output:** Verified resume JSON with a `fact_check_log` array.

### Agent 3 — The ATS Parser
**Input:** Verified resume JSON + original JD  
**Task:** Run ATS simulation. Check for exact keyword matches, standardized section headers, and absence of ATS-breaking formatting.  
**Compliance checklist:**
- Required JD keywords present verbatim
- Headers: "Work Experience", "Education", "Skills", "Projects" (no creative equivalents)
- No tables, columns, text boxes, or inline graphics
- 1-column layout enforced
- Contact info in body text, not in headers/footers  
**Output:** ATS-ready resume JSON + `ats_report` with keyword coverage score.

### User Confirmation Gate
Before PDF rendering, the frontend presents the user with each generated bullet point alongside the source accomplishment record. The user explicitly confirms or rejects each claim. **This is the integrity checkpoint.** No PDF is generated without explicit user confirmation.

---

## 7. PDF Generation Pipeline

```
Verified Resume JSON
        │
        ▼
Template Engine
├── Option A: LaTeX template (pdflatex)
│   - Superior typographic quality
│   - Best ATS compatibility
│   - Hosted LaTeX rendering via a sidecar container or cloud function
│
└── Option B: Puppeteer (HTML → PDF)
    - Easier to iterate on template design
    - Good ATS compatibility with a 1-column HTML template
    - Runs as a Node.js microservice
        │
        ▼
PDF file stored in Supabase Storage / S3
        │
        ▼
Presigned URL returned to frontend → User downloads
PDF URL stored in resume_versions table
```

---

## 8. Integration Layer

### 8.1 GitHub Integration
- User authenticates via GitHub OAuth (Supabase Auth handles the token).
- Backend queries the GitHub API for the user's commits, filtered by date range and repo.
- Commit messages and diffs are passed to an LLM prompt that drafts `accomplishment` records in the Master DB schema.
- Drafted records are surfaced in the UI as **unverified** (`verified = FALSE`). User reviews and confirms before they can be used in generation.

### 8.2 Jira Integration
- User provides Jira API token and workspace URL.
- Backend queries completed tickets assigned to the user.
- Ticket summaries and descriptions are parsed to draft `accomplishment` records, tagged with inferred skills.
- Same unverified → user review → confirmed flow as GitHub integration.

---

## 9. Security Considerations

- **API keys:** LLM API keys stored in environment variables only, never in client-side code or the DB.
- **JD scraping:** URL-based JD fetching is restricted to known job board domains to prevent SSRF. Alternatively, scraping runs via a sandboxed lambda with no internal network access.
- **User data isolation:** All DB queries are scoped by `user_id` with row-level security (RLS) enforced at the Supabase/PostgreSQL layer.
- **Third-party tokens (GitHub/Jira):** Stored encrypted at rest. Rotated on user request. Scoped to read-only permissions.
- **PDF generation:** LaTeX/Puppeteer runs in a sandboxed environment. User content is sanitized before template injection to prevent LaTeX injection or HTML injection attacks.

---

## 10. Development Phases

### Phase 1 — MVP (Weeks 1–6)
- [ ] User auth (Supabase Auth)
- [ ] Master DB CRUD UI (Experiences + Accomplishments)
- [ ] Manual JD paste input
- [ ] Writer Agent (single-agent, no fact-checker yet)
- [ ] Puppeteer PDF output
- [ ] Basic application tracking (job URL + outcome field)

### Phase 2 — Core Product (Weeks 7–12)
- [ ] RAG pipeline (pgvector embeddings on accomplishments)
- [ ] Fact-Checker Agent
- [ ] ATS Parser Agent
- [ ] User confirmation gate UI
- [ ] LaTeX template option
- [ ] Cover Letter / Business Impact Pitch Agent

### Phase 3 — Growth Features (Weeks 13–20)
- [ ] GitHub integration (commit → Draft accomplishment)
- [ ] Jira integration
- [ ] Analytics dashboard (A/B testing view)
- [ ] Lifetime DB hosting tier (inactive account state)

### Phase 4 — B2B Layer (Month 6+)
- [ ] Multi-tenant bootcamp dashboard
- [ ] Bulk student account provisioning
- [ ] API endpoints for bootcamp CMS integration
