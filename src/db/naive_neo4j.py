import csv
from contextlib import suppress

from neo4j import Session
from neo4j.exceptions import ConstraintError

from src.db.neo4j import Neo4jStorage
from src.schemes import STransaction, SInput, SOutput


class NaiveNeo4jStorage(Neo4jStorage):
    def _process_transactions(self, session: Session, transactions: csv.DictReader) -> int:
        """Обработка транзакций и запись в базу данных."""
        total = 0

        for transaction in transactions:
            model = STransaction.model_validate(transaction)
            params = model.model_dump()

            with suppress(ConstraintError):
                session.run(
                    """
                    CREATE (t:Transaction $params)
                """,
                    {"params": params},
                )

            total += 1

        return total

    def _process_inputs(self, session: Session, inputs: csv.DictReader) -> None:
        """Обработка входов и запись в базу данных."""
        for item in inputs:
            model = SInput.model_validate(item)
            params = model.model_dump()

            with suppress(ConstraintError):
                session.run(
                    """
                    CREATE (i:Input $props)
                    WITH i
                    MATCH (t:Transaction {hash: $transaction_hash})
                    CREATE (i)-[:INPUT_TO]->(t)
                """,
                    {"props": params, "transaction_hash": model.transaction_hash},
                )

    def _process_outputs(self, session: Session, outputs: csv.DictReader) -> None:
        """Обработка выходов и запись в базу данных."""
        for output in outputs:
            model = SOutput.model_validate(output)
            params = model.model_dump()

            with suppress(ConstraintError):
                session.run(
                    """
                    CREATE (o:Output $props)
                    WITH o
                    MATCH (t:Transaction {hash: $transaction_hash})
                    CREATE (t)-[:OUTPUT_TO]->(o)
                """,
                    {"props": params, "transaction_hash": model.transaction_hash},
                )
