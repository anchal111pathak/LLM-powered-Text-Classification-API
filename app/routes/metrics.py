from fastapi import APIRouter
from app.services.telemetry import telemetry
from app.services.feedback_store import FeedbackStore

router = APIRouter()
store = FeedbackStore("data/feedback.jsonl")

@router.get("")
def get_metrics():
    fb = store.load_all()
    positive = sum(1 for x in fb if x.get("predicted") == x.get("correct"))
    negative = len(fb) - positive
    return {
        "total_requests": telemetry.total_requests,
        "class_distribution": telemetry.class_counts,
        "feedback_counts": {"positive": positive, "negative": negative},
        "latency": telemetry.get_latency_summary(),
        "stored_feedback": len(fb),
    }
