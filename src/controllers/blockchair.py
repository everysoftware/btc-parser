import datetime
from typing import Literal

from fastapi import APIRouter, Depends, Query

from src.blockchair import BlockchairClient

router = APIRouter(tags=["Blockchair"])


@router.get(
    "/transactions/date",
    description="Получить транзакции за день",
)
async def get_dump(
    dump_type: Literal["transactions", "inputs", "outputs"] = Query("transactions"),
    date: datetime.date = Query(datetime.date(2009, 1, 12)),
    client: BlockchairClient = Depends(BlockchairClient),
):
    transactions = list(await client.get_dump(date, dump_type))

    return transactions
