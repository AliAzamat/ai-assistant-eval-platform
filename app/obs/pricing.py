# USD per 1K tokens, by model. The single source of truth for cost math.
PRICES = {
    "gpt-4o-mini": {"input": 0.00015, "output": 0.00060},
    "gpt-4o": {"input": 0.0025, "output": 0.0100},
}


def cost_usd(model: str, input_tokens: int, output_tokens: int) -> float:
    """Turn a usage record into dollars."""
    p = PRICES.get(model)
    if not p:
        return 0.0
    return (input_tokens / 1000) * p["input"] + (output_tokens / 1000) * p["output"]
