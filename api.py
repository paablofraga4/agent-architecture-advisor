"""FastAPI wrapper around the agent arena — production-ready for a Next.js frontend.

Security / scaling layer:
  - Supabase JWT auth (see auth.py). OPEN mode when env unset (local dev/tests).
  - Per-user run quota: 1 free run, admins unlimited. Counted on success only.
  - Runs are scoped to the authenticated user (no cross-tenant reads).
  - CORS locked to CORS_ORIGINS (comma-separated env).
  - IP rate limiting via slowapi as a coarse abuse guard.
  - SSE stream is cancelled when the client disconnects (no wasted tokens).

Endpoints:
  - GET  /healthz                         — liveness
  - GET  /me                              — current user + quota
  - POST /arena/run        (SSE)          — stream pipeline events + final result
  - GET  /arena/runs                      — list the caller's past runs
  - GET  /arena/runs/{run_id}             — full snapshot (owner/admin only)
  - POST /arena/upload                    — multipart upload of project_case docs

Run with:
    python -m uvicorn api:app --reload --port 8080
"""
from __future__ import annotations

import asyncio
import json
import os
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from agent_arena.arena import run_agent_arena_with_llm_planner_pydantic_async
from agent_arena.config import DEFAULT_MODEL
from agent_arena.schemas import DEFAULT_BUSINESS_CONTEXT
from agent_arena.audit import list_snapshots, load_snapshot
from agent_arena.kb_upload import ingest_document, reindex_async_safe
from auth import (
    AUTH_ENABLED,
    CurrentUser,
    get_current_user,
    require_run_quota,
    increment_runs_used,
)

app = FastAPI(title="Agent Architecture Advisor API", version="2.0")

# --- CORS ---------------------------------------------------------------
# Comma-separated allowed origins, e.g. "https://app.tudominio.com,http://localhost:3000".
_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000")
ALLOWED_ORIGINS = [o.strip() for o in _origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Rate limiting ------------------------------------------------------
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def _rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": {"code": "RATE_LIMITED", "message": "Demasiadas peticiones, prueba en un momento."}},
    )


class RunRequest(BaseModel):
    idea: str
    model: Optional[str] = None


def _sse(event: str, data: dict | str) -> str:
    body = data if isinstance(data, str) else json.dumps(data, ensure_ascii=False)
    return f"event: {event}\ndata: {body}\n\n"


@app.get("/healthz")
async def healthz():
    return {"status": "ok", "auth_enabled": AUTH_ENABLED}


@app.get("/me")
async def me(user: CurrentUser = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "run_limit": user.run_limit,
        "runs_used": user.runs_used,
        "has_quota": user.has_quota,
        "is_admin": user.is_admin,
    }


@app.post("/arena/run")
@limiter.limit("10/minute")
async def arena_run(
    request: Request,
    body: RunRequest,
    user: CurrentUser = Depends(require_run_quota),
):
    # Runs are always scoped to the authenticated user id — clients can't spoof it.
    client_id = user.id
    queue: asyncio.Queue = asyncio.Queue()
    run_succeeded = {"ok": False}

    async def progress_callback(event: str, payload: dict):
        await queue.put((event, payload))

    async def runner():
        try:
            result = await run_agent_arena_with_llm_planner_pydantic_async(
                user_idea=body.idea,
                model=body.model or DEFAULT_MODEL,
                business_context=DEFAULT_BUSINESS_CONTEXT,
                progress_callback=progress_callback,
                client_id=client_id,
            )
            await queue.put(("result", result.model_dump(mode="json")))
            run_succeeded["ok"] = True
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            await queue.put(("error", {"error": str(exc)}))
        finally:
            await queue.put(("__done__", {}))

    task = asyncio.create_task(runner())

    async def event_stream():
        try:
            while True:
                # Stop burning tokens if the browser tab is gone.
                if await request.is_disconnected():
                    task.cancel()
                    break
                try:
                    event, payload = await asyncio.wait_for(queue.get(), timeout=1.0)
                except asyncio.TimeoutError:
                    continue
                if event == "__done__":
                    yield _sse("done", {})
                    break
                yield _sse(event, payload)
        finally:
            if not task.done():
                task.cancel()
            # Count the run only if it actually finished and quota applies.
            if run_succeeded["ok"] and not user.is_admin:
                try:
                    await increment_runs_used(user.id)
                except Exception:
                    pass

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.get("/arena/runs")
async def list_runs(user: CurrentUser = Depends(get_current_user)):
    # Admins can see everything; normal users only their own runs.
    client_id = None if user.is_admin else user.id
    return {"runs": list_snapshots(client_id=client_id)}


@app.get("/arena/runs/{run_id}")
async def get_run(run_id: str, user: CurrentUser = Depends(get_current_user)):
    try:
        snapshot = load_snapshot(run_id)
    except FileNotFoundError:
        raise HTTPException(404, "run not found")
    if not user.is_admin and snapshot.get("client_id") != user.id:
        raise HTTPException(403, "forbidden")
    return snapshot


@app.post("/arena/upload")
async def upload_doc(
    file: UploadFile = File(...),
    doc_type: str = Form("project_case"),
    title: Optional[str] = Form(None),
    user: CurrentUser = Depends(get_current_user),
):
    raw = await file.read()
    result = ingest_document(
        raw_bytes=raw,
        filename=file.filename or "upload",
        client_id=user.id,
        title=title or (file.filename or "upload"),
        doc_type=doc_type,
    )
    if not result["ok"]:
        raise HTTPException(400, result["error"])
    reindex = reindex_async_safe()
    return JSONResponse({"ingest": result, "reindex": reindex})
