# LLM-powered Text Classification API

## Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Run API
uvicorn app.main:app --reload --port 8000

## Endpoints
- POST `/classify`
- POST `/feedback`
- GET `/metrics`
- GET `/healthz`

## Evaluate
python eval/run.py
Evaluation Results:
Accuracy: 0.667
Precision: 0.500  Recall: 0.667  F1: 0.556

## Design trade-offs & limitations.
Model choice (BART MNLI vs chat LLM): Chose facebook/bart-large-mnli for small footprint, fast CPU inference, and deterministic zero-shot classification via label entailment, trading off few-shot flexibility and nuanced reasoning of larger chat LLMs. This reduces cost/latency but may underperform on subtle toxicity and context-heavy spam
Zero-shot NLI prompting: Uses label hypotheses like “This text is toxic/spam/safe” and picks the highest entailment score; this keeps the system simple and reproducible, trading off domain adaptation that prompt-tuned chat models or fine-tuned heads could provide.
Schema enforcement in API: Response normalization to {class, confidence} is handled in the service layer to guarantee contract stability; this adds parsing/validation code but prevents brittle downstream consumers
Lightweight persistence: Feedback stored in JSONL for simplicity and portability; it’s easy to version and inspect, but lacks concurrency guarantees and query efficiency of relational stores.
Metrics in-memory: Avg and p95 latency are computed over a sliding window in memory for zero-dependency ops; this sacrifices historical analytics and durability compared to Prometheus/Grafana setups.
Small eval set (~20–30 examples): Optimized for quick iteration within the assignment timebox, trading off statistical confidence; results are indicative, not definitive.
## limitation :
Label granularity: Only three labels {toxic, spam, safe}; nuanced categories (harassment, hate subtypes, self-harm) are out of scope and may be mis-bucketed.

Context insensitivity: NLI over single snippets may miss sarcasm, multi-turn context, and implicit harm; thread-aware models or additional heuristics would be needed for production.

Cultural/lingual coverage: BART MNLI is strongest on English; code-mixed or low-resource languages may degrade accuracy without multilingual models or translation.

Calibration of confidence: Entailment probabilities are not perfectly calibrated; reported confidence is monotonic but not guaranteed to be truthful uncertainty without temperature scaling or Platt calibration.

Adversarial robustness: Simple prompts and static labels are vulnerable to obfuscation (leet speak, zero-width chars, spaced profanity); production systems should add regex heuristics, normalization, or ensembles.

Throughput and scaling: CPU inference is fine for low QPS; high-traffic scenarios need batching, GPU inference, or a faster distilled model to maintain p95 latency goals.
