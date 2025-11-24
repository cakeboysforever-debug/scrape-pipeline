# Scrape Pipeline

A step-by-step scraping pipeline blueprint focused on collecting **usernames and emails** tied to a niche or keyword and storing them in a SQLite contacts database. All collection is scoped to **publicly available data**—no API keys required. This repo bundles:

- **Niche identification** heuristics so you know what to target.
- **Scraping adapters** for Reddit, Quora, Twitter/X, Amazon, YouTube, and generic forums that return contact handles.
- **Data storage** helpers for JSON/CSV outputs plus a deduplicated SQLite contact table.
- **Runner** to orchestrate the pipeline with simple configuration.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m scrape_pipeline.pipeline --preview
```

- `--preview` skips live network calls and shows what each stage would do.

## Project Structure

```
src/scrape_pipeline/
  niche_identification.py   # demand scoring + prioritization helpers
  pipeline.py               # orchestration CLI entrypoint
  storage.py                # JSON/CSV writers + SQLite contact sink
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

## Extending

- Add more sources by creating a new module under `src/scrape_pipeline/sources/` and wiring it into `SOURCE_BUILDERS` in `pipeline.py`.
- Swap storage backends by extending `storage.py` (e.g., Postgres, S3, or Firestore clients).

## Disclaimer

This repository provides scaffolding. Before running against real sites, review each target's Terms of Service and apply appropriate rate limiting, authentication, and consent.
