import asyncio
import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import redis.asyncio as redis

router = APIRouter()
r = redis.from_url("redis://localhost:6379")


async def _event_stream():
    """Subscribe to live traces and yield each as an SSE 'data:' frame."""
    pubsub = r.pubsub()
    await pubsub.subscribe("traces")
    async for message in pubsub.listen():
        if message["type"] != "message":
            continue
        data = message["data"].decode()
        yield f"data: {data}\n\n"


@router.get("/metrics/stream")
async def stream():
    # text/event-stream is the SSE content type the browser understands.
    return StreamingResponse(_event_stream(), media_type="text/event-stream")
