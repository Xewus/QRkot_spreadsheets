"""Модуль с обработчиками ошибок.
"""
from http import HTTPStatus


from sqlalchemy.exc import IntegrityError        # noqa
from starlette.exceptions import HTTPException


class HTTPExceptionBadRequest(HTTPException):
    """Обработчик ошибки со статус-кодом `400`'
    """
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=detail
        )


class HTTPExceptionMethodNotAllowed(HTTPException):
    """Обработчик ошибки со статус-кодом `405`'
    """
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=HTTPStatus.METHOD_NOT_ALLOWED,
            detail=detail
        )


class HTTPExceptionUnprocessableEntity(HTTPException):
    """Обработчик ошибки со статус-кодом `422`'
    """
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=detail
        )


class HTTPExceptionInternalServerError(HTTPException):
    """Обработчик ошибки со статус-кодом `500`'
    """
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=detail
        )
