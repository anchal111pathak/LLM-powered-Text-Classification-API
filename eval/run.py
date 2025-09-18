import json
from pathlib import Path
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from app.services.hf_model import HFClassifier

DATASET = Path(__file__).parent / "dataset.jsonl"

def load_dataset():
    out = []
    with open(DATASET, "r", encoding="utf-8") as f:
        for line in f:
            out.append(json.loads(line))
    return out

def run_eval():
    ds = load_dataset()
    clf = HFClassifier()
    y_true, y_pred = [], []

    for rec in ds:
        y_true.append(rec["label"])
        result = clf.classify(rec["text"])
        y_pred.append(result["label"])

    acc = accuracy_score(y_true, y_pred)
    p, r, f1, _ = precision_recall_fscore_support(y_true, y_pred, average="macro", zero_division=0)

    print("Evaluation Results:")
    print(f"Accuracy: {acc:.3f}")
    print(f"Precision: {p:.3f}  Recall: {r:.3f}  F1: {f1:.3f}")

if __name__ == "__main__":
    run_eval()
