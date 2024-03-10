import datetime
from typing import Literal

from fastapi import APIRouter, Depends, Query, Path

from src.deps import transaction_service
from src.schemes import SLoadDumpResponse, STransactionPage
from src.services import TransactionService

router = APIRouter(tags=["Transactions"])


@router.post(
    "/load_dump",
    response_model=SLoadDumpResponse,
    description="Загружает транзакции с Blockchair за указанную дату в базу данных",
    response_description="Информация о загруженных транзакциях",
)
async def load_dump(
    date: datetime.date = Query(example=datetime.date(2009, 1, 12), description="Дата"),
    service: TransactionService = Depends(transaction_service),
):
    return await service.load_dump(date)


@router.get(
    "/address/{address}",
    response_model=STransactionPage,
    description="Возвращает список транзакций по адресу",
    response_description="Список транзакций",
)
async def get_transactions_by_address(
    address: str = Path(
        example="12cbQLTFMXRnSzktFkuoG3eHoMeFtpTu3S", description="Адрес"
    ),
    transaction_type: Literal["from", "to", "all"] = Query(
        "all", description="Тип транзакции"
    ),
    limit: int = Query(
        100, description="Ограничение на количество транзакций", ge=1, le=100
    ),
    offset: int = Query(0, description="Смещение", ge=0, le=100),
    service: TransactionService = Depends(transaction_service),
):
    return service.get_transactions_by_address(address, transaction_type, limit, offset)
