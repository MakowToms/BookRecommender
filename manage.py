"""This file sets up a command line manager.

Use "python manage.py" for a list of available commands.
Use "python manage.py runserver" to start the development web server on localhost:5000.
Use "python manage.py runserver --help" for additional runserver options.
"""

import click
# from flask_migrate import MigrateCommand
from flask.cli import FlaskGroup

from app import create_app


@click.group(cls=FlaskGroup, create_app=create_app)
@click.pass_context
def cli(ctx):
    """Management script for the Wiki application."""
    if ctx.parent:
        click.echo(ctx.parent.get_help())


if __name__ == "__main__":
    cli()
