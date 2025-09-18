from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import time
from app.services.hf_model import HFClassifier
from app.prompts.prompts import get_prompt
from app.services.telemetry import telemetry

router = APIRouter()
classifier = HFClassifier()

class ClassifyRequest(BaseModel):
    text: str
    prompt_variant: str = "improved"  # baseline / improved

class ClassifyResponse(BaseModel):
    cls: str
    confidence: float
    prompt_used: str
    latency_ms: int

@router.post("", response_model=ClassifyResponse)
def classify(req: ClassifyRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="text must not be empty")

    prompt = get_prompt(req.prompt_variant, req.text)
    start = time.time()
    result = classifier.classify(req.text)
    latency_ms = int((time.time() - start) * 1000)

    telemetry.record(latency_ms, result["label"])

    return ClassifyResponse(
        cls=result["label"],
        confidence=result["confidence"],
        prompt_used=prompt,
        latency_ms=latency_ms,
    )
