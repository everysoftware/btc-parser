import datetime
from typing import Literal

from src.blockchair import BlockchairClient
from src.db.base import Storage
from src.exceptions import (
    TransactionNotFoundError,
    InputNotFoundError,
    OutputNotFoundError,
)
from src.schemes import SLoadDumpResponse, STransactionPage


class TransactionService:
    def __init__(self, storage: Storage, client: BlockchairClient):
        self.storage = storage
        self.client = client

    async def _load_dumps(self, date: datetime.date) -> tuple[str, str, str]:
        """Получение дампа транзакций, входов и выходов."""
        transactions = await self.client.load_dump(date, "transactions")

        if transactions is None:
            raise TransactionNotFoundError()

        inputs = await self.client.load_dump(date, "inputs")

        if inputs is None:
            raise InputNotFoundError()

        outputs = await self.client.load_dump(date, "outputs")

        if outputs is None:
            raise OutputNotFoundError()

        return transactions, inputs, outputs

    async def load_dump(self, date: datetime.date) -> SLoadDumpResponse:
        """Загрузка дампа транзакций, входов и выходов в базу данных."""
        self.storage.create_constraints()

        dumps = await self._load_dumps(date)

        total = self.storage.process_dump(*dumps)

        return SLoadDumpResponse(total=total)

    def get_transactions_by_address(
        self,
        address: str,
        transaction_type: Literal["from", "to", "all"] = "all",
        limit: int = 100,
        offset: int = 0,
    ) -> STransactionPage:
        """Получение списка транзакций по адресу."""
        transactions = self.storage.get_transactions_by_address(
            address, transaction_type, limit, offset
        )
        return STransactionPage(transactions=transactions, total=len(transactions))
