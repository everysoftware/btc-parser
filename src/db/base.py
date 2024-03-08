import csv
from typing import Protocol


class Storage(Protocol):

    def create_constraints(self) -> None:
        """Создание ограничений в базе данных."""
        pass

    def process_dump(
        self,
        transactions: csv.DictReader,
        inputs: csv.DictReader,
        outputs: csv.DictReader,
    ) -> int:
        """Обработка данных из csv-файлов и запись в базу данных."""
        pass
