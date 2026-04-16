"""Tests for fetcher module."""

from unittest.mock import MagicMock, patch


from wikipdf.fetcher import Article, WikipediaFetcher, fetch_article


class TestWikipediaFetcher:
    """Tests for WikipediaFetcher class."""

    def test_fetch_success(self):
        """Test successful article fetch."""
        with patch("wikipdf.fetcher.wikipediaapi.Wikipedia") as mock_wiki_class:
            mock_wiki = MagicMock()
            mock_page = MagicMock()
            mock_page.title = "Python_(programming_language)"
            mock_page.summary = "Python is a programming language."
            mock_page.text = "Full content here..."
            mock_page.canonicalurl = (
                "https://en.wikipedia.org/wiki/Python_(programming_language)"
            )
            mock_page.exists.return_value = True
            mock_page.sections = []

            mock_wiki.page.return_value = mock_page
            mock_wiki_class.return_value = mock_wiki

            fetcher = WikipediaFetcher()
            article = fetcher.fetch("Python")

            assert article is not None
            assert article.title == "Python_(programming_language)"
            assert article.summary == "Python is a programming language."

    def test_fetch_not_found(self):
        """Test fetch with non-existent topic."""
        with patch("wikipdf.fetcher.wikipediaapi.Wikipedia") as mock_wiki_class:
            mock_wiki = MagicMock()
            mock_wiki.page.return_value.exists.return_value = False
            mock_wiki_class.return_value = mock_wiki

            fetcher = WikipediaFetcher()
            article = fetcher.fetch("NonexistentTopicThatDoesNotExist123")

            assert article is None

    def test_fetch_article_convenience(self):
        """Test fetch_article convenience function."""
        with patch("wikipdf.fetcher.WikipediaFetcher.fetch") as mock_fetch:
            mock_article = Article(
                title="Test",
                summary="Summary",
                content="Content",
                url="https://example.com",
                sections=[],
            )
            mock_fetch.return_value = mock_article

            result = fetch_article("Test")

            assert result is not None
            mock_fetch.assert_called_once()


class TestArticle:
    """Tests for Article dataclass."""

    def test_article_creation(self):
        """Test Article dataclass creation."""
        article = Article(
            title="Test",
            summary="Summary",
            content="Content",
            url="https://example.com",
            sections=[{"title": "Section", "text": "Text"}],
        )

        assert article.title == "Test"
        assert article.summary == "Summary"
        assert article.content == "Content"
        assert len(article.sections) == 1
