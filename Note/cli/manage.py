

from Note.cli.validators import _format_tags_callback
from Note.cli.search import search_by_id
from Note.cli.utils import display_output
from Note.database.database import NoteDatabase, Database
from Note.database.table import Note as NoteTable

from enum import Enum
from typing import List, Optional, Tuple
import os
import tempfile
import subprocess
import sys

import typer

app = typer.Typer(name="manage", help="Manage the database.")

FILENAME = "tmp_note"
FILEPATH = os.path.join(tempfile.gettempdir(), FILENAME)


class Editor:
    """
    Editor defines command a line text editor. 
    """

    editors = []

    def __init__(self, name: str, args: Tuple):
        """Constructor

        Args:
            name: the name of the command line editor.
            args: arguments to pass into the command line editor.
        """

        self.name = name
        self.args = args
        self.editors.append(self)

    def __eq__(self, b):
        return self.name == b

    def __repr__(self):
        return self.name


class EditorChoice(str, Enum):
    """
    Define command line editors
    """

    vim = str(Editor("vim", ("vim", "-n", FILEPATH)))
    nano = str(Editor("nano", ("nano", FILEPATH)))


@app.command()
def add(
        message: Optional[str] = typer.Option(
            None, "-m", "--message", show_default=False, help="Message to add to the database."),
        tags: Optional[List[str]] = typer.Option(
            None, "-t", "--tags", show_default=False, help="Tags to organize message.", callback=_format_tags_callback),
        editor: EditorChoice = typer.Option(
            "vim", show_choices=True, help="Write a note in selected editor.")):
    """
    Add note to the database.

    Args:
        message: A note to add to the database directly.
        tags: The tags to attach to a note.
        editor: The selected command line editor to use.

    """

    message = message if message else get_message_from_editor(editor)

    db = NoteDatabase(Database)

    db.insert_note(NoteTable(content=message.encode("utf-8")))

    note = db.select_note_by_id(db.last_row_id)

    db.insert_tag(note.id_, set(tags))

    search_by_id(db.last_row_id)


@app.command()
def remove(
    id_: int = typer.Argument(
        ..., metavar="id", help="The id of the note to hide/delete from list."),
    delete: bool = typer.Option(
        False, show_default=False, confirmation_prompt=True, help="Delete note from list forever.")):
    """
    Hide or Delete a note from the database.

    Args:
        id_: The id of the selected note to hide.
        delete: A Flag to delete a note out right.
    """

    db = NoteDatabase(Database)

    if delete:
        db.delete_note(id_)
    else:
        db.set_note_active_value(id_, False)
        result = db.select_note_by_id(id_,)

        display_output([result])


@app.command()
def recover(
    id_: int = typer.Argument(
        ..., metavar="id", help="The id of the note to recover."),
):
    """
    Restore a hidden note in the database.

    Args:
        id_: The id of the note to restore. Only effect's hidden notes.

    """

    db = NoteDatabase(Database)

    db.set_note_active_value(id_, value=True)

    result = db.select_note_by_id(id_)

    display_output([result])


def get_message_from_editor(editor_: str) -> str:
    """
    Launch editor and get message content's.

    Args:
        editor_: The name of the editor to use.

    Raises:
        Exception: if editor_ is not installed.
        NotImplementError: if editor_ usage is not define.

    """

    for editor in Editor.editors:
        if editor == editor_:

            process = subprocess.run(" ".join(editor.args), shell=True)

            if process.returncode:
                raise Exception(f"{editor} not installed!")

            return _read_message()

    raise NotImplementedError(f"editor: {editor_} not implemented.")


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
        sys.exit(1)
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
