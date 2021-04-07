
import os
import tempfile
import subprocess
import logging

import typer


logger = logging.getLogger(__name__)

app = typer.Typer(name="manage", help="Manage the database.")

FILENAME = "tmp_note"
FILEPATH = os.path.join(tempfile.gettempdir(), FILENAME)

EDITORS = {
    "vim": ("vim", "-n", FILEPATH)
}


@app.command()
def create(
    message: str =
        typer.Option(None, "-m", show_default=False,
                     help="The message to add to the database.", ),
    tags: str =
        typer.Option("", "-t", show_default=False, help="Tags to organize message.")):
    """
    Insert note into the database.
    """

    message = message if message else get_message_from_editor()

    tags = tags.split(",") if tags else ""
    tags = [tag.replace(" ", "-") for tag in tags]

    logger.info(f"Note message: \n{message}")
    logger.info(f"Note tags: \n{tags}")


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
        exit(0)
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
