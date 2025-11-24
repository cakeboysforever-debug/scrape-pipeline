"""Module entrypoint for the scrape_pipeline CLI."""

from . import pipeline


def main() -> None:
    pipeline.main()


if __name__ == "__main__":
    main()
