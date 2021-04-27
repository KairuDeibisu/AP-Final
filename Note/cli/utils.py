
from typing import List

import typer

def display_output(results: List[any]) -> None:
    """
    Display output from database.
    """
    
    if not results:
        error_message = typer.style("Can't find any results!", fg=typer.colors.YELLOW)
        typer.echo()
        typer.echo(error_message)
        typer.echo()
        typer.Exit(1)

    for result in results:
        result.display()
    
    
