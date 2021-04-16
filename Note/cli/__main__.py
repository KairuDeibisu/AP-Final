
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


@app.callback()
def main(
        verbose: bool = False,
        password: str = typer.Option(
            None, envvar="NOTE_PASSWORD")):
    """
    Note Database Manager.
    """

    global CONFIGRATION
    CONFIGRATION = {
        "verbose": verbose,
        "password": password
    }

    if verbose:
        setup(logging.INFO)

    if not password:
        logger.warn("""
        Authentication has not be configred. 
        Add sql password to the environment.
            Example:
                NOTE_PASSWORD = password1 
        """)


if __name__ == "__main__":
    app()
