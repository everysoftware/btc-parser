import csv
import datetime
from typing import Sequence, Literal

from src.blockchair import BlockchairClient
from src.db.base import Storage
from src.exceptions import (
    TransactionNotFoundError,
    InputNotFoundError,
    OutputNotFoundError,
)
from src.schemes import LoadDumpResponse, STransaction


class TransactionService:
    def __init__(self, storage: Storage, client: BlockchairClient):
        self.storage = storage
        self.client = client

    async def _get_dump(self, date: datetime.date) -> Sequence[csv.DictReader]:
        """Получение дампа транзакций, входов и выходов."""
        transactions = await self.client.get_dump(date, "transactions")

        if transactions is None:
            raise TransactionNotFoundError()

        inputs = await self.client.get_dump(date, "inputs")

        if inputs is None:
            raise InputNotFoundError()

        outputs = await self.client.get_dump(date, "outputs")

        if outputs is None:
            raise OutputNotFoundError()

        return transactions, inputs, outputs

    async def load_dump(self, date: datetime.date) -> LoadDumpResponse:
        """Загрузка дампа транзакций, входов и выходов в базу данных."""
        self.storage.create_constraints()

        total = self.storage.process_dump(*await self._get_dump(date))

        return LoadDumpResponse(total=total)

    def get_transactions_by_address(
        self, address: str, transaction_type: Literal["from", "to", "all"] = "all"
    ) -> list[STransaction]:
        """Получение списка транзакций по адресу."""
        return self.storage.get_transactions_by_address(address, transaction_type)
