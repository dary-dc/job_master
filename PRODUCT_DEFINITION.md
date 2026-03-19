# JobMaster — Product Definition

> **Document type:** Product Definition  
> **Version:** 0.1  
> **Date:** March 18, 2026  
> **Audience:** Founders, early team, investors

---

## 1. Vision

> *"Every senior developer has a decade of achievements scattered across commit histories, Jira tickets, and fading memories. JobMaster is the single source of truth for your career — a living database that knows everything you've ever built, and deploys the right story directly to any job opportunity in seconds."*

JobMaster is not a resume builder. It is a **Career Content Management System** combined with an **AI Deployment Pipeline for Resumes** — treating the job hunt the way a senior engineer would: as a data-driven, automated, integrity-first pipeline.

---

## 2. The Problem

### 2.1 Existing Tools Are Broken by Design
Today's AI resume builders (Teal, Rezi, Kickresume, etc.) share a fundamental flaw: they treat the resume as a **one-time text document**.

The workflow is:
1. User uploads a 1-page PDF.
2. AI rewrites it.
3. User downloads it and cancels their subscription.

**Result:** Near 100% monthly churn. No retention. No compounding value.

### 2.2 The Raw LLM Chat Ceiling
Using ChatGPT or Gemini directly hits a hard ceiling: you can only give the LLM the 1-page resume you already have. It optimizes within a shallow pool of information, can hallucinate metrics, and produces output you still have to manually format into a PDF every time.

### 2.3 The Problems No Current Tool Solves

| Problem | Why it matters |
|---|---|
| **The 1-page information loss** | A 1-page resume is a lossy compression of a 10-year career. ATS and hiring managers only see what made the cut — not the full depth of what you've done. |
| **LLM hallucination risk** | AI tools invent metrics and skills to make the resume look better, which destroys credibility in technical interviews. |
| **Keyword mismatch** | A resume saying "SQL" fails the ATS check when the JD says "PostgreSQL". Humans don't catch this consistently. |
| **Formatting debt** | Every application requires manually reformatting output into Word/PDF. This is pure friction that costs hours per job search. |
| **No institutional memory** | Every job hunt starts from zero. There's no compounding benefit from previous applications. |

---

## 3. Target User

### Primary Persona: The Senior Developer in Transition
- **Experience:** 5–15 years of software engineering
- **Target market:** $100k+ remote positions, primarily US market
- **Pain point:** Too experienced to have a simple resume, too busy to spend 4 hours tailoring it per application
- **Behavior:** Thinks in systems. Responds to technical credibility. Will PAY for tools that save high-cognitive-cost time.
- **Fear:** Looking like a fraud in a technical interview due to an AI-inflated resume.

### Secondary Persona: The Bootcamp Graduate
*(Unlocked via B2B channel — see Business Model)*
- 6–12 months of project-based experience
- Needs help extracting and articulating technical achievements from raw project work
- Managed at scale through bootcamp partnerships

---

## 4. Unique Value Proposition

> **JobMaster turns your entire career history into a queryable database and deploys a hyper-targeted, 100% truthful, ATS-optimized resume to any job in under 30 seconds.**

The UVP rests on three pillars:

1. **Depth over compression:** Your Master Career Database stores everything — the full iceberg, not the tip.
2. **Verified truth:** A multi-agent system cross-references every generated line against your actual career data. Nothing gets invented.
3. **Zero formatting overhead:** Input a job URL. Receive a formatted PDF. No manual work.

---

## 5. Core Features

### 5.1 The Master Career Database
The foundational differentiator of the product.

- A structured database where users record the **full, uncompressed history** of their career: every role, project, feature, bug fix touched, library used, metric improved, and team outcome.
- Can be 10–20 pages of raw career data — this is intentional and desirable.
- Supports free-text "raw notes" fields alongside structured fields so users can dump stream-of-consciousness memories.
- **GitHub / Jira Integration:** Connect repositories and project boards; the AI auto-drafts achievement bullet points from real commits and ticket themes, reducing the input burden for the user.
- **The retention engine:** The database lives on the platform. It becomes more valuable with every update and every job hunt cycle. Users cannot take it elsewhere without significant effort.

