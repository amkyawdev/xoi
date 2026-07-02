"""Main CLI entry point"""

import sys
from typing import Optional

import click

from cli.commands import (
    ask, chat, code, crawl, scrape, search, summarize, analyze,
    config, models, health, version
)


@click.group()
@click.option("--debug", is_flag=True, help="Enable debug mode")
@click.pass_context
def main(ctx: click.Context, debug: bool) -> None:
    """Web Agent Platform CLI"""
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug


# Register command groups
main.add_command(ask.ask)
main.add_command(chat.chat)
main.add_command(code.code)
main.add_command(crawl.crawl)
main.add_command(scrape.scrape)
main.add_command(search.search)
main.add_command(summarize.summarize)
main.add_command(analyze.analyze)
main.add_command(config.config)
main.add_command(models.models)
main.add_command(health.health)
main.add_command(version.version)


if __name__ == "__main__":
    main()
