"""
Build the knowledge base from official cloud documentation.

This script:
1. Fetches official documentation pages for each service in the catalog
2. Extracts and structures the content into markdown documents
3. Places them in knowledge_base/cloud_services/{provider}/
4. Generates a source manifest for full traceability
5. Optionally runs ingestion + Qdrant indexing

Usage:
    python build_knowledge_base.py                          # full build
    python build_knowledge_base.py --provider azure         # only Azure
    python build_knowledge_base.py --provider gcp --no-cache  # GCP, skip cache
    python build_knowledge_base.py --service aws_bedrock    # single service
    python build_knowledge_base.py --index                  # build + reindex Qdrant
    python build_knowledge_base.py --list                   # list available services
    python build_knowledge_base.py --dry-run                # fetch only, don't write docs

The knowledge base is structured for exportability:

    knowledge_base/
      cloud_services/     <- PUBLIC: scraped from official docs (this script generates these)
      patterns/           <- PUBLIC: curated architectural patterns (maintained manually)
      decisions/          <- PUBLIC: general decision records (maintained manually)
      cost_references/    <- PUBLIC: pricing data (this script can update these)
      project_cases/      <- PRIVATE per company: add your own project experiences
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
KB_DIR = BASE_DIR / "knowledge_base"

# Ensure imports work
sys.path.insert(0, str(BASE_DIR))

from knowledge_builder.catalog import SERVICE_CATALOG, get_services_by_provider
from knowledge_builder.scraper import fetch_service_pages, clear_cache
from knowledge_builder.generator import generate_service_document, generate_source_manifest


def list_services():
    """Print all services in the catalog."""
    for provider in ["azure", "aws", "gcp"]:
        services = get_services_by_provider(provider)
        print(f"\n  {provider.upper()} ({len(services)} services):")
        for key, svc in sorted(services.items()):
            urls = len(svc["urls"])
            print(f"    {key:<35} {svc['name']:<40} ({urls} pages)")
    print(f"\n  Total: {len(SERVICE_CATALOG)} services")


def build_service(
    service_key: str,
    service_config: dict,
    use_cache: bool = True,
    dry_run: bool = False,
) -> dict:
    """Fetch and generate docs for a single service. Returns fetched pages."""
    provider = service_config["provider"]
    print(f"\n  [{provider.upper()}] {service_config['name']}")

    # Fetch
    fetched = fetch_service_pages(service_config, use_cache=use_cache)

    if dry_run:
        for page_type, page in fetched.items():
            status = "OK" if not page.get("error") else page["error"]
            chars = len(page.get("markdown", ""))
            print(f"    {page_type}: {status} ({chars} chars)")
        return fetched

    # Generate
    output_dir = KB_DIR / "cloud_services" / provider
    generate_service_document(
        service_key=service_key,
        service_config=service_config,
        fetched_pages=fetched,
        output_dir=output_dir,
    )

    return fetched


def main():
    parser = argparse.ArgumentParser(
        description="Build knowledge base from official cloud documentation"
    )
    parser.add_argument("--provider", choices=["azure", "aws", "gcp"],
                        help="Only build for a specific provider")
    parser.add_argument("--service", help="Only build a specific service (e.g. aws_bedrock)")
    parser.add_argument("--no-cache", action="store_true",
                        help="Ignore cached pages, fetch fresh from web")
    parser.add_argument("--clear-cache", action="store_true",
                        help="Clear the scraper cache and exit")
    parser.add_argument("--dry-run", action="store_true",
                        help="Fetch pages but don't generate documents")
    parser.add_argument("--index", action="store_true",
                        help="Run ingest_and_index.py after building")
    parser.add_argument("--list", action="store_true",
                        help="List all services in the catalog")
    args = parser.parse_args()

    if args.clear_cache:
        clear_cache()
        return

    if args.list:
        list_services()
        return

    print("=" * 80)
    print("AGENT ARENA — Knowledge Base Builder")
    print("=" * 80)
    print(f"\nSource: Official cloud documentation (Azure, AWS, GCP)")
    print(f"Output: {KB_DIR}/cloud_services/")
    print(f"Cache:  {'DISABLED' if args.no_cache else 'ENABLED (7 day TTL)'}")

    use_cache = not args.no_cache
    t0 = time.time()

    # Determine which services to build
    if args.service:
        if args.service not in SERVICE_CATALOG:
            print(f"\nERROR: Unknown service '{args.service}'")
            print("Use --list to see available services")
            sys.exit(1)
        services = {args.service: SERVICE_CATALOG[args.service]}
    elif args.provider:
        services = get_services_by_provider(args.provider)
    else:
        services = SERVICE_CATALOG

    print(f"\nServices to process: {len(services)}")
    total_urls = sum(len(s["urls"]) for s in services.values())
    print(f"Total pages to fetch: {total_urls}")

    if not args.dry_run:
        estimated_time = total_urls * 2  # ~2s per page with caching
        print(f"Estimated time: ~{estimated_time}s (less if cached)")

    # Build
    all_fetched = {}
    success_count = 0
    error_count = 0

    for service_key, service_config in sorted(services.items()):
        try:
            fetched = build_service(
                service_key=service_key,
                service_config=service_config,
                use_cache=use_cache,
                dry_run=args.dry_run,
            )
            all_fetched[service_key] = fetched
            success_count += 1
        except Exception as e:
            print(f"    ERROR: {e}")
            error_count += 1

    # Generate source manifest
    if not args.dry_run and all_fetched:
        manifest_path = KB_DIR / "_sources" / "source_manifest.md"
        generate_source_manifest(all_fetched, manifest_path)

    elapsed = time.time() - t0
    print(f"\n{'=' * 80}")
    print(f"DONE in {elapsed:.1f}s — {success_count} OK, {error_count} errors")
    print(f"{'=' * 80}")

    # Optionally reindex
    if args.index and not args.dry_run:
        print("\nRunning ingestion and indexing...")
        import subprocess
        result = subprocess.run(
            [sys.executable, str(BASE_DIR / "ingest_and_index.py")],
            cwd=str(BASE_DIR),
        )
        if result.returncode != 0:
            print("WARNING: Indexing failed")
            sys.exit(1)


if __name__ == "__main__":
    main()
