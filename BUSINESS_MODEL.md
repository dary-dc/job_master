# JobMaster — Business Model

> **Document type:** Business Model  
> **Version:** 0.1  
> **Date:** March 18, 2026  
> **Audience:** Founders, co-founders, investors

---

## 1. Strategic Position

JobMaster does **not** compete on price. The market for cheap, disposable AI resume wrappers is saturated and margin-less.

JobMaster competes on **compounding value** — the longer a user stays, the deeper their Master Career Database grows, the more irreplaceable the product becomes. This is a fundamentally different business model than time-boxed resume generators.

**The positioning:** JobMaster is the **"Notion for Career History"** — a high-value, senior-professional SaaS that users build into and never want to leave.

---

## 2. Why "Copy & Undercut" Fails

| Problem with price-cutting | Consequence |
|---|---|
| Existing tools have near-100% monthly churn | Underpricing a broken model adds acquisition cost without solving retention |
| Heavily funded competitors (Teal, Rezi) run free tiers indefinitely | A $5 discount is invisible against $0 |
| Raw ChatGPT/Gemini covers the basic use case for free | Any simple wrapper competes against free |
| Price-driven positioning attracts price-sensitive users | These are the first to cancel and least likely to pay for premium features |

**The alternative:** Charge premium pricing to an audience that does not optimize for cheapness. Senior developers applying for $100k+ remote roles are optimizing for **ROI, not cost**.

---

## 3. Revenue Streams

### 3.1 Job Hunt Sprint Pass (Primary — Individual)
**Price:** $29–$49 / 3-month access  
**Rationale:** Aligned to the natural duration of a focused job search. No confusing monthly subscriptions that feel punitive to cancel. A flat "sprint" fee feels like a tool, not a trap.

- Includes full access to Master DB builder, RAG generation, multi-agent fact-checker, PDF export, analytics dashboard, and cover letter agent.
- At the end of the sprint, the account shifts to "inactive" — data preserved, generation disabled.
- Upsell path: renew a Sprint Pass when the next job hunt begins.

### 3.2 Lifetime Database Hosting (Retention — Individual)
**Price:** $15/year  
**Rationale:** This is the "keep the lights on for your career data" fee. It creates a continuous revenue stream from users not actively job hunting, maintains the relationship, and ensures they return to JobMaster — not a competitor — for their next search.

- Users who have built a rich Master DB will pay $15/year without blinking. The cost of rebuilding it from scratch elsewhere is far higher.
- This is a **switching cost converted into a subscription.**

### 3.3 B2B API — Bootcamp Licensing (Scale Revenue)
**Price:** TBD (per-seat or flat monthly license)  
**Target customers:** Coding bootcamps (e.g., Soy Henry, Hack Reactor, General Assembly, Le Wagon)  
**Rationale:** Bootcamps graduate 50–500 students per cohort. Every student needs a resume. Career coaches at bootcamps are overwhelmed. JobMaster's API solves this at scale.

- **Bootcamp value prop:** Students connect GitHub projects; JobMaster auto-drafts ATS-optimized resumes from real project work. Career coaches review and approve, not write from scratch.
- **Revenue model:** Monthly license per bootcamp (e.g., $500–$2,000/month depending on cohort size) or per-student fee ($10–$20 per active student).
- **Strategic value:** Bootcamp students become future individual paying users as they advance in their careers. This is a **customer acquisition channel disguised as a revenue stream.**

---

## 4. Pricing Philosophy

> Target users applying for $100k+ remote roles. The economic frame is: "This tool helps me land a $10k/month salary. A $49 investment for a 3-month hunt is a 200x ROI if it shortens the search by even one week."

- **No $4.99/month tier.** It devalues the product and attracts users who will not find it worth the premium features.
- **No feature-gated free tier initially.** Free tiers are acquisition tools for scale-stage companies. At the current stage, every user interaction generates learning, not just revenue. Charge from day one.
- **Future freemium consideration:** A limited "Build your first 5 Master DB entries" tier may make sense post-product-market-fit to drive organic top-of-funnel.

---

## 5. Go-to-Market Strategy

### Phase 1: Personal Use as Public Proof (Months 1–3)
The founder uses JobMaster to run their own job search.

- **The GitHub Repo IS the marketing.** Publish the repo with an architecture diagram showing: Vector DB, Multi-Agent evaluation loop, automated PDF rendering.
- When sharing the repo or applying to roles, tell the story: *"I built an LLM-powered pipeline that uses RAG to map my career accomplishments to US job requirements."*
- This proves the product works in production and generates authentic social proof.
- Collect 5–10 user testimonials from peers going through their own job hunts.

### Phase 2: Waitlist & Early Access (Month 2–4)
- Launch a minimal landing page focused on the **"Master Career Database"** concept and the **"ATS Truth Guardrail"** feature.
- Run a waitlist. Target communities: Hacker News "Show HN," Dev.to, r/cscareerquestions, LinkedIn senior dev communities, LATAM remote-work communities (Platzi, freeCodeCamp Spanish, etc.).
- Offer waitlist members a discounted Sprint Pass ($29 instead of $49) in exchange for feedback interviews.

### Phase 3: SaaS Launch (Month 4–6)
- Public launch with Sprint Pass pricing.
- Focus on one ICP (Ideal Customer Profile) for acquisition: **Senior backend/fullstack developer, 5+ years experience, targeting US remote roles.**
- Content strategy: Publish articles/threads explaining why ATS optimization is an engineering problem, not an HR problem. Draw the technically curious.

### Phase 4: B2B Pivot (Month 8+)
- Once individual product-market-fit is validated, approach 2–3 coding bootcamps for pilot API partnerships.
- Build the multi-tenant bootcamp dashboard on top of the existing individual product backend.

---

## 6. Retention Mechanism

The Master Career Database is the **retention engine** of the business.

- A user who spends 2 hours building their database has created an asset that doesn't exist anywhere else.
- Each job hunt *adds* to the database (new roles, new metrics, new projects).
- After 2–3 job hunts, the database is so rich that switching to any other tool means starting from zero.
- **This is intentional vendor lock-in through user-created value** — the most ethical and defensible form of lock-in.

### Retention Loop
```
User inputs career history → Database grows richer →
Next job hunt generates better, more targeted resumes →
User builds more trust in the system →
User updates DB more actively → Database grows richer → ...
```

---

## 7. Unit Economics (Projections — Conservative)

| Metric | Year 1 Target |
|---|---|
| Individual Sprint Pass sales | 200 users × $39 avg = **$7,800** |
| Lifetime DB Hosting conversions | 80 users × $15 = **$1,200** |
| B2B Pilot (1 bootcamp, 100 students) | $1,000/month × 4 months = **$4,000** |
| **Year 1 Total Revenue** | **~$13,000** |

These numbers are conservative and serve as a validation target, not a financial forecast. The B2B channel is the primary scale path once individual PMF is confirmed.

---

## 8. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| LLM API cost per generation scales with usage | Implement generation quotas per Sprint Pass. Cache JD parsing results. Optimize prompts for token efficiency. |
| Users don't want to spend time building a Master DB | Reduce friction via GitHub/Jira auto-import. First-run "career dump" wizard. Resume upload → AI-assisted DB population. |
| OpenAI/Google builds this as a native feature | Position around the **data layer** (Master DB + integrations), not the LLM call. The moat is the data structure, not the AI model. |
| Slow B2B sales cycle | Keep B2B as Phase 4. Do not slow individual SaaS development to chase enterprise deals early. |
