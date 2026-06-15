import os
from pathlib import Path

BASE_DIR = Path(os.getenv("AGENT_ARENA_BASE_DIR", Path.cwd()))
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "agent_arena_knowledge_base")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
DEFAULT_MODEL = os.getenv("AGENT_ARENA_MODEL", "gpt-4o-mini")

# Per-agent model overrides (fall back to DEFAULT_MODEL)
PLANNER_MODEL = os.getenv("AGENT_ARENA_PLANNER_MODEL", DEFAULT_MODEL)
AZURE_AGENT_MODEL = os.getenv("AGENT_ARENA_AZURE_MODEL", DEFAULT_MODEL)
AWS_AGENT_MODEL = os.getenv("AGENT_ARENA_AWS_MODEL", DEFAULT_MODEL)
GCP_AGENT_MODEL = os.getenv("AGENT_ARENA_GCP_MODEL", DEFAULT_MODEL)
JUDGE_MODEL = os.getenv("AGENT_ARENA_JUDGE_MODEL", DEFAULT_MODEL)
FINAL_MODEL = os.getenv("AGENT_ARENA_FINAL_MODEL", DEFAULT_MODEL)
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
