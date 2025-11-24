"""CLI-friendly pipeline orchestrator."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Callable, Iterable, List, Mapping, Sequence

from . import niche_identification
from . import storage
from . import proxies
from .sources import amazon, forums, quora, reddit, twitter, youtube

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
LOGGER = logging.getLogger(__name__)

SourceFunc = Callable[[Iterable[str], int, Sequence[str] | None], List[Mapping[str, object]]]


SOURCE_BUILDERS: Mapping[str, SourceFunc] = {
    "reddit": reddit.fetch_contacts,
    "quora": quora.fetch_contacts,
    "twitter": twitter.fetch_contacts,
    "amazon": amazon.fetch_contacts,
    "youtube": youtube.fetch_contacts,
    "forums": forums.fetch_contacts,
}


def run_sources(keywords: Sequence[str], preview: bool, limit: int, proxies_list: Sequence[str] | None) -> Mapping[str, List[Mapping[str, object]]]:
    results: dict[str, List[Mapping[str, object]]] = {}
    for name, fetcher in SOURCE_BUILDERS.items():
        LOGGER.info("Running source: %s", name)
        if preview:
            results[name] = [
                {
                    "source": name,
                    "keyword": kw,
                    "handle": f"preview_user_{idx}",
                    "email": None,
                    "url": "https://example.com",
                    "note": "Preview mode — replace stub with live scraping",
                }
                for idx, kw in enumerate(keywords, start=1)
            ][:limit]
        else:
            results[name] = fetcher(keywords, limit=limit, proxies=proxies_list)
    return results


def persist_outputs(output_dir: Path, db_path: Path, payload: Mapping[str, List[Mapping[str, object]]]) -> None:
    flattened: list[Mapping[str, object]] = []

    for name, records in payload.items():
        json_path = output_dir / f"{name}.jsonl"
        csv_path = output_dir / f"{name}.csv"
        LOGGER.info("Writing %s records to %s", len(records), json_path)
        storage.write_jsonl(json_path, records)
        storage.write_csv(csv_path, records)
        flattened.extend(records)

    LOGGER.info("Persisting %s contact rows into SQLite at %s", len(flattened), db_path)
    storage.write_sqlite(db_path, flattened)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Step-by-step scraping pipeline")
    parser.add_argument("--keywords", nargs="*", default=["weight loss", "cybersecurity", "passive income"], help="Keywords or niches to target")
    parser.add_argument("--limit", type=int, default=25, help="Max items per source")
    parser.add_argument("--output-dir", type=Path, default=Path("data/latest"), help="Where to save per-source JSON/CSV files")
    parser.add_argument("--db-path", type=Path, default=Path("data/contacts.db"), help="SQLite file for deduplicated contacts")
    parser.add_argument("--proxy", action="append", default=[], help="Proxy URL (e.g., http://host:port). Repeatable")
    parser.add_argument("--proxy-file", type=Path, help="Path to newline-delimited proxies to rotate")
    parser.add_argument("--preview", action="store_true", help="Skip live scraping and show planned actions")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    proxies_list = proxies.load_proxies(args.proxy, args.proxy_file)
    if proxies_list:
        LOGGER.info("Loaded %s proxies (first: %s)", len(proxies_list), proxies_list[0])
    else:
        LOGGER.info("No proxies configured — running direct requests")
    LOGGER.info("Scoring niches: %s", args.keywords)
    ranked = niche_identification.prioritize_niches(args.keywords, top_n=len(args.keywords))
    for item in ranked:
        LOGGER.info("%-20s score=%.2f (payout=%.2f, urgency=%.2f, evergreen=%.2f, volume=%.2f)",
                    item.keyword, item.total(), item.payout_score, item.urgency_score, item.evergreen_score, item.search_volume_score)

    results = run_sources(args.keywords, preview=args.preview, limit=args.limit, proxies_list=proxies_list)

    if args.output_dir:
        persist_outputs(args.output_dir, args.db_path, results)
        LOGGER.info("Wrote outputs to %s and %s", args.output_dir, args.db_path)


if __name__ == "__main__":
    main()
