from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()
generator = GeminiDocumentGenerator()

class DocumentRequest(BaseModel):
    document_type: str = Field(min_length=2, max_length=120)
    parties: str = Field(min_length=2, max_length=4000)
    terms: str = Field(min_length=2, max_length=8000)
    dates: str = Field(min_length=1, max_length=100)

@router.post("/generate")
def generate_document(request: DocumentRequest):
    try:
        return {"document": generator.generate_document(request.document_type, request.parties, request.terms, request.dates)}
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
