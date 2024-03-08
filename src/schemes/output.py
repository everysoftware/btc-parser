from src.schemes.base import SBase


class SOutput(SBase):
    block_id: int
    transaction_hash: str
    index: int
    time: str
    value: int
    value_usd: float
    recipient: str
    type: str
    script_hex: str
    is_from_coinbase: bool
    is_spendable: int
