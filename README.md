# JobMaster

> **The "Notion for Career History" — an AI-powered Career CMS and Resume Deployment Pipeline for Senior Engineers.**

JobMaster is not a resume builder. It is a **personalized CI/CD pipeline for your career.**

You build a deep, structured database of everything you've ever done. When you find a job, the system semantically retrieves the most relevant 15% of your career history, drafts a hyper-targeted resume using a multi-agent pipeline that guarantees no hallucinations, and renders a 1-column ATS-optimized PDF — in under 30 seconds.

---

## The Problem with Existing Tools

Every AI resume builder shares the same fatal flaw: they treat the resume as a one-time text document. You upload a 1-page PDF, the AI rewrites it, you download it, and you cancel. Near 100% monthly churn. No compounding value.

Using raw ChatGPT hits a different ceiling: you're limited to the information in the 1-page resume you already have, the AI invents metrics to make you look good, and you still have to manually format the output every time.

JobMaster solves all three problems.

---

## How It Works

```
Your Entire Career History (Master DB)
         │
         ▼ RAG Semantic Search
You paste a Job Description
         │
         ▼
 ┌───────────────────────────────────┐
 │  Writer Agent                     │
 │  → Drafts resume from relevant    │
 │    DB entries using JD keywords   │
 └─────────────┬─────────────────────┘
               │
 ┌─────────────▼─────────────────────┐
 │  Fact-Checker Agent               │
 │  → Cross-references every claim   │
 │    against your Master DB.        │
 │    Flags invented metrics.        │
 └─────────────┬─────────────────────┘
               │
 ┌─────────────▼─────────────────────┐
 │  ATS Parser Agent                 │
 │  → Verifies keyword coverage,     │
 │    standardized headers,          │
 │    no ATS-breaking formatting     │
 └─────────────┬─────────────────────┘
               │
         User confirms each bullet point
               │
               ▼
         ATS-Optimized PDF
```

---

## Core Features

- **Master Career Database** — A structured store of every role, achievement, metric, and technology in your career history. Much richer than any 1-page resume.
- **RAG-Powered Generation** — Semantic search retrieves only what's relevant to each specific JD.
- **Multi-Agent Truth Guardrail** — Three agents (Writer → Fact-Checker → ATS Parser) ensure the output is accurate, verified, and ATS-ready.
- **Zero-Touch PDF Rendering** — LaTeX or Puppeteer renders a formatted PDF. No manual formatting.
- **Cover Letter / Business Impact Pitch** — JD-specific pitch letters sourced from real career data.
- **Application Analytics** — A/B test your job hunt. Track which resume versions generate callbacks.
- **GitHub / Jira Integration** — Auto-draft accomplishment bullets from real commits and tickets.

---

## Documentation

| Document | Description |
|---|---|
| [PRODUCT_DEFINITION.md](./PRODUCT_DEFINITION.md) | Vision, problem, target users, features, UVP, competitive landscape |
| [BUSINESS_MODEL.md](./BUSINESS_MODEL.md) | Monetization, pricing, go-to-market, retention strategy |
| [TECHNICAL_ARCHITECTURE.md](./TECHNICAL_ARCHITECTURE.md) | System design, data schemas, agent pipeline, dev phases |

---

## Status

> **Phase:** Pre-development — Product & Architecture definition  
> **Date:** March 2026

This repository is the starting point. The documentation above defines what gets built.

---

## The "Why Build This" Story

> *"I wanted to optimize my job search, so I built an LLM-powered pipeline that uses RAG to map my actual career accomplishments to specific job requirements — with a multi-agent fact-checking layer that guarantees I never submit a hallucinated metric."*

This project exists because the job hunt is an engineering problem, and it deserves an engineering solution.
