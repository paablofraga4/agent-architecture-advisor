"""
Automated knowledge base ingestion and Qdrant indexing.

Usage:
    python ingest_and_index.py                     # full rebuild
    python ingest_and_index.py --dry-run            # preview without writing to Qdrant
    python ingest_and_index.py --collection my_col  # custom collection name
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, FieldCondition, Filter, MatchValue, PointStruct, VectorParams


def _make_client(host: str, port: int) -> QdrantClient:
    """Connect to the Qdrant server, or fall back to embedded local mode."""
    import os
    if os.getenv("QDRANT_FORCE_LOCAL", "false").lower() != "true":
        try:
            c = QdrantClient(host=host, port=port, timeout=2)
            c.get_collections()
            print(f"[INFO] Using Qdrant server at {host}:{port}")
            return c
        except Exception as exc:
            print(f"[INFO] Qdrant server unreachable ({type(exc).__name__}). Falling back to embedded mode.")
    local = os.getenv(
        "QDRANT_LOCAL_PATH",
        str(Path(__file__).resolve().parent / "data" / "qdrant_local"),
    )
    Path(local).mkdir(parents=True, exist_ok=True)
    print(f"[INFO] Using embedded Qdrant at {local}")
    return QdrantClient(path=local)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

DEFAULT_COLLECTION = "agent_arena_knowledge_base"
DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_QDRANT_HOST = "localhost"
DEFAULT_QDRANT_PORT = 6333

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


# ---------------------------------------------------------------------------
# Step 1: Discover and read markdown files
# ---------------------------------------------------------------------------
def infer_metadata_from_path(file_path: Path) -> Dict:
    parts = [part.lower() for part in file_path.parts]
    filename = file_path.stem.lower()

    provider = "unknown"
    document_type = "unknown"

    # --- Provider detection ---
    if "azure" in parts or filename.startswith("azure_"):
        provider = "azure"
    elif (
        "aws" in parts
        or filename.startswith("aws_")
        or filename.startswith("amazon_")
        or "bedrock" in filename
    ):
        provider = "aws"
    elif "gcp" in parts or filename.startswith("gcp_"):
        provider = "gcp"
    else:
        provider = "neutral"

    # --- Document type detection ---
    if "cloud_services" in parts:
        document_type = "service_reference"

    elif "patterns" in parts:
        document_type = "architecture_pattern"
        # Patterns are always neutral unless explicitly provider-scoped
        if provider == "unknown":
            provider = "neutral"

    elif "project_cases" in parts:
        document_type = "project_case"
        if provider == "unknown":
            # Try to infer from filename
            if "azure" in filename:
                provider = "azure"
            elif "aws" in filename:
                provider = "aws"
            elif "gcp" in filename:
                provider = "gcp"
            else:
                provider = "neutral"

    elif "decisions" in parts:
        document_type = "decision_record"
        if provider == "unknown":
            if "azure" in filename or "cosmos" in filename:
                provider = "azure"
            elif (
                "aws" in filename
                or "bedrock" in filename
                or "textract" in filename
                or "lambda" in filename
                or "ecs" in filename
                or "opensearch" in filename
                or "step_functions" in filename
                or "dynamodb" in filename
                or "sagemaker" in filename
            ):
                provider = "aws"
            elif "gcp" in filename or "vertex" in filename or "cloud_run" in filename:
                provider = "gcp"
            elif "qdrant" in filename:
                provider = "neutral"

    elif "cost_references" in parts:
        document_type = "cost_reference"
        if "azure" in filename:
            provider = "azure"
        elif "aws" in filename:
            provider = "aws"
        elif "gcp" in filename:
            provider = "gcp"
        else:
            provider = "neutral"

    elif "company_context" in parts:
        document_type = "company_context"
        provider = "neutral"

    # Fallback for cloud_services subfolders
    if document_type == "unknown":
        if "azure" in parts or "aws" in parts or "gcp" in parts:
            document_type = "cloud_reference"

    # Final fallback
    if provider == "unknown":
        provider = "neutral"
    if document_type == "unknown":
        document_type = "cloud_reference"

    return {
        "source_file": file_path.name,
        "source_path": str(file_path),
        "provider": provider,
        "document_type": document_type,
    }


def extract_document_title(text: str, file_path: Path) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line.replace("# ", "").strip()
    return file_path.stem.replace("_", " ").title()


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def read_markdown_file(file_path: Path) -> Dict:
    text = file_path.read_text(encoding="utf-8")
    metadata = infer_metadata_from_path(file_path)
    return {
        **metadata,
        "document_title": extract_document_title(text, file_path),
        "text": text,
        "clean_text": clean_text(text),
        "num_characters": len(text),
    }


# ---------------------------------------------------------------------------
# Step 2: Parse markdown into sections and chunk
# ---------------------------------------------------------------------------
def parse_markdown_sections(text: str) -> List[Dict]:
    lines = text.splitlines()
    sections = []
    current_heading_stack: list[str] = []
    current_content: list[str] = []
    current_section_title = "Document Introduction"
    current_level = 0

    def flush_section():
        if current_content:
            section_text = "\n".join(current_content).strip()
            if section_text:
                sections.append({
                    "section_title": current_section_title,
                    "section_path": " > ".join(current_heading_stack) if current_heading_stack else current_section_title,
                    "section_level": current_level,
                    "section_text": section_text,
                })

    for line in lines:
        heading_match = re.match(r"^(#{1,6})\s+(.*)", line)
        if heading_match:
            flush_section()
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            while current_heading_stack and len(current_heading_stack) >= level:
                current_heading_stack.pop()
            current_heading_stack.append(title)
            current_section_title = title
            current_level = level
            current_content = [line]
        else:
            current_content.append(line)

    flush_section()
    return sections


def split_long_text(text: str, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> List[str]:
    if len(text) <= chunk_size:
        return [text.strip()]
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - chunk_overlap
    return chunks


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text)
    return text.strip("_")


def build_contextualized_text(
    document_title: str,
    provider: str,
    document_type: str,
    source_file: str,
    section_path: str,
    chunk_text: str,
) -> str:
    return f"""Document: {document_title}
