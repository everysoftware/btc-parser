from fastapi import Depends

from src.blockchair import BlockchairClient
from src.db import DefaultNeo4jStorage
from src.db.base import Storage
from src.services import TransactionService


def transaction_service(
    storage: Storage = Depends(DefaultNeo4jStorage),
    client: BlockchairClient = Depends(BlockchairClient),
) -> TransactionService:
    return TransactionService(storage, client)
