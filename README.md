# Scrape Pipeline

A step-by-step scraping pipeline blueprint focused on collecting **usernames and emails** tied to a niche or keyword and storing them in a SQLite contacts database. All collection is scoped to **publicly available data**—no API keys required. This repo bundles:

- **Niche identification** heuristics so you know what to target.
- **Scraping adapters** for Reddit, Quora, Twitter/X, Amazon, YouTube, and generic forums that return contact handles.
- **Data storage** helpers for JSON/CSV outputs plus a deduplicated SQLite contact table.
- **Runner** to orchestrate the pipeline with simple configuration.
- **Proxy helpers** to rotate free/public proxies when you need to reduce blocking risk.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./bin/scrape_pipeline --help   # or: python -m scrape_pipeline --help
python -m scrape_pipeline.pipeline --preview
```

- `--preview` skips live network calls and shows what each stage would do.
  - `scrape_pipeline --help` shows all flags without running the pipeline.
  - `man scrape_pipeline` (see below) opens the manual page.
  - `--preview` skips live network calls and shows what each stage would do.

## Project Structure

```
src/scrape_pipeline/
  niche_identification.py   # demand scoring + prioritization helpers
  pipeline.py               # orchestration CLI entrypoint
  storage.py                # JSON/CSV writers + SQLite contact sink
  proxies.py                # proxy rotation helpers (file + inline)
  sources/
    reddit.py               # Reddit adapter (Pushshift/scrape-ready)
    quora.py                # Quora adapter (selenium/quora-scraper ready)
    twitter.py              # Twitter/X adapter (snscrape-ready)
    amazon.py               # Amazon reviews/products adapter
    youtube.py              # YouTube comments/metadata adapter (youtube-dl/yt-dlp)
    forums.py               # Generic forums via Scrapy/BeautifulSoup
```

## Configuration

- This pipeline leans on public-page tooling: `snscrape` for Twitter/X, `youtube-dl` for YouTube comments/metadata, and `requests` + `BeautifulSoup`/`Scrapy`/`selenium` for forums, Amazon, Quora, and Reddit. No API secrets are necessary.
- Customize keywords and sources in `pipeline.py` (see the `SOURCE_BUILDERS` mapping).
- Rotate free proxies via `--proxy`/`--proxy-file` to avoid rate limits.

## Step-by-Step Flow

1. **Niche Identification**
   - Score candidate niches with payout, urgency, evergreen demand, and search volume signals.
   - Validate spikes using **Google Trends**, **SEMrush**, or **Exploding Topics** exports.
2. **Scraping Data Sources** (usernames/emails)
   - Reddit: authors in matched threads.
   - Quora: question askers/answerers in the niche.
   - Twitter/X: posters referencing the keyword.
   - Amazon: sellers/reviewers mentioning the niche.
   - YouTube: commenters or channel handles.
   - Forums: posters in niche-specific discussions.
3. **Storage**
   - Save raw pulls per source as JSON lines or CSV for inspection.
   - Insert deduped contacts into `data/contacts.db` (SQLite) with `source`, `keyword`, `handle`, optional `email`, `url`, and `note` fields.
4. **Review & Iterate**
   - Inspect outputs, refine keywords, and reschedule runs.

## Usage Examples

### Dry-run the pipeline

```bash
python -m scrape_pipeline.pipeline --keywords "weight loss" "cybersecurity" --preview
```

### Persist outputs (JSON/CSV + SQLite)

```bash
python -m scrape_pipeline.pipeline \
  --keywords "passive income" "ai tools" \
  --output-dir data/runs/$(date +%Y-%m-%d) \
  --db-path data/contacts.db
```

- Creates per-source JSONL/CSV files in the output directory.
- Deduplicates contacts into `data/contacts.db` (table: `contacts`).
- Remove `--preview` to enable real network calls once your scraping logic is filled in.

### CLI help and manual page

- Show command help:

  ```bash
  ./bin/scrape_pipeline --help
  ```

- Read the man page from this repo (without installing system-wide):

  ```bash
  MANPATH="$(pwd)/man:${MANPATH}" man scrape_pipeline
  ```

### Use free proxies (optional)

Free/public proxies can be noisy or short-lived; always test before production use.

1. Grab a list from a free provider (examples):
   - https://www.sslproxies.org/
   - https://free-proxy-list.net/
   - GitHub mirrors such as https://github.com/roosterkid/openproxylist or https://github.com/prxchk/proxy-list
2. Save them to `proxies.txt`, one per line (format: `http://host:port`). Comments with `#` are ignored.
3. Run the pipeline with rotation enabled:

```bash
python -m scrape_pipeline.pipeline \
  --keywords "niche keyword" \
  --proxy-file proxies.txt \
  --proxy http://additional-proxy:8080 \
  --output-dir data/runs/with-proxies \
  --db-path data/contacts.db
```

- The CLI de-duplicates proxies from the file and `--proxy` flags.
- In stubs, proxies are logged; wire them into your HTTP client or `snscrape`/`requests` calls as needed.

## Extending

- Add more sources by creating a new module under `src/scrape_pipeline/sources/` and wiring it into `SOURCE_BUILDERS` in `pipeline.py`.
- Swap storage backends by extending `storage.py` (e.g., Postgres, S3, or Firestore clients).

## Disclaimer

This repository provides scaffolding. Before running against real sites, review each target's Terms of Service and apply appropriate rate limiting, authentication, and consent.
