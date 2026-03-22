import asyncio

import google.generativeai as genai

from app.services.llm.base import LLMProvider


class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str, model_name: str) -> None:
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required when LLM_PROVIDER=gemini")
        self.model_name = model_name
        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(model_name=model_name)

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        def _run() -> str:
            response = self._model.generate_content(
                [
                    {"role": "user", "parts": [f"SYSTEM INSTRUCTIONS:\n{system_prompt}"]},
                    {"role": "user", "parts": [user_prompt]},
                ]
            )
            text = response.text or ""
            return text.strip()

        return await asyncio.to_thread(_run)
