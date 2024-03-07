from .base import SBase


class STransaction(SBase):
    block_id: int
    hash: str
    time: str
    size: int
    weight: int
    version: int
    lock_time: int
    is_coinbase: bool
    has_witness: bool
    input_count: int
    output_count: int
    input_total: int
    input_total_usd: float
    output_total: int
    output_total_usd: float
    fee: int
    fee_usd: float
    fee_per_kb: float
    fee_per_kb_usd: float
    fee_per_kwu: float
    fee_per_kwu_usd: float
    cdd_total: float


class SAddressTransaction(SBase):
    block_id: int
    hash: str
    time: str
    balance_change: int
