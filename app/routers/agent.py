from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.config.registry import get_config
from app.agent.run import run_turn

router = APIRouter(prefix="/assistants/{assistant_id}/agent", tags=["agent"])


class AgentTurn(BaseModel):
    message: str


@router.post("/{thread_id}/chat")
async def agent_chat(assistant_id: str, thread_id: str, body: AgentTurn) -> dict:
    """Run a stateful, tool-using agent turn — only if this assistant is agent-mode."""
    cfg = get_config(assistant_id)
    if cfg.mode != "agent":
        raise HTTPException(400, f"assistant '{assistant_id}' is not in agent mode")
    answer = await run_turn(body.message, assistant_id, thread_id)
    return {"answer": answer, "mode": "agent"}
