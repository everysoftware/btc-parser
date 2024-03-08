from typing import Literal

from neo4j import GraphDatabase, basic_auth, Driver

from src.db.base import Storage
from src.schemes import STransaction


class Neo4jStorage(Storage):
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
                CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.address IS UNIQUE
            """
            )

    def get_transactions_by_address(
        self, address: str, transaction_type: Literal["from", "to", "all"] = "all"
    ) -> list[STransaction]:
        """Получение транзакций по адресу."""

        with self.driver.session() as session:
            match transaction_type:
                case "from":
                    result = session.run(
                        """
                        MATCH (t:Transaction)-[:TRANSACTION_TO]->(u:User {address: $address})
                        RETURN t
                        """,
                        address=address,
                    )
                case "to":
                    result = session.run(
                        """
                        MATCH (t:Transaction)-[:TRANSACTION_FROM]->(u:User {address: $address})
                        RETURN t
                        """,
                        address=address,
                    )
                case "all":
                    result = session.run(
                        """
                        MATCH (t:Transaction)-[:TRANSACTION_FROM|TRANSACTION_TO]->(u:User {address: $address})
                        RETURN DISTINCT t
                        """,
                        address=address,
                    )
                case _:
                    raise ValueError("Invalid transaction type")

            return [STransaction.model_validate(record["t"]) for record in result]
