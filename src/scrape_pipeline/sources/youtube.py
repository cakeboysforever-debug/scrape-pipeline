"""YouTube comments/metadata adapter."""

from typing import Iterable, List, Mapping


def fetch_contacts(keywords: Iterable[str], limit: int = 50) -> List[Mapping[str, object]]:
    """Placeholder for `youtube-dl`/`yt-dlp` comment + metadata scraping."""

    return [
        {
            "source": "youtube",
            "keyword": keyword,
            "handle": f"channel_{idx}",
            "email": None,
            "url": "https://youtube.com/watch?v=example",
            "note": f"Commenter on a {keyword} video",
        }
        for idx, keyword in enumerate(keywords, start=1)
    ][:limit]
