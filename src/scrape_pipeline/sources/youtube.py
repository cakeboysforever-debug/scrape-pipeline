"""YouTube comments/metadata adapter."""

from typing import Iterable, List, Mapping


def fetch_comments(keywords: Iterable[str], limit: int = 50) -> List[Mapping[str, object]]:
    """Placeholder for YouTube Data API or youtube-dl extraction."""

    return [
        {
            "source": "youtube",
            "keyword": keyword,
            "video_title": f"{keyword} deep dive",
            "comment": "Informative content!",
            "video_url": "https://youtube.com/watch?v=example",
        }
        for keyword in keywords
    ][:limit]
