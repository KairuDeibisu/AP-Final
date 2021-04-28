

from Note.cli import manage
from Note.cli import search

import typer

app = typer.Typer(name="Note")
app.add_typer(manage.app)
app.add_typer(search.app)

if __name__ == "__main__":
    app()
