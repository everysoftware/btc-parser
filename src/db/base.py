import csv
from typing import Protocol, Literal

from src.schemes import STransaction


class Storage(Protocol):

    def create_constraints(self) -> None:
        """Создание ограничений в базе данных."""
        pass

    def process_dump(
        self,
        transactions_path: str,
        inputs_path: str,
        outputs_path: str,
    ) -> int:
        """Обработка данных из csv-файлов и запись в базу данных."""
        pass

    def get_transactions_by_address(
        self, address: str, transaction_type: Literal["from", "to", "all"]
    ) -> list[STransaction]:
        """Получение списка транзакций по адресу."""
        pass
