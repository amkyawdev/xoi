"""Scrape command - Extract content from pages"""

import click


@click.command()
@click.argument("url")
@click.option("--selector", "-s", help="CSS selector to extract")
@click.option("--markdown/--no-markdown", default=True, help="Convert to markdown")
def scrape(url: str, selector: str | None, markdown: bool) -> None:
    """Scrape content from a URL"""
    click.echo(f"URL: {url}")
    click.echo(f"Selector: {selector or 'all content'}")
    click.echo(f"Markdown: {markdown}")
    click.echo("\nScraping not yet implemented. Use API endpoint for scraping functionality.")
