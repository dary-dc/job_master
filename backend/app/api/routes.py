from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import PlainTextResponse

from app.config import get_settings
from app.models.schemas import GenerationMeta, GenerationResponse, HealthResponse
from app.services.generator import generate_resume_markdown
from app.services.jd_parser import parse_career_dump, parse_jd
from app.services.cv_parser import parse_cv
from app.services.llm.factory import get_llm_provider

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post("/generate", response_model=GenerationResponse)
async def generate(
    cv: UploadFile = File(...),
    career_dump: UploadFile = File(...),
    jd: UploadFile = File(...),
) -> GenerationResponse:
    settings = get_settings()

    try:
        llm = get_llm_provider(settings)
        cv_text = await parse_cv(cv)
        career_dump_text = await parse_career_dump(career_dump)
        jd_text = await parse_jd(jd)
        markdown = await generate_resume_markdown(
            llm=llm,
            cv_text=cv_text,
            career_dump_text=career_dump_text,
            jd_text=jd_text,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f"Generation failed: {exc}") from exc

    provider_name = settings.llm_provider.lower()
    model_name = settings.gemini_model if provider_name == "gemini" else settings.openai_model

    return GenerationResponse(
        markdown=markdown,
        meta=GenerationMeta(provider=provider_name, model=model_name),
    )


@router.post("/generate.md", response_class=PlainTextResponse)
async def generate_markdown(
    cv: UploadFile = File(...),
    career_dump: UploadFile = File(...),
    jd: UploadFile = File(...),
) -> PlainTextResponse:
    payload = await generate(cv=cv, career_dump=career_dump, jd=jd)
    return PlainTextResponse(content=payload.markdown, media_type="text/markdown")
