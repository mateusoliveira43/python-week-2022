"""Beerlog CLI main script."""

import inspect
from typing import Any, Callable, Optional

import typer

from beerlog.cli.commands import add, list_beers

EPILOG = "\N{clinking beer mugs} Cheers!"

CLI = typer.Typer(
    help="Beer Management Application \N{beer mug}",
    epilog=EPILOG,
    no_args_is_help=True,
)

NUMPY_PARAMS = "Parameters"
GOOGLE_PARAMS = "Args:"
SPHINX_PARAM = ":param"
SPHINX_RETURNS = ":returns"
SPHINX_RAISES = ":raises"
DOCSTRING_SECTIONS = {
    NUMPY_PARAMS: True,
    "Returns": True,
    "Raises": True,
    GOOGLE_PARAMS: True,
    "Returns:": True,
    "Raises:": True,
}


def get_help_from_docstring(command: Callable[..., Any]) -> str:
    """
    Get help message from callable object.

    Parameters
    ----------
    command : Callable[..., Any]
        Callable object (command, callback, ...).

    Returns
    -------
    str
        Docstring summary, if exists.

    """
    docstring = inspect.getdoc(command)
    # if not docstring:
    #     return ""
    docstring_lines = docstring.strip().splitlines()  # type: ignore
    help_message = ""
    for line in docstring_lines:
        if DOCSTRING_SECTIONS.get(line.strip()) or line.strip().startswith(
            (SPHINX_PARAM, SPHINX_RETURNS, SPHINX_RAISES)
        ):
            break
        help_message += line + "\n" if line else ""
    return help_message


def add_command(
    command: Callable[..., Any], name: Optional[str] = None
) -> None:
    """
    Add a command to CLI.

    Parameters
    ----------
    command : Callable[..., Any]
        Command to be added.
    name : Optional[str], optional
        Name of the command, by default None

    """
    CLI.command(
        name=name if name else command.__name__,
        help=get_help_from_docstring(command),
        epilog=CLI.info.epilog,
    )(command)


add_command(add.add)
add_command(list_beers.list_beers, name="list")
