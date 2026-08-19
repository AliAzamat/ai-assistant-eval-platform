from pydantic import BaseModel, Field


class AssistantConfig(BaseModel):
    """Everything about an assistant EXCEPT its prompt text (that's versioned)."""
    assistant_id: str
    display_name: str
    model: str = "gpt-4o-mini"
    temperature: float = Field(0.2, ge=0.0, le=1.0)
    # A hard ceiling so a runaway answer can't blow up cost or latency.
    max_output_tokens: int = Field(512, ge=1, le=4096)
    # Knowledge sources this assistant may retrieve from.
    knowledge_sources: list[str] = Field(default_factory=list)
    # "single" = one grounded model call; "agent" = the LangGraph tool loop.
    mode: str = Field("single", pattern="^(single|agent)$")
