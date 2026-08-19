import asyncio
import json
import random
import redis.asyncio as redis
from app.evals.judge import judge
from app.evals.cases import EvalCase

r = redis.from_url("redis://localhost:6379")

# Judging every answer would double model spend, so sample a fraction.
SAMPLE_RATE = 0.10


async def score_live(assistant_id: str, question: str, answer: str,
                     reference: str) -> None:
    """Sample-score one live answer for hallucination and publish the signal."""
    if random.random() > SAMPLE_RATE:
        return  # not sampled this time
    case = EvalCase(id="live", question=question, expected=reference,
                    must_include=[])
    verdict = await judge(case, answer)          # reuse the eval LLM-judge
    payload = json.dumps({
        "assistant_id": assistant_id,
        "hallucinated": bool(verdict.get("hallucinated")),
        "correct": float(verdict.get("correct", 0.0)),
    })
    await r.lpush(f"quality:{assistant_id}", payload)
    await r.ltrim(f"quality:{assistant_id}", 0, 499)
    await r.publish("quality", payload)


def score_live_bg(assistant_id: str, question: str, answer: str,
                  reference: str) -> None:
    """Fire-and-forget: scoring must never slow the user's response."""
    asyncio.create_task(score_live(assistant_id, question, answer, reference))