Provider: {provider}
Document type: {document_type}
Source file: {source_file}
Section: {section_path}

{chunk_text}""".strip()


# ---------------------------------------------------------------------------
# Step 3: Build chunks dataframe
# ---------------------------------------------------------------------------
def build_chunks(df_docs: pd.DataFrame) -> pd.DataFrame:
    chunk_rows = []
    context_counter = 1

    for _, doc in df_docs.iterrows():
        sections = parse_markdown_sections(doc["clean_text"])
        for section_idx, section in enumerate(sections):
            section_chunks = split_long_text(section["section_text"])
            for chunk_idx, chunk_text in enumerate(section_chunks):
                section_slug = slugify(section["section_path"])
                context_id = f"CTX-{context_counter:04d}"
                context_counter += 1

                chunk_id = (
                    f"{doc['provider']}::"
                    f"{doc['document_type']}::"
                    f"{doc['source_file']}::"
                    f"{section_slug}::"
                    f"chunk_{chunk_idx}"
                )

                contextualized_chunk_text = build_contextualized_text(
                    document_title=doc["document_title"],
                    provider=doc["provider"],
                    document_type=doc["document_type"],
                    source_file=doc["source_file"],
                    section_path=section["section_path"],
                    chunk_text=chunk_text,
                )

                chunk_rows.append({
                    "context_id": context_id,
                    "chunk_id": chunk_id,
                    "source_file": doc["source_file"],
                    "source_path": doc["source_path"],
                    "document_title": doc["document_title"],
                    "provider": doc["provider"],
                    "document_type": doc["document_type"],
                    "section_title": section["section_title"],
                    "section_path": section["section_path"],
                    "section_level": section["section_level"],
                    "section_index": section_idx,
                    "chunk_index": chunk_idx,
                    "chunk_text": chunk_text,
                    "contextualized_chunk_text": contextualized_chunk_text,
                    "chunk_num_characters": len(chunk_text),
                    "contextualized_num_characters": len(contextualized_chunk_text),
                })

    return pd.DataFrame(chunk_rows)


# ---------------------------------------------------------------------------
# Step 4: Embed chunks
# ---------------------------------------------------------------------------
def embed_chunks(df_chunks: pd.DataFrame, model_name: str) -> np.ndarray:
    print(f"Loading embedding model: {model_name}")
    model = SentenceTransformer(model_name)
    dim = model.get_sentence_embedding_dimension()
    print(f"Embedding dimension: {dim}")

    texts = df_chunks["contextualized_chunk_text"].tolist()
    print(f"Embedding {len(texts)} chunks...")
    t0 = time.time()
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
    print(f"Embedding done in {time.time() - t0:.1f}s — shape: {embeddings.shape}")
    return embeddings


# ---------------------------------------------------------------------------
# Step 5: Index into Qdrant
# ---------------------------------------------------------------------------
PAYLOAD_COLUMNS = [
    "context_id", "chunk_id", "source_file", "source_path",
    "document_title", "provider", "document_type",
    "section_title", "section_path", "section_level",
    "section_index", "chunk_index", "chunk_text",
    "contextualized_chunk_text",
]


def index_to_qdrant(
    df_chunks: pd.DataFrame,
    embeddings: np.ndarray,
    collection_name: str,
    host: str,
    port: int,
):
    print(f"Connecting to Qdrant at {host}:{port}")
    client = _make_client(host, port)

    embedding_dim = embeddings.shape[1]

    # Recreate collection
    if client.collection_exists(collection_name):
        print(f"Deleting existing collection '{collection_name}'")
        client.delete_collection(collection_name)

    print(f"Creating collection '{collection_name}' (dim={embedding_dim}, cosine)")
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=embedding_dim, distance=Distance.COSINE),
    )

    # Build points
    points = []
    for idx, row in df_chunks.reset_index(drop=True).iterrows():
        payload = {
            col: row[col]
            for col in PAYLOAD_COLUMNS
            if col in row and pd.notna(row[col])
        }
        points.append(PointStruct(
            id=idx,
            vector=embeddings[idx].tolist(),
            payload=payload,
        ))

    # Upsert in batches of 100
    batch_size = 100
    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        client.upsert(collection_name=collection_name, points=batch)
        print(f"  Upserted {min(i + batch_size, len(points))}/{len(points)} points")

    info = client.get_collection(collection_name)
    print(f"Collection '{collection_name}': {info.points_count} points indexed")


# ---------------------------------------------------------------------------
# Step 6: Verify
# ---------------------------------------------------------------------------
def verify_index(collection_name: str, host: str, port: int, model_name: str):
    client = _make_client(host, port)
    model = SentenceTransformer(model_name)

    for provider in ["azure", "aws", "gcp", "neutral"]:
        query_vector = model.encode(
            f"{provider} architecture services",
            convert_to_numpy=True,
            normalize_embeddings=True,
        ).tolist()

        search_filter = Filter(
            must=[FieldCondition(key="provider", match=MatchValue(value=provider))]
        )

        response = client.query_points(
            collection_name=collection_name,
            query=query_vector,
            query_filter=search_filter,
            limit=3,
            with_payload=True,
            with_vectors=False,
        )

        print(f"\n  [{provider.upper()}] {len(response.points)} results:")
        for p in response.points:
            print(f"    {p.payload.get('context_id')} | {p.payload.get('document_type')} | {p.payload.get('source_file')} | score={p.score:.4f}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Ingest knowledge base and index into Qdrant")
    parser.add_argument("--collection", default=DEFAULT_COLLECTION, help="Qdrant collection name")
    parser.add_argument("--embedding-model", default=DEFAULT_EMBEDDING_MODEL, help="SentenceTransformer model")
    parser.add_argument("--qdrant-host", default=DEFAULT_QDRANT_HOST)
    parser.add_argument("--qdrant-port", type=int, default=DEFAULT_QDRANT_PORT)
    parser.add_argument("--dry-run", action="store_true", help="Process and embed but don't write to Qdrant")
    parser.add_argument("--skip-save", action="store_true", help="Don't save parquet files")
    args = parser.parse_args()

    print("=" * 80)
    print("AGENT ARENA — Knowledge Base Ingestion & Indexing")
    print("=" * 80)

    # 1. Discover files
    md_files = sorted(
        f for f in KNOWLEDGE_BASE_DIR.rglob("*.md")
        if f.name != "_template.md"
    )
    print(f"\n[1/6] Found {len(md_files)} markdown files in {KNOWLEDGE_BASE_DIR}")

    if not md_files:
        print("ERROR: No markdown files found. Check KNOWLEDGE_BASE_DIR.")
        sys.exit(1)

    # 2. Read and parse
    print(f"\n[2/6] Reading and parsing documents...")
    documents = [read_markdown_file(f) for f in md_files]
    df_docs = pd.DataFrame(documents)

    # Summary by provider and type
    summary = df_docs.groupby(["provider", "document_type"]).size().reset_index(name="count")
    print(f"\n  Documents by provider/type:")
    for _, row in summary.iterrows():
        print(f"    {row['provider']:>10} | {row['document_type']:<25} | {row['count']}")
    print(f"  Total documents: {len(df_docs)}")

    # 3. Build chunks
    print(f"\n[3/6] Building chunks (chunk_size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})...")
    df_chunks = build_chunks(df_docs)

    chunk_summary = df_chunks.groupby(["provider", "document_type"]).size().reset_index(name="count")
    print(f"\n  Chunks by provider/type:")
    for _, row in chunk_summary.iterrows():
        print(f"    {row['provider']:>10} | {row['document_type']:<25} | {row['count']}")
    print(f"  Total chunks: {len(df_chunks)}")

    # 4. Save parquet
    if not args.skip_save:
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        docs_path = PROCESSED_DIR / "knowledge_base_docs.parquet"
        chunks_path = PROCESSED_DIR / "knowledge_base_chunks.parquet"
        df_docs.to_parquet(docs_path, index=False)
        df_chunks.to_parquet(chunks_path, index=False)
        print(f"\n[4/6] Saved parquet files:")
        print(f"  Docs:   {docs_path}")
        print(f"  Chunks: {chunks_path}")
    else:
        print(f"\n[4/6] Skipping parquet save (--skip-save)")

    # 5. Embed
    print(f"\n[5/6] Embedding chunks...")
    embeddings = embed_chunks(df_chunks, args.embedding_model)

    # 6. Index
    if args.dry_run:
        print(f"\n[6/6] DRY RUN — skipping Qdrant indexing")
        print(f"  Would index {len(df_chunks)} points into '{args.collection}'")
    else:
        print(f"\n[6/6] Indexing into Qdrant...")
        index_to_qdrant(
            df_chunks=df_chunks,
            embeddings=embeddings,
            collection_name=args.collection,
            host=args.qdrant_host,
            port=args.qdrant_port,
        )

        print(f"\n  Verifying index...")
        verify_index(args.collection, args.qdrant_host, args.qdrant_port, args.embedding_model)

    print(f"\n{'=' * 80}")
    print("DONE")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
