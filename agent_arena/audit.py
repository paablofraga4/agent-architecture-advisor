"""Reproducible audit trail.

Every arena run produces an immutable snapshot saved to data/runs/<run_id>.json
that contains everything needed to re-execute the run 6 months later:

- prompts_hash: SHA256 of the prompt-generation modules
- kb_hash:      SHA256 of every file in the knowledge base
- model + seed + temperature
- timestamp + duration
- full AgentArenaResult (user idea, contexts, proposals, verdict, citations)
- signature: SHA256 over everything above

A reviewer can later open the snapshot and verify the run was deterministic
and reproducible against the same KB + prompts + model.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .schemas import AgentArenaResult


REPO_ROOT = Path(__file__).resolve().parent.parent
RUNS_DIR = REPO_ROOT / "data" / "runs"
KB_DIR = REPO_ROOT / "knowledge_base"
PROMPT_FILES = [
    REPO_ROOT / "agent_arena" / "prompts.py",
    REPO_ROOT / "agent_arena" / "diagram.py",
    REPO_ROOT / "agent_arena" / "planner.py",
    REPO_ROOT / "agent_arena" / "cost_estimator.py",
]


def _sha256_of_path(path: Path) -> str:
    h = hashlib.sha256()
    if path.is_file():
        h.update(path.read_bytes())
    elif path.is_dir():
        # Stable ordering for deterministic hash
        for f in sorted(path.rglob("*")):
            if not f.is_file():
                continue
            # Skip generated / cache
            if any(p in f.parts for p in ("__pycache__", ".pytest_cache", "scraper_cache")):
                continue
            h.update(str(f.relative_to(path)).encode("utf-8"))
            h.update(b"\0")
            h.update(f.read_bytes())
            h.update(b"\0")
    return h.hexdigest()


def compute_kb_hash() -> str:
    """Hash of every file in knowledge_base/."""
    if not KB_DIR.exists():
        return "no-kb"
    return _sha256_of_path(KB_DIR)


def compute_prompts_hash() -> str:
    """Hash of the prompt-generation modules."""
    h = hashlib.sha256()
    for f in PROMPT_FILES:
        if f.exists():
            h.update(f.name.encode("utf-8"))
            h.update(b"\0")
            h.update(f.read_bytes())
            h.update(b"\0")
    return h.hexdigest()


def new_run_id() -> str:
    """Sortable + unique. Format: YYYYMMDD-HHMMSS-<8 hex>."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"{ts}-{uuid.uuid4().hex[:8]}"


def build_snapshot(
    *,
    run_id: str,
    user_idea: str,
    model: str,
    seed: int,
    temperature: float,
    started_at: float,
    finished_at: float,
    client_id: str,
    result: AgentArenaResult,
) -> dict[str, Any]:
    """Assemble the immutable record (signature added in save_snapshot)."""
    kb_hash = compute_kb_hash()
    prompts_hash = compute_prompts_hash()

    record = {
        "schema_version": 1,
        "run_id": run_id,
        "client_id": client_id,
        "timestamp_utc": datetime.fromtimestamp(started_at, timezone.utc).isoformat(),
        "duration_seconds": round(finished_at - started_at, 2),
        "user_idea": user_idea,
        "execution": {
            "model": model,
            "seed": seed,
            "temperature": temperature,
            "kb_hash": kb_hash,
            "prompts_hash": prompts_hash,
        },
        "verdict": result.verdict.model_dump() if result.verdict else None,
        "validation": {
            "azure_valid": result.azure_validation.valid,
            "azure_citations": result.azure_validation.cited_ids,
            "aws_valid": result.aws_validation.valid,
            "aws_citations": result.aws_validation.cited_ids,
            "gcp_valid": result.gcp_validation.valid if result.gcp_validation else None,
            "gcp_citations": result.gcp_validation.cited_ids if result.gcp_validation else [],
            "rewrite_counts": result.rewrite_counts,
        },
        "result_summary": {
            "project_summary": result.context_pack.planner_output.project_summary,
            "project_type": result.context_pack.planner_output.project_type,
            "required_capabilities": result.context_pack.planner_output.required_capabilities,
            "explicit_cloud_preferences": result.context_pack.planner_output.explicit_cloud_preferences,
            "azure_contexts": len(result.context_pack.azure_contexts),
            "aws_contexts": len(result.context_pack.aws_contexts),
            "gcp_contexts": len(result.context_pack.gcp_contexts),
            "neutral_contexts": len(result.context_pack.neutral_contexts),
        },
        "final_architecture_proposal": result.final_architecture_proposal,
        "mermaid_diagram": result.mermaid_diagram,
    }
    return record


def save_snapshot(record: dict[str, Any]) -> Path:
    """Sign and persist. Returns the path to the saved JSON."""
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    # Canonical JSON (sorted keys) → stable signature
    payload = json.dumps(record, sort_keys=True, ensure_ascii=False).encode("utf-8")
    signature = hashlib.sha256(payload).hexdigest()
    record_signed = {**record, "signature_sha256": signature}
    path = RUNS_DIR / f"{record['run_id']}.json"
    path.write_text(
        json.dumps(record_signed, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return path


def load_snapshot(run_id: str) -> dict[str, Any]:
    path = RUNS_DIR / f"{run_id}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def verify_snapshot(record: dict[str, Any]) -> bool:
    """Recompute signature and compare. Returns True if the record is intact."""
    sig = record.get("signature_sha256")
    if not sig:
        return False
    body = {k: v for k, v in record.items() if k != "signature_sha256"}
    payload = json.dumps(body, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest() == sig


def list_snapshots(client_id: str | None = None) -> list[dict[str, Any]]:
    """Return summarized metadata of all stored runs, optionally filtered by client."""
    if not RUNS_DIR.exists():
        return []
    out = []
    for path in sorted(RUNS_DIR.glob("*.json")):
        try:
            rec = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if client_id is not None and rec.get("client_id") != client_id:
            continue
        out.append({
            "run_id": rec.get("run_id"),
            "client_id": rec.get("client_id"),
            "timestamp_utc": rec.get("timestamp_utc"),
            "project_summary": (rec.get("result_summary") or {}).get("project_summary"),
            "verdict_winner": (rec.get("verdict") or {}).get("winner"),
            "verdict_confidence": (rec.get("verdict") or {}).get("confidence"),
        })
    return out
