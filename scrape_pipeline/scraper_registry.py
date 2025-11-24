from typing import Dict, List

from .sources import DataSource, Registry


def _stub(name: str, query: str) -> List[Dict[str, str]]:
    return [
        {
            "source": name,
            "query": query,
            "summary": "Placeholder result. Replace with real API or scraper call.",
        }
    ]


def reddit_scraper(query: str) -> List[Dict[str, str]]:
    return _stub("Reddit", query)


def quora_scraper(query: str) -> List[Dict[str, str]]:
    return _stub("Quora", query)


def twitter_scraper(query: str) -> List[Dict[str, str]]:
    return _stub("Twitter/X", query)


def amazon_scraper(query: str) -> List[Dict[str, str]]:
    return _stub("Amazon", query)


def youtube_scraper(query: str) -> List[Dict[str, str]]:
    return _stub("YouTube", query)


def forum_scraper(query: str) -> List[Dict[str, str]]:
    return _stub("Forums", query)


def build_registry() -> Registry:
    return Registry(
        [
            DataSource(
                name="Reddit",
                description="Niche threads and pain points",
                recommended_tools=["praw", "pushshift", "snoowrap"],
                scraper=reddit_scraper,
            ),
            DataSource(
                name="Quora",
                description="Long-tail Q&A and reviews",
                recommended_tools=["selenium", "quora-scraper"],
                scraper=quora_scraper,
            ),
            DataSource(
                name="Twitter/X",
                description="Trends and keyword intelligence",
                recommended_tools=["tweepy", "snscrape"],
                scraper=twitter_scraper,
            ),
            DataSource(
                name="Amazon",
                description="Product mentions and reviews",
                recommended_tools=["requests", "beautifulsoup4", "official Amazon APIs"],
                scraper=amazon_scraper,
            ),
            DataSource(
                name="YouTube",
                description="Comments and video metadata",
                recommended_tools=["youtube-dl", "youtube-data-api"],
                scraper=youtube_scraper,
            ),
            DataSource(
                name="Forums",
                description="Deep niche complaints",
                recommended_tools=["scrapy", "beautifulsoup4"],
                scraper=forum_scraper,
            ),
        ]
    )
