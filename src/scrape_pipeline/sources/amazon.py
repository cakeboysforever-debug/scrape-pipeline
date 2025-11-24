"""Amazon product/review adapter."""

from typing import Iterable, List, Mapping


def fetch_reviews(keywords: Iterable[str], limit: int = 50) -> List[Mapping[str, object]]:
    """Placeholder for Amazon scraping or Product Advertising API calls."""

    return [
        {
            "source": "amazon",
            "keyword": keyword,
            "title": f"Sample product for {keyword}",
            "review": "Great product!",
            "rating": 4.5,
            "url": "https://amazon.com/example",
        }
        for keyword in keywords
    ][:limit]
