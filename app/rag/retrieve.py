from app.config.schema import AssistantConfig
from app.rag.sources import lookup


def ground(config: AssistantConfig, question: str) -> tuple[str | None, list[str]]:
    """Retrieve only from the sources THIS assistant is configured for."""
    hits: list[str] = []
    for source in config.knowledge_sources:
        hits.extend(lookup(source, question))
    if not hits:
        return None, []
    context = "Use ONLY these facts:\n" + "\n".join(hits)
    return context, hits


def build_messages(config: AssistantConfig, system_prompt: str,
                   question: str) -> tuple[list[dict], list[str]]:
    """Assemble the model messages, injecting grounding when available."""
    messages = [{"role": "system", "content": system_prompt}]
    context, hits = ground(config, question)
    if context:
        messages.append({"role": "system", "content": context})
    messages.append({"role": "user", "content": question})
    return messages, hits
