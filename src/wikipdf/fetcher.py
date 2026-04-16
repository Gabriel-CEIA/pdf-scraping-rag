"""Wikipedia article fetcher using wikipedia-api."""

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

import wikipediaapi
from requests_cache import CachedSession

from wikipdf import config

if TYPE_CHECKING:
    from wikipediaapi import WikipediaPage

logger = logging.getLogger(__name__)


@dataclass
class Article:
    """Represents a fetched Wikipedia article."""

    title: str
    summary: str
    content: str
    url: str
    sections: list[dict[str, str]]


class WikipediaFetcher:
    """Fetches articles from Wikipedia."""

    def __init__(self, language: str = config.DEFAULT_WIKIPEDIA_LANGUAGE):
        self.language = language
        self._wiki = wikipediaapi.Wikipedia(
            language,
            headers={"User-Agent": "wikipdf/0.1.0 (https://github.com/wikipdf)"},
        )
        if config.CACHE_ENABLED:
            session = CachedSession(
                cache_name=config.OUTPUT_DIR / ".cache",
                expire_after=config.CACHE_EXPIRY_DAYS * 24 * 3600,
            )
            self._wiki.session = session

    def fetch(self, topic: str) -> Optional[Article]:
        """Fetch a Wikipedia article by topic name.

        Args:
            topic: The Wikipedia article title to fetch.

        Returns:
            Article object if found, None if not found.
        """
        page = self._wiki.page(topic)
        if not page.exists():
            logger.warning(f"Page not found: {topic}")
            return None

        article = Article(
            title=page.title,
            summary=page.summary,
            content=page.text,
            url=page.canonicalurl,
            sections=self._extract_sections(page),
        )
        logger.info(f"Fetched article: {topic}")
        return article

    def _extract_sections(self, page: "WikipediaPage") -> list[dict[str, str]]:
        """Extract sections from a Wikipedia page."""
        sections = []
        for section in page.sections:
            if section.text:
                sections.append(
                    {
                        "title": section.title,
                        "text": section.text,
                    }
                )
        return sections


def fetch_article(topic: str, language: str = "en") -> Optional[Article]:
    """Convenience function to fetch a Wikipedia article."""
    fetcher = WikipediaFetcher(language)
    return fetcher.fetch(topic)
