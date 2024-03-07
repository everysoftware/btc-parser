import csv
import datetime
import gzip
import io
from typing import Any, TypeVar, Literal

import aiohttp
from starlette import status

from src.schemes import STransaction, SAddressTransaction
from src.schemes.base import SBase

T = TypeVar("T", bound=SBase)


def to_models(transactions: list[dict[str, Any]], model: type[T]) -> list[T]:
    """Преобразует список словарей в список моделей."""
    return [model.model_validate(t) for t in transactions]


class BlockchairClient:
    """Клиент для работы с API Blockchair."""

    api_base_url: str = "https://api.blockchair.com/bitcoin"
    """Базовый URL для API."""
    dumps_base_url: str = "https://gz.blockchair.com/bitcoin"
    """Базовый URL для дампов."""
    dump_models: dict[str, type[SBase]] = {
        "transactions": STransaction,
        "inputs": STransaction,
        "outputs": STransaction,
    }
    """Модели для дампов."""

    async def get_transactions(
        self, limit: int = 10, offset: int = 0
    ) -> list[STransaction] | None:
        """Получает список последних транзакций."""
        url = f"{self.api_base_url}/transactions?limit={limit}&offset={offset}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != status.HTTP_200_OK:
                    return None

                response = await response.json()
                transactions = response["data"]

                return to_models(transactions, STransaction)

    async def get_address_transactions(
        self, address: str, limit: int = 10, offset: int = 0
    ) -> list[SAddressTransaction] | None:
        """Получает список транзакций по адресу."""
        url = f"{self.api_base_url}/dashboards/address/{address}?transaction_details=true&limit={limit}&offset={offset}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != status.HTTP_200_OK:
                    return None

                response = await response.json()

                transactions = response["data"][address]["transactions"]

                return to_models(transactions, SAddressTransaction)

    async def get_dump(
        self,
        date: datetime.date,
        dump_type: Literal["transactions", "inputs", "outputs"],
    ) -> csv.DictReader | None:
        """Получает дамп транзакций за день."""
        date_str = date.strftime("%Y%m%d")
        url = f"{self.dumps_base_url}/{dump_type}/blockchair_bitcoin_{dump_type}_{date_str}.tsv.gz"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != status.HTTP_200_OK:
                    return None

                compressed_data = await response.read()
                decompressed_data = gzip.decompress(compressed_data)
                text_data = decompressed_data.decode()

                return csv.DictReader(io.StringIO(text_data), delimiter="\t")
