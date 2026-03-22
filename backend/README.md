# JobMaster Backend (MVP)

This backend-only MVP generates a tailored Markdown resume from:
1. A current CV text file
2. A messy career dump text file (initial database)
3. A target job description text file

## Stack
- FastAPI
- LLM provider abstraction: Gemini or OpenAI

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:
   - `pip install -e .`
3. Copy `.env.example` to `.env` and fill API keys.

## Run

```bash
uvicorn app.main:app --app-dir backend --reload
```

## Endpoints
- `GET /health`
- `POST /generate` (JSON response with markdown + metadata)
- `POST /generate.md` (raw markdown response)

## Example request

```bash
curl -X POST "http://127.0.0.1:8000/generate.md" \
  -F "cv=@samples/sample_cv.txt" \
  -F "career_dump=@samples/sample_career_dump.txt" \
  -F "jd=@samples/sample_jd.txt"
```
