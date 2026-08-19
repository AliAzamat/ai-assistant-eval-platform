from dataclasses import dataclass
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.config.schema import AssistantConfig
from app.config.registry import get_config
from app.db.models import PromptVersion


@dataclass
class RunnableAssistant:
    """Config + the live prompt text = everything needed to answer one turn."""
    config: AssistantConfig
    system_prompt: str
    prompt_version: int


def active_prompt(db: Session, assistant_id: str) -> PromptVersion:
    """The one prompt version traffic currently uses."""
    row = db.scalar(
        select(PromptVersion)
        .where(PromptVersion.assistant_id == assistant_id,
               PromptVersion.is_active.is_(True))
    )
    if row is None:
        raise LookupError(f"assistant '{assistant_id}' has no active prompt version")
    return row


def assemble(db: Session, assistant_id: str) -> RunnableAssistant:
    """Join static config with the active versioned prompt."""
    cfg = get_config(assistant_id)
    pv = active_prompt(db, assistant_id)
    return RunnableAssistant(config=cfg, system_prompt=pv.system_prompt,
                             prompt_version=pv.version)
