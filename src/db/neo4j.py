import csv
import itertools
from typing import TypeVar

from neo4j import Session

from src.db.neo4j_base import Neo4jStorage
from src.schemes import STransaction, SInput, SOutput
from src.schemes.base import SBase

T = TypeVar("T", bound=SBase)


class DefaultNeo4jStorage(Neo4jStorage):
    def process_dump(
        self,
        transactions_path: str,
        inputs_path: str,
        outputs_path: str,
        block_size: int = 5000,
    ) -> int:
        """Обработка данных из csv-файлов и запись в базу данных."""
        with self.driver.session() as session:
            with open(transactions_path) as transactions_f, open(
                inputs_path
            ) as inputs_f, open(outputs_path) as outputs_f:
                total = self._process_transactions(
                    session, csv.DictReader(transactions_f, delimiter="\t"), block_size
                )
                self._process_inputs(
                    session, csv.DictReader(inputs_f, delimiter="\t"), block_size
                )
                self._process_outputs(
                    session, csv.DictReader(outputs_f, delimiter="\t"), block_size
                )

            return total

    @staticmethod
    def _item_generator(items: csv.DictReader, model: type[T]):
        for item in items:
            yield model.model_validate(item).model_dump()

    def _process_transactions(
        self, session: Session, transactions: csv.DictReader, block_size: int
    ) -> int:
        """Обработка транзакций и запись в базу данных."""

        transaction_gen = self._item_generator(transactions, STransaction)
        transaction_list = list(itertools.islice(transaction_gen, block_size))
        count = 0

        while transaction_list:
            session.run(
                """
                UNWIND $params AS param
                MERGE (t:Transaction {block_id: param.block_id, hash: param.hash, time: param.time, size: param.size, weight: param.weight, version: param.version, lock_time: param.lock_time, is_coinbase: param.is_coinbase, has_witness: param.has_witness, input_count: param.input_count, output_count: param.output_count, input_total: param.input_total, input_total_usd: param.input_total_usd, output_total: param.output_total, output_total_usd: param.output_total_usd, fee: param.fee, fee_usd: param.fee_usd, fee_per_kb: param.fee_per_kb, fee_per_kb_usd: param.fee_per_kb_usd, fee_per_kwu: param.fee_per_kwu, fee_per_kwu_usd: param.fee_per_kwu_usd, cdd_total: param.cdd_total})
                """,
                {"params": transaction_list},
            )
            count += len(transaction_list)
            transaction_list = list(itertools.islice(transaction_gen, block_size))

        return count

    def _process_inputs(
        self, session: Session, inputs: csv.DictReader, block_size: int
    ) -> None:
        """Обработка входов и запись в базу данных."""
        input_gen = self._item_generator(inputs, SInput)
        input_list = list(itertools.islice(input_gen, block_size))

        while input_list:
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
            input_list = list(itertools.islice(input_gen, block_size))

    def _process_outputs(
        self, session: Session, outputs: csv.DictReader, block_size: int
    ) -> None:
        """Обработка выходов и запись в базу данных."""
        output_gen = self._item_generator(outputs, SOutput)
        output_list = list(itertools.islice(output_gen, block_size))

        while output_list:
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
            output_list = list(itertools.islice(output_gen, block_size))
