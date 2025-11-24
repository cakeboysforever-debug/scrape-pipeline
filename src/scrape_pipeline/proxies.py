"""Lightweight helpers for proxy rotation with public lists."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable, List

LOGGER = logging.getLogger(__name__)


def load_proxies(inline: Iterable[str] | None = None, proxy_file: Path | None = None) -> List[str]:
    """Combine inline proxies and an optional file into a de-duplicated list.

    The file is expected to be newline-delimited (e.g., ``http://host:port``).
    Empty lines and comments (``#`` prefix) are ignored.
    """

    inline = inline or []
    combined: list[str] = []

    for item in inline:
        cleaned = item.strip()
        if cleaned:
            combined.append(cleaned)

    if proxy_file and proxy_file.exists():
        for raw in proxy_file.read_text().splitlines():
            cleaned = raw.strip()
            if not cleaned or cleaned.startswith("#"):
                continue
            combined.append(cleaned)
    elif proxy_file:
        LOGGER.warning("Proxy file %s not found; skipping", proxy_file)

    # Preserve order but drop duplicates
    seen: set[str] = set()
    deduped: list[str] = []
    for proxy in combined:
        if proxy not in seen:
            deduped.append(proxy)
            seen.add(proxy)
    return deduped


def example_free_sources() -> List[str]:
    """Return placeholder proxy URLs from well-known free lists.

    Swap this stub with a real fetcher (e.g., scraping sslproxies.org or
    https://github.com/roosterkid/openproxylist). This keeps the project free
    of bundled live proxies while showing the expected format.
    """

    return [
        "http://203.0.113.10:8080",
        "http://203.0.113.11:3128",
    ]
