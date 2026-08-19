from dataclasses import dataclass
import json
import redis.asyncio as redis

r = redis.from_url("redis://localhost:6379")


@dataclass
class Trace:
    assistant_id: str
    model: str
    latency_ms: float
    input_tokens: int
    output_tokens: int
    cost_usd: float
    truncated: bool


async def save_trace(t: Trace) -> None:
    """Append a trace to a capped per-assistant list and publish it live."""
    payload = json.dumps(t.__dict__)
    key = f"traces:{t.assistant_id}"
    await r.lpush(key, payload)
    await r.ltrim(key, 0, 999)          # keep the last 1000 traces
    await r.publish("traces", payload)  # fan out to live dashboards
