# A knowledge source is a named bundle of facts the assistant may cite.
# In production each source is a vector-store namespace; here, a dict.
SOURCES: dict[str, dict[str, str]] = {
    "refund": {
        "policy": "Refunds are issued within 30 days of purchase to the original card.",
    },
    "shipping": {
        "times": "Orders ship in 2 business days; tracking is emailed on dispatch.",
    },
    "pricing": {
        "tiers": "Plans are Free, Pro ($20/mo), and Enterprise (contact sales).",
    },
}


def lookup(source: str, question: str) -> list[str]:
    """Naive keyword retrieval within one source (a vector search stand-in)."""
    docs = SOURCES.get(source, {})
    q = question.lower()
    return [text for key, text in docs.items() if key in q or source in q]
