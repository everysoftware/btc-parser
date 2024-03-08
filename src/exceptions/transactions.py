from fastapi import HTTPException
from starlette import status


class TransactionAlreadyExistsError(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Транзакция уже существует"
        )


class TransactionNotFoundError(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail="Транзакция не найдена"
        )


class InputNotFoundError(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail="Входы транзакции не найдены"
        )


class OutputNotFoundError(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail="Выходы транзакции не найдены"
        )
