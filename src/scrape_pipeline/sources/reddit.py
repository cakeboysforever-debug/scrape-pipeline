"""Reddit adapter using public endpoints or HTML scraping."""

from typing import Iterable, List, Mapping


def build_query(keywords: Iterable[str]) -> str:
    return " OR ".join(f"title:{kw}" for kw in keywords)


def fetch_contacts(keywords: Iterable[str], limit: int = 50) -> List[Mapping[str, object]]:
    """Placeholder for Reddit scraping without API keys.

    Swap this stub for a `snscrape`/Pushshift query or requests + BeautifulSoup
    crawl that extracts public author handles and any contact hints from
    comments or bios. Keep collection compliant with Reddit policies and
    robots.txt.
    """

    query = build_query(keywords)
    return [
        {
            "source": "reddit",
            "keyword": kw,
            "handle": f"reddit_user_{idx}",
            "email": None,
            "url": "https://reddit.com/r/example/comments/123",
            "note": f"Matched query: {query}",
        }
        for idx, kw in enumerate(keywords, start=1)
    ][:limit]
