from fastapi import APIRouter
from pydantic import BaseModel
from app.services.feedback_store import FeedbackStore

router = APIRouter()
store = FeedbackStore("data/feedback.jsonl")

class FeedbackIn(BaseModel):
    text: str
    predicted: str
    correct: str

@router.post("")
def post_feedback(f: FeedbackIn):
    store.add_feedback(f.dict())
    return {"status": "ok"}
