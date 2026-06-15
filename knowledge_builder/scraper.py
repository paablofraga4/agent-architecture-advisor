"""
Web scraper for official cloud documentation.

Fetches pages from Microsoft Learn, AWS Docs, and GCP Docs.
Extracts clean text content preserving structure.
Every piece of data is traceable to a source URL.
"""
from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup, Tag
import markdownify

# Rate limiting: be respectful to doc sites
REQUEST_DELAY_SECONDS = 1.5
REQUEST_TIMEOUT = 30
USER_AGENT = "AgentArena-KnowledgeBuilder/1.0 (architecture-advisor; documentation-indexer)"

# Cache directory for raw fetched pages
CACHE_DIR = Path(__file__).resolve().parent.parent / "data" / "scraper_cache"


def _cache_path(url: str) -> Path:
    url_hash = hashlib.sha256(url.encode()).hexdigest()[:16]
    return CACHE_DIR / f"{url_hash}.json"


def _load_from_cache(url: str, max_age_hours: int = 24 * 7) -> Optional[dict]:
    """Load cached page if fresh enough."""
    path = _cache_path(url)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        fetched_at = datetime.fromisoformat(data["fetched_at"])
        age_hours = (datetime.now(timezone.utc) - fetched_at).total_seconds() / 3600
        if age_hours < max_age_hours:
            return data
    except Exception:
        pass
    return None


def _save_to_cache(url: str, data: dict):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = _cache_path(url)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def fetch_page(url: str, use_cache: bool = True) -> dict:
    """
    Fetch a documentation page and return structured result.

    Returns:
        {
            "url": str,
            "status": int,
            "fetched_at": str (ISO),
            "html": str (raw HTML),
            "text": str (extracted clean text),
            "markdown": str (converted to markdown),
            "title": str,
            "error": str | None,
        }
    """
    if use_cache:
        cached = _load_from_cache(url)
        if cached:
            return cached

    result = {
        "url": url,
        "status": 0,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "html": "",
        "text": "",
        "markdown": "",
        "title": "",
        "error": None,
    }

    try:
        headers = {"User-Agent": USER_AGENT}
        resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        result["status"] = resp.status_code

        if resp.status_code != 200:
            result["error"] = f"HTTP {resp.status_code}"
            return result

        result["html"] = resp.text
        soup = BeautifulSoup(resp.text, "html.parser")

        # Extract title
        title_tag = soup.find("title")
        result["title"] = title_tag.get_text(strip=True) if title_tag else ""

        # Extract main content based on doc site
        main_content = _extract_main_content(soup, url)

        if main_content:
            # Remove nav, sidebars, footers, scripts, styles
            for tag in main_content.find_all(["nav", "script", "style", "footer", "aside"]):
                tag.decompose()
            for tag in main_content.find_all(attrs={"role": ["navigation", "complementary"]}):
                tag.decompose()
            # Remove feedback sections, "was this helpful" etc.
            for tag in main_content.find_all(class_=lambda c: c and any(
                x in str(c).lower() for x in ["feedback", "rating", "survey", "cookie",
                    "action-bar", "page-actions", "toc", "breadcrumb", "metadata",
                    "ms-auth", "uhf", "share-link", "content-action"]
            )):
                tag.decompose()
            # Remove MS Learn interactive elements (table of contents, ask learn, etc.)
            for tag in main_content.find_all(id=lambda i: i and any(
                x in str(i).lower() for x in ["toc", "action", "feedback", "ask-learn"]
            )):
                tag.decompose()

            result["text"] = main_content.get_text(separator="\n", strip=True)
            result["markdown"] = markdownify.markdownify(
                str(main_content),
                heading_style="ATX",
                strip=["img", "svg", "button", "input", "form"],
            )
        else:
            # Fallback: get body text
            body = soup.find("body")
            if body:
                result["text"] = body.get_text(separator="\n", strip=True)
                result["markdown"] = result["text"]

    except requests.RequestException as e:
        result["error"] = f"Request failed: {e}"
    except Exception as e:
        result["error"] = f"Parse error: {e}"

    if use_cache and not result["error"]:
        _save_to_cache(url, result)

    time.sleep(REQUEST_DELAY_SECONDS)
    return result


def _extract_main_content(soup: BeautifulSoup, url: str) -> Optional[Tag]:
    """Extract the main content element based on the documentation site."""

    # Microsoft Learn
    if "learn.microsoft.com" in url or "microsoft.com" in url:
        # Try multiple selectors used by MS Learn
        for selector in ["main", "#main-column", ".content", "#main"]:
            el = soup.select_one(selector)
            if el:
                return el

    # AWS Docs
    if "docs.aws.amazon.com" in url:
        for selector in ["#main-content", "#main-col-body", "main", "#content"]:
            el = soup.select_one(selector)
            if el:
                return el

    # AWS Marketing/Pricing pages
    if "aws.amazon.com" in url:
        for selector in ["main", "#aws-page-content", ".lb-content-wrapper"]:
            el = soup.select_one(selector)
            if el:
                return el

    # GCP Docs
    if "cloud.google.com" in url:
        for selector in [
            "article", "devsite-content", ".devsite-article-body",
            "main", "[role='main']"
        ]:
            el = soup.select_one(selector)
            if el:
                return el

    # Azure pricing pages
    if "azure.microsoft.com" in url:
        for selector in ["main", "#content", ".wa-content"]:
            el = soup.select_one(selector)
            if el:
                return el

    # Generic fallback
    for selector in ["main", "article", "#content", ".content"]:
        el = soup.select_one(selector)
        if el:
            return el

    return None


def fetch_service_pages(service_config: dict, use_cache: bool = True) -> dict:
    """
    Fetch all documentation pages for a service.

    Args:
        service_config: Entry from the service catalog

    Returns:
        Dict mapping page_type -> fetch result
    """
    results = {}
    for page_type, url in service_config["urls"].items():
        print(f"    Fetching {page_type}: {url}")
        results[page_type] = fetch_page(url, use_cache=use_cache)
        if results[page_type]["error"]:
            print(f"      WARNING: {results[page_type]['error']}")
    return results


def clear_cache():
    """Remove all cached pages."""
    if CACHE_DIR.exists():
        import shutil
        shutil.rmtree(CACHE_DIR)
        print(f"Cache cleared: {CACHE_DIR}")
