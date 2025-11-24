from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class NicheIdea:
    topic: str
    affiliate_payout: float
    urgent_intent_score: float
    evergreen_score: float
    search_volume: int


@dataclass
class NicheCriteria:
    min_affiliate_payout: float = 20.0
    min_urgent_intent_score: float = 0.6
    min_evergreen_score: float = 0.5
    min_search_volume: int = 1000


DEFAULT_CRITERIA = NicheCriteria()


def filter_niches(
    niches: Iterable[NicheIdea], criteria: NicheCriteria = DEFAULT_CRITERIA
) -> List[NicheIdea]:
    """Return niches that match the baseline thresholds.

    This is intentionally simple: the goal is to provide a starting point that can be
    swapped with live scoring (e.g., Google Trends, Exploding Topics, SEMrush API).
    """

    matching = []
    for niche in niches:
        if niche.affiliate_payout < criteria.min_affiliate_payout:
            continue
        if niche.urgent_intent_score < criteria.min_urgent_intent_score:
            continue
        if niche.evergreen_score < criteria.min_evergreen_score:
            continue
        if niche.search_volume < criteria.min_search_volume:
            continue
        matching.append(niche)
    return matching


def rank_niches(niches: Iterable[NicheIdea]) -> List[NicheIdea]:
    """Rank niches by a simple weighted score."""

    def niche_score(niche: NicheIdea) -> float:
        return (
            niche.affiliate_payout * 0.3
            + niche.urgent_intent_score * 30
            + niche.evergreen_score * 20
            + (niche.search_volume / 1000) * 0.4
        )

    return sorted(niches, key=niche_score, reverse=True)


def parse_niches(raw_niches: Iterable[dict]) -> List[NicheIdea]:
    """Turn YAML/JSON niches into strongly typed ideas."""
    ideas: List[NicheIdea] = []
    for raw in raw_niches:
        ideas.append(
            NicheIdea(
                topic=raw["topic"],
                affiliate_payout=float(raw.get("affiliate_payout", 0)),
                urgent_intent_score=float(raw.get("urgent_intent_score", 0)),
                evergreen_score=float(raw.get("evergreen_score", 0)),
                search_volume=int(raw.get("search_volume", 0)),
            )
        )
    return ideas
