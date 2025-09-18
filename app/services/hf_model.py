from transformers import pipeline

class HFClassifier:
    def __init__(self):
        self.labels = ["toxic", "spam", "safe"]
        self.pipeline = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    def classify(self, text: str):
        result = self.pipeline(text, candidate_labels=self.labels)
        label = result["labels"][0]
        confidence = float(result["scores"][0])
        return {"label": label, "confidence": confidence}
