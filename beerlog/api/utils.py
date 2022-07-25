"""Utils functionalities for API module."""

from fastapi import HTTPException, status

from beerlog.serializers import OperationFinished


def parse_result(result: OperationFinished) -> OperationFinished:
    """
    Parse a database operation result.

    Parameters
    ----------
    result : OperationFinished
        Information about a database operation.

    Returns
    -------
    OperationFinished
        Information about a database operation.

    Raises
    ------
    HTTPException
        If database operation was not successful.

    """
    if result.was_successful:
        return result
    # TODO parse error to return appropriate status code
    raise HTTPException(
        detail=result.message, status_code=status.HTTP_400_BAD_REQUEST
    )
