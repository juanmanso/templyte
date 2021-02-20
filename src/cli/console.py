import click

from . import __version__


@click.command()
@click.version_option(version=__version__)
def main():
    """CLI for the templyte project."""
    click.echo("Hello, world!")

