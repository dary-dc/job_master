import asyncio

from openai import OpenAI

from app.services.llm.base import LLMProvider


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, model_name: str) -> None:
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
        self.model_name = model_name
        self._client = OpenAI(api_key=api_key)

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        def _run() -> str:
            response = self._client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
            )
            text = response.choices[0].message.content or ""
            return text.strip()

        return await asyncio.to_thread(_run)
