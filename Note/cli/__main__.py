
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
        hostname: str = typer.Option(
            None, envvar="NOTE_HOSTNAME"),
        username: str = typer.Option(
            None, envvar="NOTE_USERNAME"),
        password: str = typer.Option(
            None, envvar="NOTE_PASSWORD")):
    """
    Note Database Manager.
    """

    global CONFIGRATION
    CONFIGRATION = {
        "verbose": verbose,
        "hostname": hostname,
        "username": username,
        "password": password
    }

    if verbose:
        setup(logging.INFO)

    if not all((hostname, username, password)):
        logger.warn("""
        Authentication has not be configred. 
        Add hostname, username, and password to the environment.
            Example:
                NOTE_HOSTNAME = localhost
                NOTE_USERNAME = root
                NOTE_PASSWORD = password1 
        """)


if __name__ == "__main__":
    app()
