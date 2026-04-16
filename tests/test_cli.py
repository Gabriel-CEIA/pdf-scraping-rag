"""Tests for CLI module."""

from unittest.mock import patch

import pytest
from click.testing import CliRunner

from wikipdf.cli import ErrorTracker, cli


class TestErrorTracker:
    """Tests for ErrorTracker class."""

    def test_add_error(self, tmp_path):
        """Test adding an error."""
        tracker = ErrorTracker(tmp_path)
        tracker.add_error("Topic", "Not found")

        assert len(tracker.errors) == 1
        assert tracker.errors[0] == ("Topic", "Not found")

    def test_add_success(self, tmp_path):
        """Test adding a success."""
        tracker = ErrorTracker(tmp_path)
        tracker.add_success("Topic")

        assert len(tracker.successes) == 1
        assert tracker.successes[0] == "Topic"

    def test_write_logs_errors(self, tmp_path):
        """Test writing error log."""
        tracker = ErrorTracker(tmp_path)
        tracker.add_error("Topic", "Error message")
        tracker.write_logs()

        error_log = tmp_path / "wikipdf_errors.log"
        assert error_log.exists()
        content = error_log.read_text()
        assert "Topic" in content
        assert "Error message" in content

    def test_write_logs_success(self, tmp_path):
        """Test writing success log."""
        tracker = ErrorTracker(tmp_path)
        tracker.add_success("Topic1")
        tracker.add_success("Topic2")
        tracker.write_logs()

        success_log = tmp_path / "success.txt"
        assert success_log.exists()
        content = success_log.read_text()
        assert "Topic1" in content
        assert "Topic2" in content


class TestCLI:
    """Tests for CLI commands."""

    @pytest.fixture
    def runner(self):
        """Return a Click CLI test runner."""
        return CliRunner()

    @patch("wikipdf.cli.fetch_article")
    def test_fetch_command(self, mock_fetch, runner, tmp_path):
        """Test single fetch command."""
        from wikipdf.fetcher import Article

        mock_article = Article(
            title="Python",
            summary="Summary",
            content="Content",
            url="https://en.wikipedia.org/wiki/Python",
            sections=[],
        )
        mock_fetch.return_value = mock_article

        result = runner.invoke(cli, ["fetch", "Python", "-o", str(tmp_path)])

        assert result.exit_code == 0
        assert "Generated" in result.output

    @patch("wikipdf.cli.fetch_article")
    def test_fetch_not_found(self, mock_fetch, runner, tmp_path):
        """Test fetch with not found article."""
        mock_fetch.return_value = None

        result = runner.invoke(cli, ["fetch", "Nonexistent", "-o", str(tmp_path)])

        assert result.exit_code == 1

    @patch("wikipdf.cli.fetch_article")
    def test_bulk_command(self, mock_fetch, runner, tmp_path):
        """Test bulk fetch command."""
        from wikipdf.fetcher import Article

        input_file = tmp_path / "topics.txt"
        input_file.write_text("Python\nTest")

        mock_article = Article(
            title="Python",
            summary="Summary",
            content="Content",
            url="https://example.com",
            sections=[],
        )
        mock_fetch.return_value = mock_article

        result = runner.invoke(cli, ["bulk", str(input_file), "-o", str(tmp_path)])

        assert result.exit_code == 0
        assert "2/2" in result.output

    def test_bulk_empty_file(self, runner, tmp_path):
        """Test bulk with empty file."""
        input_file = tmp_path / "topics.txt"
        input_file.write_text("")

        result = runner.invoke(cli, ["bulk", str(input_file), "-o", str(tmp_path)])

        assert result.exit_code == 0
        assert "0 topics" in result.output

    def test_bulk_with_comments(self, runner, tmp_path):
        """Test bulk ignores comment lines."""
        input_file = tmp_path / "topics.txt"
        input_file.write_text("# Comment\nPython\n")

        with patch("wikipdf.cli.fetch_article") as mock_fetch:
            from wikipdf.fetcher import Article

            mock_fetch.return_value = Article(
                title="Python",
                summary="Summary",
                content="Content",
                url="https://example.com",
                sections=[],
            )

            result = runner.invoke(cli, ["bulk", str(input_file), "-o", str(tmp_path)])

            assert result.exit_code == 0
            mock_fetch.assert_called_once()

    def test_help_command(self, runner):
        """Test help command."""
        result = runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        assert "Wikipedia PDF Generator" in result.output
