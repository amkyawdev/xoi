"""Health command - Check system health"""

import click


@click.command()
@click.option("--url", "-u", default="http://localhost:8000", help="API URL")
def health(url: str) -> None:
    """Check API health status"""
    click.echo(f"Checking health at: {url}")
    click.echo("\nHealth check not yet implemented. Connect to API for actual status.")
