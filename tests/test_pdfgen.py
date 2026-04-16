"""Tests for pdfgen module."""

from unittest.mock import patch


from wikipdf.fetcher import Article
from wikipdf.pdfgen import (
    ArticleToPDF,
    article_to_pdf,
    format_title_for_display,
    sanitize_filename,
)


class TestSanitizeFilename:
    """Tests for sanitize_filename function."""

    def test_simple_title(self):
        """Test simple title sanitization."""
        result = sanitize_filename("Python")
        assert result == "Python.pdf"

    def test_title_with_spaces(self):
        """Test title with spaces."""
        result = sanitize_filename("Python programming language")
        assert result == "Python_programming_language.pdf"

    def test_already_underscores(self):
        """Test title already with underscores."""
        result = sanitize_filename("Python_(programming_language)")
        assert result == "Python_(programming_language).pdf"

    def test_special_characters(self):
        """Test title with special characters."""
        result = sanitize_filename("Test: Page")
        assert result == "Test:_Page.pdf"


class TestFormatTitleForDisplay:
    """Tests for format_title_for_display function."""

    def test_underscores_to_spaces(self):
        """Test converting underscores to spaces."""
        result = format_title_for_display("Python_(programming_language)")
        assert result == "Python (programming language)"

    def test_no_change(self):
        """Test title without underscores."""
        result = format_title_for_display("Python")
        assert result == "Python"


class TestArticleToPDF:
    """Tests for ArticleToPDF class."""

    def test_generate_pdf(self, tmp_path):
        """Test PDF generation."""
        article = Article(
            title="Python",
            summary="Python is a programming language.",
            content="Full content of the article.",
            url="https://en.wikipedia.org/wiki/Python",
            sections=[],
        )

        generator = ArticleToPDF(output_dir=tmp_path)
        pdf_path = generator.generate(article)

        assert pdf_path.exists()
        assert pdf_path.name == "Python.pdf"

    def test_output_dir_created(self, tmp_path):
        """Test output directory is created if missing."""
        output_dir = tmp_path / "new_dir"
        assert not output_dir.exists()

        article = Article(
            title="Test",
            summary="Summary",
            content="Content",
            url="https://example.com",
            sections=[],
        )

        generator = ArticleToPDF(output_dir=output_dir)
        generator.generate(article)

        assert output_dir.exists()

    def test_article_to_pdf_convenience(self, tmp_path):
        """Test article_to_pdf convenience function."""
        article = Article(
            title="Test",
            summary="Summary",
            content="Content",
            url="https://example.com",
            sections=[],
        )

        with patch("wikipdf.pdfgen.ArticleToPDF.generate") as mock_gen:
            mock_gen.return_value = tmp_path / "test.pdf"
            result = article_to_pdf(article, tmp_path)

            assert result == tmp_path / "test.pdf"
