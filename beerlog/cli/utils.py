"""Utils functionalities for CLI module."""

from rich.console import Console
from rich.table import Table

from beerlog.serializers import BeerOut, OperationFinished

console = Console()


def print_table(result: OperationFinished) -> None:
    """
    Print a formatted table for BeerOut model.

    Parameters
    ----------
    result : OperationFinished
        Information about a database operation.

    """
    table = Table(title=result.message)
    headers = BeerOut.__fields__.keys()
    headers_formatted = [
        header[:-1] if header[-1] == "_" else header for header in headers
    ]
    for header in headers_formatted:
        table.add_column(header, style="magenta")
    for beer in result.beers:
        values = [str(getattr(beer, header)) for header in headers]
        table.add_row(*values)
    console.print(table)


def parse_result(result: OperationFinished) -> None:
    """
    Parse a database operation result.

    Parameters
    ----------
    result : OperationFinished
        Information about a database operation.

    Raises
    ------
    SystemExit
        If database operation was not successful.

    """
    if result.was_successful:
        return print_table(result=result)
    print(result.message)
    # TODO parse error to return appropriate return code
    raise SystemExit(1)
