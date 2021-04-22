

from Note.cli.validators import _format_tags_callback
from Note.database.database import NoteDatabase, Database
from Note.database.table import Note as NoteTable
import Note.logging_setup

import os
import tempfile
import subprocess
import logging

from enum import Enum
from typing import List, Optional, Iterable, Tuple
from dataclasses import dataclass

import typer

logger = logging.getLogger(__name__)

app = typer.Typer(name="manage", help="Manage the database.")

FILENAME = "tmp_note"
FILEPATH = os.path.join(tempfile.gettempdir(), FILENAME)


class Editor:
    editors = []

    def __init__(self, name: str, args: Tuple):
        self.name = name
        self.args = args
        self.editors.append(self)

    def __eq__(self, b):
        return self.name == b

    def __repr__(self):
        return self.name


class EditorChoice(str, Enum):
    vim = str(Editor("vim", ("vim", "-n", FILEPATH)))
    nano = str(Editor("nano", ("nano", FILEPATH)))


@app.command()
def create(
        message: Optional[str] = typer.Option(
            None, "-m", "--message", show_default=False, help="Message to add to the database."),
        tags: Optional[List[str]] = typer.Option(
            None, "-t", "--tags", show_default=False, help="Tags to organize message.", callback=_format_tags_callback),
        editor: EditorChoice = typer.Option(
            "vim", show_choices=True, help="Supported editors.")):
    """
    Insert note into the database.
    """

    message = message if message else get_message_from_editor(editor)

    logger.info(f"Note message: \n{message}")
    logger.info(f"Note tags: {tags}")

    db = NoteDatabase(Database)

    db.insert_note(NoteTable(content=message.encode("utf-8")))

    note = db.select_note(db.last_row_id)

    db.insert_tag(note.id_, tags)


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


def get_message_from_editor(selected_editor: str) -> str:
    """
    Launch editor and get a note message.
    """

    logger.info(f"Starting {selected_editor}")

    for editor in Editor.editors:
        if editor == selected_editor:

            process = subprocess.run(" ".join(editor.args), shell=True)

            if process.returncode:
                raise Exception(f"{editor} not installed!")

            return _read_message()

    raise NotImplementedError(f"editor: {selected_editor} not implemented.")


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
