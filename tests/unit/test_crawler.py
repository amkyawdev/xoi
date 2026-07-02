"""Unit tests for crawler module"""

import pytest

from crawler.parser import HTMLParser
from crawler.cleaner import HTMLCleaner


def test_html_parser():
    """Test HTML parsing"""
    parser = HTMLParser()
    html = "<html><body><h1>Title</h1><p>Content</p></body></html>"
    soup = parser.parse(html)
    assert soup.find("h1").get_text() == "Title"


def test_extract_links():
    """Test link extraction"""
    parser = HTMLParser()
    html = '<html><body><a href="/page1">Link 1</a><a href="/page2">Link 2</a></body></html>'
    links = parser.extract_links(html, "https://example.com")
    assert len(links) == 2


def test_html_cleaner():
    """Test HTML cleaning"""
    cleaner = HTMLCleaner()
    html = "<script>alert('xss')</script><p>Content</p>"
    cleaned = cleaner.clean(html)
    assert "script" not in cleaned
    assert "Content" in cleaned
