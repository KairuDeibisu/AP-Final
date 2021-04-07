
from Note.utils.strings import StringBuilder

import logging

import typer

logger = logging.getLogger(__name__)

app = typer.Typer(name="search", help="Search the database.")


@app.command()
def list():
    pass
