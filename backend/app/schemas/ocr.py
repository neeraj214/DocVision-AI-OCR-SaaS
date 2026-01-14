from pydantic import BaseModel
from typing import Any


class OCRResponse(BaseModel):
    text: str
    structured: Any
    confidence: float
    language: str
    pdf_url: str

