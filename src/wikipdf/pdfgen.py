"""PDF generator using fpdf2."""

import logging
import re
from pathlib import Path

from fpdf import FPDF, XPos, YPos

from wikipdf import config
from wikipdf.fetcher import Article

logger = logging.getLogger(__name__)

NON_ASCII_RE = re.compile(r"[^\x00-\x7F]")


def sanitize_for_pdf(text: str) -> str:
    """Replace non-ASCII characters with their ASCII equivalents or generic placeholder."""
    return NON_ASCII_RE.sub("?", text)


def sanitize_filename(title: str) -> str:
    """Convert title to safe filename with underscores.

    Args:
        title: Original article title.

    Returns:
        Sanitized filename, e.g., "Python_(programming_language).pdf"
    """
    sanitized = title.replace(" ", "_")
    return f"{sanitized}.pdf"


def format_title_for_display(title: str) -> str:
    """Format title for PDF display (replace underscores with spaces).

    Args:
        title: Title with underscores.

    Returns:
        Title formatted with spaces.
    """
    return title.replace("_", " ")


class PDFGenerator(FPDF):
    """PDF generator for Wikipedia articles."""

    def __init__(self):
        super().__init__(unit="mm", format=config.PDF_PAGE_SIZE)
        self.set_auto_page_break(auto=True, margin=config.PDF_MARGIN)

    def header(self) -> None:
        pass

    def footer(self) -> None:
        self.set_y(-15)
        self.set_font(size=8)
        self.cell(0, 10, "Page {self.page_no()}", align="C")


class ArticleToPDF:
    """Converts Wikipedia articles to PDF."""

    def __init__(self, output_dir: Path | None = None):
        self.output_dir = output_dir or config.OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, article: Article) -> Path:
        """Generate a PDF from a Wikipedia article.

        Args:
            article: Article object from fetcher.

        Returns:
            Path to the generated PDF.
        """
        pdf = PDFGenerator()
        pdf.add_page()

        pdf.set_font("Helvetica", size=config.PDF_FONT_SIZE_TITLE)
        title_display = sanitize_for_pdf(format_title_for_display(article.title))
        pdf.cell(0, 10, title_display, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        pdf.ln(5)

        pdf.set_font("Helvetica", size=config.PDF_FONT_SIZE_SECTION)
        pdf.cell(0, 8, "Summary", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Helvetica", size=config.PDF_FONT_SIZE_BODY)
        pdf.multi_cell(0, 5, sanitize_for_pdf(article.summary))
        pdf.ln(5)

        pdf.set_font("Helvetica", size=config.PDF_FONT_SIZE_SECTION)
        pdf.cell(0, 8, "Full Article", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Helvetica", size=config.PDF_FONT_SIZE_BODY)
        pdf.multi_cell(0, 5, sanitize_for_pdf(article.content[:10000]))
        pdf.ln(10)

        pdf.set_font(size=9)
        pdf.cell(
            0,
            5,
            f"Source: {article.url}",
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
            align="C",
        )

        filename = sanitize_filename(article.title)
        filepath = self.output_dir / filename
        pdf.output(str(filepath))
        logger.info(f"Generated PDF: {filepath}")

        return filepath


def article_to_pdf(article: Article, output_dir: Path | None = None) -> Path:
    """Convenience function to generate a PDF from an article."""
    generator = ArticleToPDF(output_dir)
    return generator.generate(article)
