import statistics
from collections import Counter

class Telemetry:
    def __init__(self):
        self.latencies = []
        self.total_requests = 0
        self.class_counts = Counter()

    def record(self, latency_ms: int, label: str):
        self.latencies.append(latency_ms)
        self.total_requests += 1
        self.class_counts[label] += 1

    def get_latency_summary(self):
        if not self.latencies:
            return {"avg_ms": 0, "p95_ms": 0}
        avg = int(statistics.mean(self.latencies))
        p95 = int(sorted(self.latencies)[int(0.95 * len(self.latencies)) - 1])
        return {"avg_ms": avg, "p95_ms": p95}

telemetry = Telemetry()
