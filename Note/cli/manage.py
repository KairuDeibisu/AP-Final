

from Note.cli.validators import _format_tags_callback

import os
import tempfile
import subprocess
import logging

from enum import Enum
from typing import List, Optional

import typer

import Note.logging_setup

logger = logging.getLogger(__name__)

app = typer.Typer(name="manage", help="Manage the database.")

FILENAME = "tmp_note"
FILEPATH = os.path.join(tempfile.gettempdir(), FILENAME)

EDITORS = {
    "vim": ("vim", "-n", FILEPATH),
    "nano": ("nano", FILEPATH)
}


class CLIEditors(str, Enum):
    vim = "vim"
    nano = "nano"


@app.command()
def create(
        message: Optional[str] = typer.Option(
            None, "-m", "--message", show_default=False, help="Message to add to the database."),
        tags: Optional[List[str]] = typer.Option(
            None, "-t", "--tags", show_default=False, help="Tags to organize message.", callback=_format_tags_callback),
        editor: CLIEditors = typer.Option(
            "vim", show_choices=True, help="Supported editors.")):
    """
    Insert note into the database.
    """

    message = message if message else get_message_from_editor(editor)

    logger.info(f"Note message: \n{message}")
    logger.info(f"Note tags: {tags}")


@app.command()
def remove(
    id_: int = typer.Argument(
        ..., metavar="id", help="Note to remove."),
    delete: bool = typer.Option(
        False, show_default=False, confirmation_prompt=True, help="Delete note forever.")):
    """
    Remove note from database.
    """
    pass


def get_message_from_editor(editor="vim") -> str:
    """
    Launch editor and get note message.
    """

    logger.info(f"Starting {editor}")

    if (args := EDITORS.get(editor, None)):
        subprocess.run(args)
        return _read_message()

    raise NotImplementedError(f"editor: {editor} not implemented.")


def _read_message() -> str:
    """

    Read message from tmp file.

    Returns:
        data: test in message file.
    """

    try:
        with open(FILEPATH, "r") as f:
            data = f.read()
        return data
    except FileNotFoundError:
        typer.echo("Aborting!")
        typer.Exit(1)
    finally:
        _remove_tmp_file()


def _remove_tmp_file():
    """
    Cleans up tmp file.
    """

    try:
        os.remove(FILEPATH)
    except FileNotFoundError:
        pass
