import datetime

from fastapi import APIRouter, Depends, Query

from src.deps import transaction_service
from src.schemes import LoadDumpResponse
from src.services import TransactionService

router = APIRouter(tags=["Transactions"])


@router.get(
    "/load_dump",
    response_model=LoadDumpResponse,
    description="Загружает транзакции с Blockchair за указанную дату",
    response_description="Информация о загруженных транзакциях",
)
async def load_dump(
    date: datetime.date = Query(datetime.date(2009, 1, 12)),
    service: TransactionService = Depends(transaction_service),
):
    return await service.load_dump(date)
