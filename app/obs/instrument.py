import time
from openai import AsyncOpenAI
from app.obs.pricing import cost_usd
from app.obs.store import save_trace, Trace

client = AsyncOpenAI()


async def instrumented_chat(assistant_id: str, model: str, messages: list) -> str:
    """Call the model and record latency, token cost, and a quality signal."""
    started = time.perf_counter()
    resp = await client.chat.completions.create(model=model, messages=messages)
    latency_ms = (time.perf_counter() - started) * 1000

    usage = resp.usage
    answer = resp.choices[0].message.content or ""
    trace = Trace(
        assistant_id=assistant_id,
        model=model,
        latency_ms=latency_ms,
        input_tokens=usage.prompt_tokens,
        output_tokens=usage.completion_tokens,
        cost_usd=cost_usd(model, usage.prompt_tokens, usage.completion_tokens),
        # finish_reason == "length" means we truncated — a quality red flag.
        truncated=resp.choices[0].finish_reason == "length",
    )
    await save_trace(trace)
    return answer
