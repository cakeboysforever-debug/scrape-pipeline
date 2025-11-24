import argparse
from pathlib import Path
from typing import Any, Dict, List

import yaml

from .niche_finder import DEFAULT_CRITERIA, filter_niches, parse_niches, rank_niches
from .scraper_registry import build_registry


def load_config(path: Path) -> Dict[str, Any]:
    with path.open() as handle:
        return yaml.safe_load(handle)


def run_pipeline(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    raw_niches = config.get("niches", [])
    sources = config.get("sources", [])

    registry = build_registry()
    parsed_niches = parse_niches(raw_niches)
    filtered_niches = filter_niches(parsed_niches, DEFAULT_CRITERIA)
    ranked_niches = rank_niches(filtered_niches)

    results: List[Dict[str, Any]] = []
    for niche in ranked_niches:
        for source_name in sources:
            source = registry.get(source_name)
            scraped = source.scraper(niche.topic)
            for item in scraped:
                results.append({
                    "topic": niche.topic,
                    "source": source.name,
                    "data": item,
                })
    return results


def format_results(results: List[Dict[str, Any]]) -> str:
    lines = []
    for item in results:
        lines.append(
            f"[{item['source']}] {item['topic']}: {item['data']['summary']} (query={item['data']['query']})"
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the scraping pipeline scaffold")
    parser.add_argument("config", type=Path, help="Path to the YAML config file")
    args = parser.parse_args()

    config = load_config(args.config)
    results = run_pipeline(config)
    print(format_results(results))


if __name__ == "__main__":
    main()
