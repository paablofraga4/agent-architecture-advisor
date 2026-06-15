import os
from pathlib import Path

BASE_DIR = Path(os.getenv("AGENT_ARENA_BASE_DIR", Path.cwd()))
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "agent_arena_knowledge_base")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
# If the Qdrant server can't be reached, fall back to embedded mode (no Docker).
QDRANT_LOCAL_PATH = os.getenv(
    "QDRANT_LOCAL_PATH",
    str(BASE_DIR / "data" / "qdrant_local"),
)
QDRANT_FORCE_LOCAL = os.getenv("QDRANT_FORCE_LOCAL", "false").lower() == "true"
DEFAULT_MODEL = os.getenv("AGENT_ARENA_MODEL", "gpt-4o-mini")

# Reasoning-heavy steps default to a stronger model. The architecture proposals,
# the judge, the specialists, the adversarial reviewer and the final synthesis
# read much more like a senior engineer on gpt-4o; the cheaper, more mechanical
# steps (planner extraction, cost table, diagram syntax) stay on the default.
REASONING_MODEL = os.getenv("AGENT_ARENA_REASONING_MODEL", "gpt-4o")

# Per-agent model overrides
PLANNER_MODEL = os.getenv("AGENT_ARENA_PLANNER_MODEL", DEFAULT_MODEL)
AZURE_AGENT_MODEL = os.getenv("AGENT_ARENA_AZURE_MODEL", REASONING_MODEL)
AWS_AGENT_MODEL = os.getenv("AGENT_ARENA_AWS_MODEL", REASONING_MODEL)
GCP_AGENT_MODEL = os.getenv("AGENT_ARENA_GCP_MODEL", REASONING_MODEL)
JUDGE_MODEL = os.getenv("AGENT_ARENA_JUDGE_MODEL", REASONING_MODEL)
FINAL_MODEL = os.getenv("AGENT_ARENA_FINAL_MODEL", REASONING_MODEL)
REVIEW_MODEL = os.getenv("AGENT_ARENA_REVIEW_MODEL", REASONING_MODEL)
COST_MODEL = os.getenv("AGENT_ARENA_COST_MODEL", DEFAULT_MODEL)
DIAGRAM_MODEL = os.getenv("AGENT_ARENA_DIAGRAM_MODEL", DEFAULT_MODEL)

# Reranker configuration
RERANKER_ENABLED = os.getenv("AGENT_ARENA_RERANKER_ENABLED", "false").lower() == "true"
RERANKER_MODEL_NAME = os.getenv("AGENT_ARENA_RERANKER_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")
RERANKER_TOP_K = int(os.getenv("AGENT_ARENA_RERANKER_TOP_K", "5"))

# Retry limits for citation rewrite loops
MAX_REWRITE_RETRIES = int(os.getenv("AGENT_ARENA_MAX_REWRITE_RETRIES", "2"))

# Interactive planner: ask user for clarification when missing_information is non-empty
INTERACTIVE_PLANNER = os.getenv("AGENT_ARENA_INTERACTIVE_PLANNER", "true").lower() == "true"

# GCP support toggle
GCP_ENABLED = os.getenv("AGENT_ARENA_GCP_ENABLED", "true").lower() == "true"
