import csv

from neo4j import Session

from src.db.neo4j_base import Neo4jStorage
from src.schemes import STransaction, SInput, SOutput


class DefaultNeo4jStorage(Neo4jStorage):
    def process_dump(
        self,
        transactions_path: str,
        inputs_path: str,
        outputs_path: str,
    ) -> int:
        """Обработка данных из csv-файлов и запись в базу данных."""
        with self.driver.session() as session:
            with open(transactions_path) as transactions_f, open(
                inputs_path
            ) as inputs_f, open(outputs_path) as outputs_f:
                total = self._process_transactions(
                    session, csv.DictReader(transactions_f, delimiter="\t")
                )
                self._process_inputs(session, csv.DictReader(inputs_f, delimiter="\t"))
                self._process_outputs(
                    session, csv.DictReader(outputs_f, delimiter="\t")
                )

            return total

    @staticmethod
    def _process_transactions(session: Session, transactions: csv.DictReader) -> int:
        """Обработка транзакций и запись в базу данных."""
        transaction_list = [
            STransaction.model_validate(transaction).model_dump()
            for transaction in transactions
        ]

        session.run(
            """
            UNWIND $params AS param
            MERGE (t:Transaction {block_id: param.block_id, hash: param.hash, time: param.time, size: param.size, weight: param.weight, version: param.version, lock_time: param.lock_time, is_coinbase: param.is_coinbase, has_witness: param.has_witness, input_count: param.input_count, output_count: param.output_count, input_total: param.input_total, input_total_usd: param.input_total_usd, output_total: param.output_total, output_total_usd: param.output_total_usd, fee: param.fee, fee_usd: param.fee_usd, fee_per_kb: param.fee_per_kb, fee_per_kb_usd: param.fee_per_kb_usd, fee_per_kwu: param.fee_per_kwu, fee_per_kwu_usd: param.fee_per_kwu_usd, cdd_total: param.cdd_total})
            """,
            {"params": transaction_list},
        )

        return len(transaction_list)

    @staticmethod
    def _process_inputs(session: Session, inputs: csv.DictReader) -> None:
        """Обработка входов и запись в базу данных."""
        input_list = [SInput.model_validate(item).model_dump() for item in inputs]

        session.run(
            """
            UNWIND $props AS prop
            MERGE (i:Input {block_id: prop.block_id, transaction_hash: prop.transaction_hash, index: prop.index, time: prop.time, value: prop.value, value_usd: prop.value_usd, recipient: prop.recipient, type: prop.type, script_hex: prop.script_hex, is_from_coinbase: prop.is_from_coinbase, is_spendable: prop.is_spendable, spending_block_id: prop.spending_block_id, spending_transaction_hash: prop.spending_transaction_hash, spending_index: prop.spending_index, spending_time: prop.spending_time, spending_value_usd: prop.spending_value_usd, spending_sequence: prop.spending_sequence, spending_signature_hex: prop.spending_signature_hex, spending_witness: prop.spending_witness, lifespan: prop.lifespan, cdd: prop.cdd})
            WITH i
            MATCH (t:Transaction {hash: i.transaction_hash})
            MERGE (i)-[:INPUT_TO]->(t)
            MERGE (u:User {address: i.recipient})
            MERGE (t)-[:TRANSACTION_FROM]->(u)
            """,
            {"props": input_list},
        )

    @staticmethod
    def _process_outputs(session: Session, outputs: csv.DictReader) -> None:
        """Обработка выходов и запись в базу данных."""
        output_list = [
            SOutput.model_validate(output).model_dump() for output in outputs
        ]

        session.run(
            """
            UNWIND $props AS prop
            MERGE (o:Output {block_id: prop.block_id, transaction_hash: prop.transaction_hash, index: prop.index, time: prop.time, value: prop.value, value_usd: prop.value_usd, recipient: prop.recipient, type: prop.type, script_hex: prop.script_hex, is_from_coinbase: prop.is_from_coinbase, is_spendable: prop.is_spendable})
            WITH o
            MATCH (t:Transaction {hash: o.transaction_hash})
            MERGE (t)-[:OUTPUT_TO]->(o)
            MERGE (u:User {address: o.recipient})
            MERGE (t)-[:TRANSACTION_TO]->(u)
            """,
            {"props": output_list},
        )
