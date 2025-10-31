# config.py
from dataclasses import dataclass

@dataclass
class Config:
    base_currency: str = "USD"
    default_slippage: float = 0.0005   # fraction of price (50 bps = 0.005)
    default_fee: float = 0.0001        # fraction
    latency_ms: int = 2                # simulated network/roundtrip latency
    max_position: float = 100000.0     # max position in base units
    pnl_limit: float = -50000.0        # stop-loss for strategy
