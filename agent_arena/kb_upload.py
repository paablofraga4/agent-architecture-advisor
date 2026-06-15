"""Self-service KB upload for consultants.

Accepts a markdown / text / PDF document, saves it under
knowledge_base/project_cases/<client_id>/ and triggers a partial reindex
(adds just the new chunks to the Qdrant collection instead of a full
rebuild).

PDF parsing uses pypdf if available, otherwise falls back to text-only.
"""
from __future__ import annotations

import re
import time
import uuid
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_DIR = REPO_ROOT / "knowledge_base"


def _slugify(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9\-_]+", "_", text.strip())
    return text.lower()[:60] or "untitled"


def _extract_pdf_text(pdf_bytes: bytes) -> str:
    try:
        from pypdf import PdfReader
        import io
        reader = PdfReader(io.BytesIO(pdf_bytes))
        parts = []
        for i, page in enumerate(reader.pages):
            try:
                parts.append(f"\n## Page {i+1}\n\n{page.extract_text() or ''}")
            except Exception:
                continue
        return "\n".join(parts).strip()
    except ImportError:
        return "[PDF parsing unavailable — install pypdf: pip install pypdf]"
    except Exception as exc:
        return f"[PDF parse error: {exc}]"


def ingest_document(
    *,
    raw_bytes: bytes,
    filename: str,
    client_id: str,
    title: Optional[str] = None,
    doc_type: str = "project_case",
) -> dict:
    """Save the document as a markdown file under knowledge_base/<doc_type>/<client_id>/
    and return metadata. Caller is responsible for triggering reindex.

    doc_type can be:
      - "project_case"     (default) — a past project the team did
      - "company_context"  — preferences, constraints, contracts of the client
      - "decisions"        — ADRs / decision records
    """
    suffix = Path(filename).suffix.lower()
    title = title or Path(filename).stem

    if suffix in (".md", ".markdown", ".txt"):
        text = raw_bytes.decode("utf-8", errors="replace")
    elif suffix == ".pdf":
        text = _extract_pdf_text(raw_bytes)
    else:
        # Best-effort decode for unknown extensions.
        try:
            text = raw_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return {"ok": False, "error": f"Unsupported file type: {suffix}"}

    if not text.strip():
        return {"ok": False, "error": "Empty document after parsing."}

    # Compose final markdown with a frontmatter-ish header so downstream
    # ingestion can read provider/type/tags consistently.
    safe_title = _slugify(title)
    timestamp = int(time.time())
    file_id = f"{timestamp}_{safe_title}_{uuid.uuid4().hex[:6]}"
    target_dir = KB_DIR / doc_type / client_id
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / f"{file_id}.md"

    header = (
        f"# {title}\n\n"
        f"<!-- doc_type: {doc_type} -->\n"
        f"<!-- client_id: {client_id} -->\n"
        f"<!-- uploaded_at: {timestamp} -->\n"
        f"<!-- source_filename: {filename} -->\n\n"
    )
    target_path.write_text(header + text, encoding="utf-8")

    return {
        "ok": True,
        "path": str(target_path.relative_to(REPO_ROOT)),
        "doc_type": doc_type,
        "client_id": client_id,
        "title": title,
        "chars": len(text),
    }


def reindex_async_safe() -> dict:
    """Run the ingestion + Qdrant indexing in a separate process so it doesn't
    block the Chainlit event loop. Falls back to in-process if subprocess fails.
    """
    import subprocess
    import sys
    try:
        proc = subprocess.Popen(
            [sys.executable, str(REPO_ROOT / "ingest_and_index.py")],
            cwd=str(REPO_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return {"ok": True, "pid": proc.pid, "message": "Reindex launched in background. Toma ~30-90s."}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}
