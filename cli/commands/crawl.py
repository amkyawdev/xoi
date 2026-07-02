"""Crawl command - Web crawling"""

import click


@click.command()
@click.argument("url")
@click.option("--depth", "-d", default=2, help="Crawl depth")
@click.option("--output", "-o", help="Output file path")
@click.option("--format", "-f", type=click.Choice(["json", "markdown", "html"]), default="markdown", help="Output format")
def crawl(url: str, depth: int, output: str | None, format: str) -> None:
    """Crawl a website starting from URL"""
    click.echo(f"URL: {url}")
    click.echo(f"Depth: {depth}")
    click.echo(f"Format: {format}")
    click.echo(f"Output: {output or 'stdout'}")
    click.echo("\nCrawling not yet implemented. Use API endpoint for crawling functionality.")
