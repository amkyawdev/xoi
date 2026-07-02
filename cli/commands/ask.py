"""Ask command - Query the AI agent"""

import click
import httpx


@click.command()
@click.argument("question")
@click.option("--model", "-m", help="Model to use")
@click.option("--stream/--no-stream", default=False, help="Enable streaming response")
def ask(question: str, model: str | None, stream: bool) -> None:
    """Ask a question to the AI agent"""
    # Placeholder implementation
    click.echo(f"Question: {question}")
    click.echo(f"Model: {model or 'default'}")
    click.echo(f"Stream: {stream}")
    click.echo("\nThis is a placeholder. Connect to API for actual functionality.")
