from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.db.session import session_scope
from app.config.assemble import assemble
from app.rag.retrieve import build_messages
from app.obs.instrument import instrumented_chat
from app.obs.quality import score_live_bg

router = APIRouter(prefix="/assistants/{assistant_id}", tags=["chat"])


class ChatTurn(BaseModel):
    message: str


@router.post("/chat")
async def chat(assistant_id: str, body: ChatTurn) -> dict:
    """One trustworthy turn: assemble → ground → instrument → sample-score."""
    with session_scope() as db:
        ra = assemble(db, assistant_id)            # config + active prompt

    messages, hits = build_messages(ra.config, ra.system_prompt, body.message)
    answer = await instrumented_chat(             # latency + cost + truncation
        assistant_id, ra.config.model, messages,
    )
    reference = "\n".join(hits)                    # what we grounded on
    score_live_bg(assistant_id, body.message, answer, reference)  # sampled, async
    return {"answer": answer, "prompt_version": ra.prompt_version,
            "grounded": bool(hits)}
