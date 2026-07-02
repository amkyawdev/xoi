"""Config command - Configuration management"""

import click

from cli.utils import load_config, save_config, ensure_config_dir


@click.group()
def config() -> None:
    """Manage CLI configuration"""
    pass


@config.command()
def show() -> None:
    """Show current configuration"""
    cfg = load_config()
    import json
    click.echo(json.dumps(cfg, indent=2))


@config.command()
@click.option("--key")
@click.option("--value")
def set(key: str | None, value: str | None) -> None:
    """Set configuration value"""
    if not key or not value:
        click.echo("Both --key and --value are required")
        return
    cfg = load_config()
    cfg[key] = value
    save_config(cfg)
    click.echo(f"Set {key} = {value}")


@config.command()
def init() -> None:
    """Initialize configuration directory"""
    ensure_config_dir()
    click.echo("Configuration directory initialized")
