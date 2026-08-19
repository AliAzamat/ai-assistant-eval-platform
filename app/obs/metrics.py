import json
import redis.asyncio as redis

r = redis.from_url("redis://localhost:6379")


def _percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    idx = min(len(s) - 1, int(pct / 100 * len(s)))
    return s[idx]


async def snapshot(assistant_id: str) -> dict:
    """Roll the recent trace window into the numbers a dashboard shows."""
    raw = await r.lrange(f"traces:{assistant_id}", 0, -1)
    traces = [json.loads(x) for x in raw]
    if not traces:
        return {"count": 0}
    latencies = [t["latency_ms"] for t in traces]
    return {
        "count": len(traces),
        "p50_latency_ms": _percentile(latencies, 50),
        "p95_latency_ms": _percentile(latencies, 95),
        "total_cost_usd": round(sum(t["cost_usd"] for t in traces), 4),
        "truncation_rate": sum(t["truncated"] for t in traces) / len(traces),
    }


async def quality_snapshot(assistant_id: str) -> dict:
    """Roll the sampled quality window into a hallucination + correctness view."""
    raw = await r.lrange(f"quality:{assistant_id}", 0, -1)
    judged = [json.loads(x) for x in raw]
    if not judged:
        return {"judged": 0}
    n = len(judged)
    hallucination_rate = sum(j["hallucinated"] for j in judged) / n
    avg_correct = sum(j["correct"] for j in judged) / n
    return {
        "judged": n,
        "hallucination_rate": round(hallucination_rate, 3),
        "avg_correct": round(avg_correct, 3),
        # A single 0–1 quality score: correctness penalized by hallucination.
        "quality_score": round(avg_correct * (1 - hallucination_rate), 3),
    }
