"""Reddit adapter ready for praw/Pushshift."""

from typing import Iterable, List, Mapping


def build_query(keywords: Iterable[str]) -> str:
    return " OR ".join(f"title:{kw}" for kw in keywords)


def fetch_submissions(keywords: Iterable[str], limit: int = 50) -> List[Mapping[str, object]]:
    """Placeholder for Reddit scraping.

    Swap this stub with `praw` or Pushshift-powered logic. Return a list of
    dictionaries so downstream storage is consistent.
    """

    query = build_query(keywords)
    return [
        {
            "source": "reddit",
            "query": query,
            "title": "Example Reddit thread about " + ", ".join(keywords),
            "url": "https://reddit.com/example",
            "score": 123,
            "comments": 42,
        }
        for _ in range(limit)
    ]
