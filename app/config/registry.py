from app.config.schema import AssistantConfig

# A startup runs several assistants; this is the catalog of their settings.
_CONFIGS: dict[str, AssistantConfig] = {
    "support": AssistantConfig(
        assistant_id="support",
        display_name="Support Assistant",
        knowledge_sources=["refund", "shipping"],
    ),
    "sales": AssistantConfig(
        assistant_id="sales",
        display_name="Sales Assistant",
        model="gpt-4o",
        temperature=0.4,
    ),
}


def get_config(assistant_id: str) -> AssistantConfig:
    """Look up an assistant's settings, or fail loudly on a typo."""
    try:
        return _CONFIGS[assistant_id]
    except KeyError:
        raise KeyError(f"no assistant configured for id '{assistant_id}'")
