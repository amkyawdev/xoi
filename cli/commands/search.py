"""Search command - Web search"""

import click


@click.command()
@click.argument("query")
@click.option("--engine", "-e", type=click.Choice(["google", "bing", "ddg"]), default="ddg", help="Search engine")
@click.option("--limit", "-l", default=10, help="Number of results")
def search(query: str, engine: str, limit: int) -> None:
    """Search the web"""
    click.echo(f"Query: {query}")
    click.echo(f"Engine: {engine}")
    click.echo(f"Limit: {limit}")
    click.echo("\nSearch not yet implemented. Use API endpoint for search functionality.")
