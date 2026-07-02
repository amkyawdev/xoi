"""Version command - Show version information"""

import click


@click.command()
@click.option("--json/--no-json", default=False, help="Output as JSON")
def version(json: bool) -> None:
    """Show version information"""
    from cli import __version__
    
    version_info = {
        "name": "web-agent-platform",
        "version": __version__,
        "python_version": "3.10+"
    }
    
    if json:
        import json
        click.echo(json.dumps(version_info, indent=2))
    else:
        click.echo(f"web-agent-platform v{__version__}")
