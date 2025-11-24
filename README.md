# Scrape Pipeline

A step-by-step, API-friendly scraping pipeline blueprint that collects niche intel from social and commerce sources. This repo bundles:

- **Niche identification** heuristics so you know what to target.
- **Scraping adapters** for Reddit, Quora, Twitter/X, Amazon, YouTube, and generic forums.
- **Data storage** helpers for JSON/CSV outputs.
- **Runner** to orchestrate the pipeline with simple configuration.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m scrape_pipeline.pipeline --preview
```

- `--preview` skips live network calls and shows what each stage would do.
- Add API keys in a `.env` file or environment variables when ready for real scraping.

## Project Structure

```
src/scrape_pipeline/
  niche_identification.py   # demand scoring + prioritization helpers
  pipeline.py               # orchestration CLI entrypoint
  storage.py                # JSON/CSV writers
  sources/
    reddit.py               # Reddit adapter (praw/pushshift-ready)
    quora.py                # Quora adapter (selenium/quora-scraper ready)
    twitter.py              # Twitter/X adapter (snscrape/tweepy-ready)
    amazon.py               # Amazon reviews/products adapter
    youtube.py              # YouTube comments/metadata adapter
    forums.py               # Generic forums via Scrapy/BeautifulSoup
```

## Configuration

- Set credentials via environment variables (recommended with a `.env` file):
  - `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USER_AGENT`
  - `TWITTER_BEARER_TOKEN` (if using Twitter API), or rely on `snscrape` for public data
  - `YOUTUBE_API_KEY`
  - `AMAZON_PARTNER_TAG` and `AMAZON_ACCESS_KEY/SECRET` (if using Product Advertising API)
- Customize keywords and sources in `pipeline.py` (see the `SOURCE_BUILDERS` mapping).

## Step-by-Step Flow

1. **Niche Identification**
   - Score candidate niches with payout, urgency, evergreen demand, and search volume signals.
   - Validate spikes using **Google Trends**, **SEMrush**, or **Exploding Topics** exports.
2. **Scraping Data Sources**
   - Reddit: niche threads, user pain points.
   - Quora: long-tail Q&A and reviews.
   - Twitter/X: trends, questions, keyword intel.
   - Amazon: product mentions and reviews.
   - YouTube: comments and video metadata.
   - Forums: deep niche complaints.
3. **Storage**
   - Save raw pulls per source as JSON lines or CSV for analysis.
4. **Review & Iterate**
   - Inspect outputs, refine keywords, and reschedule runs.

## Usage Examples

### Dry-run the pipeline

```bash
python -m scrape_pipeline.pipeline --keywords "weight loss" "cybersecurity" --preview
```

### Persist outputs

```bash
python -m scrape_pipeline.pipeline \
  --keywords "passive income" "ai tools" \
  --output-dir data/runs/$(date +%Y-%m-%d)
```

- Creates per-source JSONL files in the output directory.
- Remove `--preview` to enable real network calls once credentials and scraping logic are filled in.

## Extending

- Add more sources by creating a new module under `src/scrape_pipeline/sources/` and wiring it into `SOURCE_BUILDERS` in `pipeline.py`.
- Swap storage backends by extending `storage.py` (e.g., Postgres, S3, or Firestore clients).

## Disclaimer

This repository provides scaffolding. Before running against real sites, review each target's Terms of Service and apply appropriate rate limiting, authentication, and consent.
