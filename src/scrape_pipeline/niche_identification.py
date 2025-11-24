"""Niche identification heuristics."""

from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class NicheScore:
    """Represents a scored niche candidate."""

    keyword: str
    payout_score: float
    urgency_score: float
    evergreen_score: float
    search_volume_score: float

    def total(self) -> float:
        """Return weighted total score."""

        return (
            self.payout_score * 0.35
            + self.urgency_score * 0.25
            + self.evergreen_score * 0.2
            + self.search_volume_score * 0.2
        )


def score_keyword(keyword: str) -> NicheScore:
    """Stub for evaluating a keyword.

    Replace with calls to Google Trends, SEMrush, or Exploding Topics by fetching
    their CSV exports and normalizing into 0–1 scores.
    """

    baseline = len(keyword) % 10 / 10  # deterministic placeholder
    return NicheScore(
        keyword=keyword,
        payout_score=baseline + 0.3,
        urgency_score=baseline + 0.2,
        evergreen_score=baseline + 0.1,
        search_volume_score=baseline + 0.2,
    )


def prioritize_niches(keywords: Iterable[str], top_n: int = 5) -> List[NicheScore]:
    """Score and rank keywords, returning the top choices."""

    scores = [score_keyword(keyword) for keyword in keywords]
    return sorted(scores, key=lambda item: item.total(), reverse=True)[:top_n]
