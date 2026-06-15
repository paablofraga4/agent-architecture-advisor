"""
Knowledge base document generator.

Takes scraped documentation pages and generates structured markdown documents
for the knowledge base. Every fact is sourced from official documentation.

The output documents include:
- Source URLs for traceability
- Fetch timestamps
- Only content extracted from official pages — no invented data
"""
from __future__ import annotations

import re
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def _clean_markdown(text: str) -> str:
    """Clean up markdown from conversion artifacts."""
    # Remove common doc-site UI noise
    noise_patterns = [
        r"^Table of contents\s*$",
        r"^Exit editor mode\s*$",
        r"^Ask Learn\s*$",
        r"^Reading mode\s*$",
        r"^Copy Markdown\s*$",
        r"^Print\s*$",
        r"^Feedback\s*$",
        r"^Summarize this article for me\s*$",
        r"^Add to plan\s*$",
        r"^\[Read in English\].*$",
        r"^\[Edit\]\(https://github\.com/MicrosoftDocs.*$",
        r"^Access to this page requires authorization\..*$",
        r"^Add\s*$",
        r"^---\s*$",
    ]
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        if any(re.match(p, line.strip(), re.IGNORECASE) for p in noise_patterns):
            continue
        cleaned_lines.append(line)
    text = "\n".join(cleaned_lines)
    # Remove excessive blank lines
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    # Remove trailing whitespace per line
    text = "\n".join(line.rstrip() for line in text.splitlines())
    # Remove excessive heading markers with no content
    text = re.sub(r"^#+\s*$", "", text, flags=re.MULTILINE)
    return text.strip()


def _truncate_section(text: str, max_chars: int = 3000) -> str:
    """Truncate a section to max chars, cutting at last complete sentence."""
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars]
    # Try to cut at last sentence end
    last_period = truncated.rfind(". ")
    if last_period > max_chars // 2:
        return truncated[:last_period + 1]
    # Try newline
    last_newline = truncated.rfind("\n")
    if last_newline > max_chars // 2:
        return truncated[:last_newline]
    return truncated + "..."


def _extract_section_by_keywords(markdown: str, keywords: list[str], max_chars: int = 3000) -> str:
    """Extract a section from markdown by heading keywords."""
    lines = markdown.splitlines()
    capturing = False
    captured = []
    capture_level = 0

    for line in lines:
        heading_match = re.match(r"^(#{1,4})\s+(.*)", line)
        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).lower().strip()
            if any(kw in title for kw in keywords):
                capturing = True
                capture_level = level
                captured.append(line)
                continue
            elif capturing and level <= capture_level:
                break

        if capturing:
            captured.append(line)

    result = "\n".join(captured).strip()
    return _truncate_section(result, max_chars)


def generate_service_document(
    service_key: str,
    service_config: dict,
    fetched_pages: dict,
    output_dir: Path,
) -> Optional[Path]:
    """
    Generate a structured knowledge base document from fetched pages.

    The document structure:
    - Metadata header (provider, type, sources, timestamp)
    - Overview (from overview page)
    - Key Features
    - Limits and Quotas (from limits page — CRITICAL for credibility)
    - Pricing (from pricing page — CRITICAL for credibility)
    - Integration Points
    - When to Use / When NOT to Use

    Returns the path to the generated file, or None if insufficient data.
    """
    provider = service_config["provider"]
    service_name = service_config["name"]
    category = service_config["category"]
    tags = service_config.get("tags", [])

    # Check we have at least the overview
    overview_page = fetched_pages.get("overview", {})
    if overview_page.get("error") or not overview_page.get("markdown"):
        print(f"    SKIP {service_key}: no overview content")
        return None

    # Collect source URLs
    source_urls = []
    for page_type, page in fetched_pages.items():
        if not page.get("error"):
            source_urls.append(f"- [{page_type}]({page['url']})")

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Build document sections
    sections = []

    # Header
    sections.append(f"# Service: {service_name}")
    sections.append("")
    sections.append(f"**Provider:** {provider}")
    sections.append(f"**Document type:** service_reference")
    sections.append(f"**Category:** {category}")
    sections.append(f"**Tags:** {', '.join(tags)}")
    sections.append(f"**Last updated:** {timestamp}")
    sections.append(f"**Sources:**")
    sections.extend(source_urls)
    sections.append("")

    # Overview
    overview_md = _clean_markdown(overview_page.get("markdown", ""))
    if overview_md:
        sections.append("## Overview")
        sections.append("")
        overview_text = _truncate_section(overview_md, 2500)
        sections.append(overview_text)
        sections.append("")

    # Key features — try to extract from overview
    features_text = _extract_section_by_keywords(
        overview_md, ["feature", "capabilities", "key benefits", "what is", "benefits"]
    )
    if features_text:
        sections.append("## Key Features")
        sections.append("")
        sections.append(features_text)
        sections.append("")

    # Limits and Quotas — from limits page
    limits_page = fetched_pages.get("limits") or fetched_pages.get("quotas")
    if limits_page and not limits_page.get("error"):
        limits_md = _clean_markdown(limits_page.get("markdown", ""))
        if limits_md:
            sections.append("## Limits and Quotas")
            sections.append("")
            sections.append(f"*Source: [{limits_page['url']}]({limits_page['url']})*")
            sections.append("")
            limits_text = _truncate_section(limits_md, 3000)
            sections.append(limits_text)
            sections.append("")

    # Pricing — from pricing page
    pricing_page = fetched_pages.get("pricing")
    if pricing_page and not pricing_page.get("error"):
        pricing_md = _clean_markdown(pricing_page.get("markdown", ""))
        if pricing_md:
            sections.append("## Pricing")
            sections.append("")
            sections.append(f"*Source: [{pricing_page['url']}]({pricing_page['url']})*")
            sections.append("")
            pricing_text = _truncate_section(pricing_md, 3000)
            sections.append(pricing_text)
            sections.append("")

    # Additional pages (models, vector_search, agents, etc.)
    standard_pages = {"overview", "limits", "quotas", "pricing"}
    for page_type, page in fetched_pages.items():
        if page_type in standard_pages:
            continue
        if page.get("error") or not page.get("markdown"):
            continue
        page_md = _clean_markdown(page.get("markdown", ""))
        if page_md:
            section_title = page_type.replace("_", " ").title()
            sections.append(f"## {section_title}")
            sections.append("")
            sections.append(f"*Source: [{page['url']}]({page['url']})*")
            sections.append("")
            sections.append(_truncate_section(page_md, 2000))
            sections.append("")

    # Write file
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{service_key}.md"
    content = "\n".join(sections)
    output_path.write_text(content, encoding="utf-8")

    line_count = content.count("\n") + 1
    print(f"    Generated: {output_path.name} ({line_count} lines)")
    return output_path


def generate_source_manifest(
    all_fetched: dict,
    output_path: Path,
):
    """
    Generate a manifest file listing all sources used.
    This provides full traceability for auditing.
    """
    lines = [
        "# Knowledge Base Source Manifest",
        "",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "Every document in the knowledge base is derived from the official sources listed below.",
        "No content is invented or hallucinated — all facts are traceable to these URLs.",
        "",
    ]

    for service_key, pages in sorted(all_fetched.items()):
        lines.append(f"## {service_key}")
        lines.append("")
        for page_type, page in pages.items():
            status = "OK" if not page.get("error") else f"ERROR: {page.get('error')}"
            lines.append(f"- **{page_type}**: [{page['url']}]({page['url']}) — {status}")
        lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Source manifest: {output_path}")
