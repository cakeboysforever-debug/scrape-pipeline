"""Storage helpers for pipeline outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Mapping

import pandas as pd


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_jsonl(path: Path, records: Iterable[Mapping[str, object]]) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as fp:
        for record in records:
            fp.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_csv(path: Path, records: Iterable[Mapping[str, object]]) -> None:
    ensure_dir(path.parent)
    frame = pd.DataFrame(list(records))
    frame.to_csv(path, index=False)
