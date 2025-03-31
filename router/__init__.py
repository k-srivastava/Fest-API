"""Core router functions required in every route."""
from starlette import status

from starlette.exceptions import HTTPException


def not_found_error(exception: Exception) -> HTTPException:
    """
    Generic exception for 404 Not Found.

    :param exception: Specific exception that occurred.
    :type exception: Exception

    :return: HTTP 404 Not Found exception enclosing the base exception.
    :rtype: HTTPException
    """
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exception))


def validation_error(exception: Exception) -> HTTPException:
    """
    Generic exception for 400 Bad Request.

    :param exception: Specific exception that occurred.
    :type exception: Exception

    :return: HTTP 400 Bad Request exception enclosing the base exception.
    :rtype: HTTPException
    """
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception))
