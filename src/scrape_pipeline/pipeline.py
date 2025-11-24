"""CLI-friendly pipeline orchestrator."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Callable, Iterable, List, Mapping, Sequence

from . import niche_identification
from . import storage
from .sources import amazon, forums, quora, reddit, twitter, youtube

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
LOGGER = logging.getLogger(__name__)

SourceFunc = Callable[[Iterable[str], int], List[Mapping[str, object]]]


SOURCE_BUILDERS: Mapping[str, SourceFunc] = {
    "reddit": reddit.fetch_submissions,
    "quora": quora.fetch_questions,
    "twitter": twitter.fetch_tweets,
    "amazon": amazon.fetch_reviews,
    "youtube": youtube.fetch_comments,
    "forums": forums.fetch_threads,
}


def run_sources(keywords: Sequence[str], preview: bool, limit: int) -> Mapping[str, List[Mapping[str, object]]]:
    results: dict[str, List[Mapping[str, object]]] = {}
    for name, fetcher in SOURCE_BUILDERS.items():
        LOGGER.info("Running source: %s", name)
        if preview:
            results[name] = [
                {
                    "source": name,
                    "keywords": ", ".join(keywords),
                    "note": "Preview mode — replace stub with live scraping",
                }
            ]
        else:
            results[name] = fetcher(keywords, limit=limit)
    return results


def persist_outputs(output_dir: Path, payload: Mapping[str, List[Mapping[str, object]]]) -> None:
    for name, records in payload.items():
        json_path = output_dir / f"{name}.jsonl"
        csv_path = output_dir / f"{name}.csv"
        LOGGER.info("Writing %s records to %s", len(records), json_path)
        storage.write_jsonl(json_path, records)
        storage.write_csv(csv_path, records)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Step-by-step scraping pipeline")
    parser.add_argument("--keywords", nargs="*", default=["weight loss", "cybersecurity", "passive income"], help="Keywords or niches to target")
    parser.add_argument("--limit", type=int, default=25, help="Max items per source")
    parser.add_argument("--output-dir", type=Path, default=Path("data/latest"), help="Where to save output files")
    parser.add_argument("--preview", action="store_true", help="Skip live scraping and show planned actions")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    LOGGER.info("Scoring niches: %s", args.keywords)
    ranked = niche_identification.prioritize_niches(args.keywords, top_n=len(args.keywords))
    for item in ranked:
        LOGGER.info("%-20s score=%.2f (payout=%.2f, urgency=%.2f, evergreen=%.2f, volume=%.2f)",
                    item.keyword, item.total(), item.payout_score, item.urgency_score, item.evergreen_score, item.search_volume_score)

    results = run_sources(args.keywords, preview=args.preview, limit=args.limit)

    if args.output_dir:
        persist_outputs(args.output_dir, results)
        LOGGER.info("Wrote outputs to %s", args.output_dir)


if __name__ == "__main__":
    main()
