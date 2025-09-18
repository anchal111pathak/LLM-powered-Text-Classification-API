from fastapi import FastAPI
from app.routes import classify, feedback, metrics, health

app = FastAPI(title="LLM Text Classification API")

app.include_router(classify.router, prefix="/classify", tags=["classify"])
app.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
app.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
app.include_router(health.router, prefix="/healthz", tags=["healthz"])
