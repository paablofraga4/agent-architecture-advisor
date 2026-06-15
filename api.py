"""FastAPI wrapper around the agent arena — ready for a Next.js frontend.

Endpoints:
  - GET  /healthz                        — liveness
  - POST /arena/run        (SSE)         — stream pipeline events + final result
  - GET  /arena/runs?client_id=...        — list past run snapshots
  - GET  /arena/runs/{run_id}            — full snapshot (audit)
  - POST /arena/upload                   — multipart upload of project_case docs

Run with:
    python -m uvicorn api:app --reload --port 8080

The SSE event stream uses one event per pipeline transition (planner, retrieval,
azure, aws, gcp, validation, judge, specialists, final, cost, diagram, audit)
plus a final `result` event with the full AgentArenaResult JSON.
"""
from __future__ import annotations

import asyncio
import json
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel

from agent_arena.arena import run_agent_arena_with_llm_planner_pydantic_async
from agent_arena.config import DEFAULT_MODEL
from agent_arena.schemas import DEFAULT_BUSINESS_CONTEXT
from agent_arena.audit import list_snapshots, load_snapshot
from agent_arena.kb_upload import ingest_document, reindex_async_safe


app = FastAPI(title="Agent Architecture Advisor API", version="1.0")

# CORS open for local Next.js dev. Lock down for production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class RunRequest(BaseModel):
    idea: str
    client_id: Optional[str] = "default"
    model: Optional[str] = None


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


def _sse(event: str, data: dict | str) -> str:
    body = data if isinstance(data, str) else json.dumps(data, ensure_ascii=False)
    return f"event: {event}\ndata: {body}\n\n"


@app.post("/arena/run")
async def arena_run(req: RunRequest):
    queue: asyncio.Queue = asyncio.Queue()

    async def progress_callback(event: str, payload: dict):
        await queue.put((event, payload))

    async def runner():
        try:
            result = await run_agent_arena_with_llm_planner_pydantic_async(
                user_idea=req.idea,
                model=req.model or DEFAULT_MODEL,
                business_context=DEFAULT_BUSINESS_CONTEXT,
                progress_callback=progress_callback,
                client_id=req.client_id,
            )
            await queue.put(("result", result.model_dump(mode="json")))
        except Exception as exc:
            await queue.put(("error", {"error": str(exc)}))
        finally:
            await queue.put(("__done__", {}))

    asyncio.create_task(runner())

    async def event_stream():
        while True:
            event, payload = await queue.get()
            if event == "__done__":
                yield _sse("done", {})
                break
            yield _sse(event, payload)

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.get("/arena/runs")
async def list_runs(client_id: Optional[str] = None):
    return {"runs": list_snapshots(client_id=client_id)}


@app.get("/arena/runs/{run_id}")
async def get_run(run_id: str):
    try:
        return load_snapshot(run_id)
    except FileNotFoundError:
        raise HTTPException(404, "run not found")


@app.post("/arena/upload")
async def upload_doc(
    file: UploadFile = File(...),
    client_id: str = Form("default"),
    doc_type: str = Form("project_case"),
    title: Optional[str] = Form(None),
):
    raw = await file.read()
    result = ingest_document(
        raw_bytes=raw,
        filename=file.filename or "upload",
        client_id=client_id,
        title=title or (file.filename or "upload"),
        doc_type=doc_type,
    )
    if not result["ok"]:
        raise HTTPException(400, result["error"])
    reindex = reindex_async_safe()
    return JSONResponse({"ingest": result, "reindex": reindex})
