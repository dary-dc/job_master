from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class GenerationMeta(BaseModel):
    provider: str
    model: str


class GenerationResponse(BaseModel):
    markdown: str
    meta: GenerationMeta
