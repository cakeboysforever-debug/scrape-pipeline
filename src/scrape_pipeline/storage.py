"""Storage helpers for pipeline outputs."""

from __future__ import annotations

import json
import logging
import sqlite3
from pathlib import Path
from typing import Iterable, Mapping

import pandas as pd

LOGGER = logging.getLogger(__name__)


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


def write_sqlite(db_path: Path, records: Iterable[Mapping[str, object]]) -> None:
    """Persist contacts into a SQLite database.

    A simple `contacts` table is created if missing. Duplicate rows based on
    `(source, handle, keyword, url)` are ignored to keep the DB deduplicated.
    """

    ensure_dir(db_path.parent)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                keyword TEXT,
                handle TEXT,
                email TEXT,
                url TEXT,
                note TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(source, handle, keyword, url)
            )
            """
        )

        prepared = [
            (
                record.get("source"),
                record.get("keyword"),
                record.get("handle"),
                record.get("email"),
                record.get("url"),
                record.get("note"),
            )
            for record in records
        ]

        if not prepared:
            LOGGER.info("No records to write to SQLite")
            return

        conn.executemany(
            """
            INSERT OR IGNORE INTO contacts (source, keyword, handle, email, url, note)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            prepared,
        )
        conn.commit()
        LOGGER.info("Inserted %s unique contact rows into %s", len(prepared), db_path)
