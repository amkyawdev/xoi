"""Chat command - Interactive conversation"""

import click


@click.command()
@click.option("--session", "-s", help="Session ID to continue")
@click.option("--model", "-m", help="Model to use")
def chat(session: str | None, model: str | None) -> None:
    """Start an interactive chat session"""
    click.echo("Starting interactive chat...")
    click.echo(f"Session: {session or 'new'}")
    click.echo(f"Model: {model or 'default'}")
    click.echo("\nChat is not yet implemented. Use API endpoint for chat functionality.")
