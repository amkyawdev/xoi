"""Models command - List and manage AI models"""

import click


@click.command()
@click.option("--provider", "-p", help="Filter by provider")
@click.option("--json/--no-json", default=False, help="Output as JSON")
def models(provider: str | None, json: bool) -> None:
    """List available AI models"""
    model_list = [
        {"name": "gpt-4", "provider": "openai", "context_length": 8192},
        {"name": "gpt-3.5-turbo", "provider": "openai", "context_length": 16385},
        {"name": "claude-3-opus", "provider": "anthropic", "context_length": 200000},
        {"name": "claude-3-sonnet", "provider": "anthropic", "context_length": 200000},
        {"name": "mixtral-8x7b", "provider": "openrouter", "context_length": 32768},
        {"name": "llama-3-70b", "provider": "openrouter", "context_length": 8192},
    ]
    
    if provider:
        model_list = [m for m in model_list if m["provider"] == provider]
    
    if json:
        import json
        click.echo(json.dumps(model_list, indent=2))
    else:
        for m in model_list:
            click.echo(f"{m['name']} ({m['provider']}) - {m['context_length']} tokens")
