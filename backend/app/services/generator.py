from app.services.llm.base import LLMProvider

SYSTEM_PROMPT = """You are a Truthful Career Consultant.

Goal: Generate a tailored ATS-friendly resume in Markdown for a target job description.

Rules:
1) Use ONLY facts present in the provided CV and the messy career database text.
2) DO NOT invent roles, dates, projects, skills, achievements, or metrics.
3) If an item is ambiguous, prefer conservative wording and avoid unsupported claims.
4) Mirror important JD keywords when truthful and supported by the source text.
5) Output clean, one-column ATS-friendly Markdown with these sections only:
   - Contact
   - Professional Summary
   - Work Experience
   - Skills
   - Education
   - Projects (optional)
6) Keep bullet points concise and impact-oriented.
7) Return Markdown only. No code fences, no commentary.
"""


def _compose_user_prompt(cv_text: str, career_dump_text: str, jd_text: str) -> str:
    return f"""Use the following input sources to produce a tailored resume.

[EXISTING CV]
{cv_text}

[MASTER CAREER DATABASE - MESSY TEXT]
{career_dump_text}

[TARGET JOB DESCRIPTION]
{jd_text}

Required output:
- A single ATS-friendly Markdown resume.
- Keep it truthful and supported by the source data.
- Prioritize relevance to the target JD.
"""


async def generate_resume_markdown(
    llm: LLMProvider,
    cv_text: str,
    career_dump_text: str,
    jd_text: str,
) -> str:
    prompt = _compose_user_prompt(cv_text=cv_text, career_dump_text=career_dump_text, jd_text=jd_text)
    markdown = await llm.generate(system_prompt=SYSTEM_PROMPT, user_prompt=prompt)
    if not markdown.strip():
        raise ValueError("The model returned empty content")
    return markdown.strip()
