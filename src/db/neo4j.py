import csv
from typing import Protocol

from neo4j import GraphDatabase, basic_auth, Driver

from src.db.base import Storage


class Neo4jStorage(Storage, Protocol):
    driver: Driver

    def __init__(self):
        self.driver = GraphDatabase.driver(
            "bolt://localhost:7687", auth=basic_auth("neo4j", "password")
        )
        self.driver.verify_connectivity()

    def create_constraints(self) -> None:
        """Создание ограничений и индексов для базы данных."""
        with self.driver.session() as session:
            session.run(
                """
                CREATE CONSTRAINT IF NOT EXISTS FOR (t:Transaction) REQUIRE t.hash IS UNIQUE
            """
            )
            session.run(
                """
                CREATE CONSTRAINT IF NOT EXISTS FOR (i:Input) REQUIRE (i.transaction_hash, i.index) IS NODE KEY
            """
            )
            session.run(
                """
                CREATE CONSTRAINT IF NOT EXISTS FOR (o:Output) REQUIRE (o.transaction_hash, o.index) IS NODE KEY
            """
            )
            session.run(
                """
                CREATE INDEX IF NOT EXISTS FOR (i:Input) ON (i.recipient)
                """
            )
            session.run(
                """
                CREATE INDEX IF NOT EXISTS FOR (o:Output) ON (o.recipient)
                """
            )

    def _process_transactions(self, session, transactions: csv.DictReader) -> int:
        """Обработка транзакций и запись в базу данных."""
        pass

    def _process_inputs(self, session, inputs: csv.DictReader) -> None:
        """Обработка входов и запись в базу данных."""
        pass

    def _process_outputs(self, session, outputs: csv.DictReader) -> None:
        """Обработка выходов и запись в базу данных."""
        pass

    def process_dump(
            self,
            transactions: csv.DictReader,
            inputs: csv.DictReader,
            outputs: csv.DictReader,
    ) -> int:
        """Обработка данных из csv-файлов и запись в базу данных."""
        with self.driver.session() as session:
            total = self._process_transactions(session, transactions)
            self._process_inputs(session, inputs)
            self._process_outputs(session, outputs)

            return total
