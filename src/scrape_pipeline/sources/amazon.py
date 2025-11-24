"""Amazon product/review adapter."""

from typing import Iterable, List, Mapping


def fetch_contacts(keywords: Iterable[str], limit: int = 50) -> List[Mapping[str, object]]:
    """Placeholder for public Amazon page scraping (no API keys)."""

    return [
        {
            "source": "amazon",
            "keyword": keyword,
            "handle": f"seller_{idx}",
            "email": None,
            "url": "https://amazon.com/example",
            "note": f"Seller or reviewer mentioning {keyword}",
        }
        for idx, keyword in enumerate(keywords, start=1)
    ][:limit]
