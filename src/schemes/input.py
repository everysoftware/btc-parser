from src.schemes.base import SBase


class SInput(SBase):
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
    is_spendable: bool
    spending_block_id: int
    spending_transaction_hash: str
    spending_index: int
    spending_time: str
    spending_value_usd: float
    spending_sequence: int
    spending_signature_hex: str
    spending_witness: str
    lifespan: int
    cdd: float
