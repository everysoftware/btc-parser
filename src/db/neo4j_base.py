from typing import Literal

from neo4j import GraphDatabase, basic_auth, Driver

from src.config import settings
from src.db.base import Storage
from src.schemes import STransaction


class Neo4jStorage(Storage):
    driver: Driver

    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.neo4j_url,
            auth=basic_auth(settings.neo4j_user, settings.neo4j_password),
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
            session.run(
                """
                CREATE INDEX IF NOT EXISTS FOR (u:User) ON (u.address)
            """
            )

    def get_transactions_by_address(
        self,
        address: str,
        transaction_type: Literal["from", "to", "all"] = "all",
        limit: int = 100,
        offset: int = 0,
    ) -> list[STransaction]:
        """Получение транзакций по адресу."""

        with self.driver.session() as session:
            match transaction_type:
                case "from":
                    result = session.run(
                        """
                        MATCH (t:Transaction)-[:TRANSACTION_TO]->(u:User {address: $address})
                        RETURN t
                        SKIP $offset
                        LIMIT $limit
                        """,
                        address=address,
                        limit=limit,
                        offset=offset,
                    )
                case "to":
                    result = session.run(
                        """
                        MATCH (t:Transaction)-[:TRANSACTION_FROM]->(u:User {address: $address})
                        RETURN t
                        SKIP $offset
                        LIMIT $limit
                        """,
                        address=address,
                        limit=limit,
                        offset=offset,
                    )
                case "all":
                    result = session.run(
                        """
                        MATCH (t:Transaction)-[:TRANSACTION_FROM|TRANSACTION_TO]->(u:User {address: $address})
                        RETURN DISTINCT t
                        SKIP $offset
                        LIMIT $limit
                        """,
                        address=address,
                        limit=limit,
                        offset=offset,
                    )
                case _:
                    raise ValueError("Invalid transaction type")

            return [STransaction.model_validate(record["t"]) for record in result]
