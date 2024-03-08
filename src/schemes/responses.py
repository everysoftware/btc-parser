from src.schemes import STransaction
from src.schemes.base import SBase


class SLoadDumpResponse(SBase):
    total: int


class STransactionPage(SBase):
    transactions: list[STransaction]
    total: int
