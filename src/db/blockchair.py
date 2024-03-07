import csv

from py2neo import Graph, Node, Relationship

from src.schemes import STransaction, SInput, SOutput

graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))


def process_transactions(transactions: csv.DictReader) -> None:
    for transaction in transactions:
        model = STransaction.model_validate(transaction)

        node = Node(
            "Transaction",
            id=model.hash,
            **model.model_dump(exclude={"hash"}),
        )

        graph.create(node)


def process_inputs(inputs: csv.DictReader) -> None:
    for item in inputs:
        model = SInput.model_validate(item)

        node = Node(
            "Input",
            **model.model_dump()
        )

        graph.create(node)

        transaction = graph.nodes.match(
            "Transaction", id=model.transaction_hash
        ).first()
        graph.create(Relationship(node, "INPUT_TO", transaction))


def process_outputs(outputs: csv.DictReader) -> None:
    for output in outputs:
        model = SOutput.model_validate(output)

        node = Node(
            "Output",
            **model.model_dump()
        )

        graph.create(node)

        transaction = graph.nodes.match(
            "Transaction", id=model.transaction_hash
        ).first()
        graph.create(Relationship(transaction, "OUTPUT_TO", node))