### 5.2 RAG-Powered Resume Generation
When a user pastes or links a Job Description:

1. The JD is parsed and its key requirements, keywords, and competency signals are extracted.
2. The system runs **semantic search (RAG)** over the user's Master Career Database to retrieve the most relevant experiences and achievements.
3. Only the top ~15% of the database relevant to this specific JD is surfaced.
4. The AI drafts a targeted 1-page resume from this filtered pool — not from a generic template.

**Result:** Every generated resume is different, hyper-targeted, and drawn from real data.

### 5.3 Multi-Agent Truth Guardrail
Three specialized agents run in sequence on every generation:

| Agent | Role |
|---|---|
| **Writer Agent** | Drafts the resume using JD keywords and retrieved Master DB experiences. |
| **Fact-Checker Agent** | Compares every claim in the draft **strictly** against the Master DB. Flags invented metrics, inflated titles, or skills not in the database. Forces a rewrite if integrity is violated. |
| **ATS Parser Agent** | Simulates ATS keyword matching. Verifies that exact JD keywords appear (e.g., "PostgreSQL" not just "SQL"), headers are standardized, and no tables, columns, or graphics are present. |

The user receives a **final manual confirmation step**: "Does this bullet point accurately reflect your work at [Company]?" before the PDF is generated. Optimization is automated; integrity remains human-authorized.

### 5.4 Automated PDF Generation
- Backend renders the verified JSON output into a **1-column, ATS-optimized PDF** via a LaTeX template or an HTML-to-PDF engine (Puppeteer).
- Users never touch formatting. No Word. No manual PDF export.
- Output is guaranteed to be clean Markdown-converted-to-PDF with no ATS-breaking elements.

### 5.5 Cover Letter / Business Impact Pitch Agent
Generic cover letters are disqualifying in 2026. JobMaster generates a **"Business Impact Pitch"** instead:

- Reads the JD for stated problems and pain points.
- Cross-references the user's Master DB for directly relevant solutions they've delivered.
- Draft structure: *"I noticed your team is working on [Problem]. In my previous role at [Company], I used [Skill] to solve a similar challenge, resulting in [Metric]."*
- Every claim is sourced from the Master DB.

### 5.6 Application Analytics
JobMaster stores every application as a record:
- Job URL
- Resume version generated
- Cover letter generated
- **Outcome:** Interview received? Offer made?

This enables users to run A/B testing on their job hunt:
- *"When I emphasize Cloudflare over AWS, my positive response rate increases by X%."*
- *"Applications to Series B startups convert better than FAANG applications for my profile."*

This is a feature no resume builder offers. It transforms the job hunt into an **engineering feedback loop**.

---

## 6. Competitive Differentiation

| Dimension | Teal / Rezi / Kickresume | Raw ChatGPT/Gemini | **JobMaster** |
|---|---|---|---|
| Data depth | 1-page resume input | 1-page resume input | Full career history database |
| Truth guarantee | None | None | Multi-agent fact-checker against real data |
| ATS optimization | Basic keyword suggestions | Manual, user-driven | Autonomous ATS Parser Agent |
| PDF output | Manual template selection | Copy-paste to Word | Automated, zero-touch PDF rendering |
| Retention value | Low (download and cancel) | None | Master DB = permanent platform lock-in |
| Analytics | None | None | A/B testing pipeline |
| GitHub/Jira sync | None | None | Auto-drafted bullet points from commits |

---

## 7. Success Metrics (Initial Phase)

| Metric | Target (Month 6) |
|---|---|
| Master DB entries per active user | > 15 structured career entries |
| Time to generate a tailored resume | < 30 seconds |
| User-reported accuracy (Fact-Checker approval rate) | > 90% accepted without modification |
| Month-2 retention | > 60% (vs. industry ~20%) |
| Interview callback rate improvement reported by users | > 10% increase vs. pre-JobMaster baseline |
