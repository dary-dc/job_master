from app.config import Settings
from app.services.llm.base import LLMProvider
from app.services.llm.gemini import GeminiProvider
from app.services.llm.openai_provider import OpenAIProvider


def get_llm_provider(settings: Settings) -> LLMProvider:
    provider = settings.llm_provider.strip().lower()

    if provider == "gemini":
        return GeminiProvider(
            api_key=settings.gemini_api_key or "",
            model_name=settings.gemini_model,
        )

    if provider == "openai":
        return OpenAIProvider(
            api_key=settings.openai_api_key or "",
            model_name=settings.openai_model,
        )

    raise ValueError("LLM_PROVIDER must be either 'gemini' or 'openai'")
