# Beginner Scraping Walkthrough

This guide is written for first-time scrapers. It shows how to run the provided pipeline safely, inspect the results, and iterate without touching production sites until you are ready.

## Prerequisites
- Python 3.10+ installed (verify with `python --version`).
- Git installed to clone the repo (optional if you already have the files).
- No API keys are required—the defaults target publicly visible pages.
- A terminal you can run commands in (macOS/Linux/WSL/PowerShell).

## 1) Set up the environment
```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
pip check                 # confirm dependencies resolve cleanly
export PYTHONPATH=src  # Makes the scrape_pipeline package importable
```

## 2) Explore with preview mode (no live network calls)
Preview mode uses stub data so you can practice without hitting real sites.

```bash
python -m scrape_pipeline.pipeline --preview \
  --keywords "ai tools" "weight loss" \
  --limit 3
```
What you will see:
- Niche scoring logs for each keyword.
- Per-source preview rows (fake `preview_user_*` handles) written to `data/latest/*.jsonl` and `*.csv`.
- A SQLite database at `data/contacts.db` that you can open with any SQLite viewer.

## 3) Inspect the outputs
- **JSONL/CSV files**: open `data/latest/reddit.jsonl` (or any other source file) to see each scraped row. Each row includes `source`, `keyword`, `handle`, `email`, `url`, and `note` fields.
- **SQLite**: run `sqlite3 data/contacts.db "SELECT * FROM contacts LIMIT 5;"` to check the schema.

## 4) Swap in real scraping logic when ready
Each source has a stub function in `src/scrape_pipeline/sources/`:
- `reddit.py`, `quora.py`, `twitter.py`, `amazon.py`, `youtube.py`, `forums.py`

Replace the placeholder code inside `fetch_contacts` with your own compliant scraper. Keep the return format the same (list of dicts) so the storage helpers continue to work.

Tip: start with one source—edit only `reddit.py`—and keep `--limit` small (e.g., `--limit 5`) while testing.

## 5) Run a real scrape (small and polite)
```bash
python -m scrape_pipeline.pipeline \
  --keywords "example niche" \
  --limit 5 \
  --output-dir data/runs/$(date +%Y-%m-%d)
```
Good practices:
- Respect each site's Terms of Service and robots.txt.
- Add delays in your scrapers to avoid hammering servers.
- Use `--proxy`/`--proxy-file` if you run into blocks; the pipeline will rotate them for you.

## 6) Iterate safely
- Adjust keywords in the command or in `pipeline.py`'s defaults.
- Keep preview mode on while developing new scrapers to avoid accidental traffic.
- Version control your scraper changes so you can roll back easily.

## Troubleshooting checklist
- **"Module not found"**: ensure `export PYTHONPATH=src` (or set it in your shell profile).
- **Empty outputs**: confirm the scraper returns a list of dictionaries with the expected fields.
- **Proxy errors**: test individual proxies with `curl -x http://host:port https://example.com` before relying on them.

Happy scraping! Start small, check your data, and expand once you are comfortable.
