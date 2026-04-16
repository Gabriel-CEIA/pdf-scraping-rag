"""Configuration settings for wikipdf."""

from pathlib import Path

OUTPUT_DIR = Path("output")
NAMING_CONVENTION = "underscore"
CACHE_ENABLED = True
CACHE_EXPIRY_DAYS = 7

DEFAULT_WIKIPEDIA_LANGUAGE = "en"

PDF_FONT_SIZE_TITLE = 18
PDF_FONT_SIZE_SECTION = 14
PDF_FONT_SIZE_BODY = 11
PDF_MARGIN = 15
PDF_PAGE_SIZE = "A4"
