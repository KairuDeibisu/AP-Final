
from Note.logging_setup import setup
from Note.cli import manage
from Note.cli import search

import os
import logging

import typer
from dotenv import load_dotenv


logger = logging.getLogger(__name__)

app = typer.Typer(name="Note")
app.add_typer(manage.app)
app.add_typer(search.app)

load_dotenv()

configration = {
    "verbose": False,
    "hostname": os.getenv("NOTE_HOSTNAME"),
    "username": os.getenv("NOTE_USERNAME"),
    "password": os.getenv("NOTE_PASSWORD")}


@app.callback()
def main(verbose: bool = False):
    """
    Note Database Manager.
    """

    configration["verbose"] = verbose

    if verbose:
        setup(logging.INFO)


if __name__ == "__main__":
    app()
