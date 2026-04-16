"""CLI interface for wikipdf."""

import logging
import sys
from pathlib import Path
from typing import Optional

import click

from wikipdf import config
from wikipdf.fetcher import fetch_article
from wikipdf.pdfgen import article_to_pdf, sanitize_filename

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


class ErrorTracker:
    """Tracks errors and successes during processing."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.errors: list[tuple[str, str]] = []
        self.successes: list[str] = []

    def add_error(self, topic: str, error: str) -> None:
        self.errors.append((topic, error))
        logger.error(f"{topic}: {error}")

    def add_success(self, topic: str) -> None:
        self.successes.append(topic)
        logger.info(f"Processed: {topic}")

    def write_logs(self) -> None:
        if self.errors:
            error_log = self.output_dir / "wikipdf_errors.log"
            with open(error_log, "w") as f:
                f.write("=== Errors ===\n")
                for topic, error in self.errors:
                    f.write(f"- {topic}: {error}\n")
            logger.info(f"Errors logged to {error_log}")

        if self.successes:
            success_log = self.output_dir / "success.txt"
            with open(success_log, "w") as f:
                f.write("=== Successfully Processed ===\n")
                for topic in self.successes:
                    f.write(f"{topic}\n")
            logger.info(f"Successes logged to {success_log}")


@click.group()
@click.option(
    "-o",
    "--output-dir",
    type=click.Path(path_type=Path),
    default=config.OUTPUT_DIR,
    help="Output directory for PDFs",
)
@click.option(
    "-l",
    "--language",
    default=config.DEFAULT_WIKIPEDIA_LANGUAGE,
    help="Wikipedia language (en, es, fr, etc.)",
)
@click.pass_context
def cli(ctx: click.Context, output_dir: Path, language: str) -> None:
    """Wikipedia PDF Generator - Fetch Wikipedia articles and convert to PDF."""
    ctx.ensure_object(dict)
    ctx.obj["output_dir"] = output_dir
    ctx.obj["language"] = language
    output_dir.mkdir(parents=True, exist_ok=True)


@cli.command()
@click.argument("topic")
@click.option(
    "-o",
    "--output-dir",
    type=click.Path(path_type=Path),
    help="Output directory (overrides global)",
)
@click.option(
    "-l",
    "--language",
    help="Wikipedia language (overrides global)",
)
@click.pass_context
def fetch(
    ctx: click.Context, topic: str, output_dir: Optional[Path], language: Optional[str]
) -> None:
    """Fetch a single Wikipedia article and generate PDF."""
    output_dir = output_dir or ctx.obj["output_dir"]
    lang = language or ctx.obj["language"]
    tracker = ErrorTracker(output_dir)

    try:
        article = fetch_article(topic, lang)
        if article is None:
            tracker.add_error(topic, "Article not found on Wikipedia")
            tracker.write_logs()
            sys.exit(1)

        pdf_path = article_to_pdf(article, output_dir)
        tracker.add_success(topic)
        tracker.add_error(topic, "")
        tracker.write_logs()
        click.echo(f"Generated: {pdf_path}")

    except Exception as e:
        tracker.add_error(topic, str(e))
        tracker.write_logs()
        sys.exit(1)


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "-o",
    "--output-dir",
    type=click.Path(path_type=Path),
    help="Output directory (overrides global)",
)
@click.option(
    "-l",
    "--language",
    help="Wikipedia language (overrides global)",
)
@click.pass_context
def bulk(
    ctx: click.Context,
    input_file: Path,
    output_dir: Optional[Path],
    language: Optional[str],
) -> None:
    """Fetch multiple Wikipedia articles from a file.

    INPUT_FILE should contain one topic per line.
    Blank lines and lines starting with # are ignored.
    """
    output_dir = output_dir or ctx.obj["output_dir"]
    lang = language or ctx.obj["language"]
    tracker = ErrorTracker(output_dir)

    with open(input_file) as f:
        topics = [
            line.strip() for line in f if line.strip() and not line.startswith("#")
        ]

    click.echo(f"Processing {len(topics)} topics...")

    for topic in topics:
        try:
            article = fetch_article(topic, lang)
            if article is None:
                tracker.add_error(topic, "Article not found")
                continue

            article_to_pdf(article, output_dir)
            tracker.add_success(topic)
            click.echo(f"  Generated: {sanitize_filename(article.title)}")

        except Exception as e:
            tracker.add_error(topic, str(e))

    tracker.write_logs()
    click.echo(f"\nDone! {len(tracker.successes)}/{len(topics)} topics processed.")

    if tracker.errors:
        click.echo(
            f"Errors: {len(tracker.errors)} (see {output_dir}/wikipdf_errors.log)"
        )


if __name__ == "__main__":
    cli()
