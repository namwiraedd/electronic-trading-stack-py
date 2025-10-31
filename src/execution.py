# execution.py
import time
from typing import Dict, List
from .config import Config
import random

class ExecutionSimulator:
    """
    Simulates execution with slippage and fees, returns fills.
    """
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.positions = {}  # symbol -> position

    def apply_slippage(self, price: float, side: str) -> float:
        """
        Simple slippage model: proportion of price plus random noise.
        """
        direction = -1 if side == "BUY" else 1  # buys move price up
        slip = direction * price * (self.cfg.default_slippage * (1 + random.random()*0.5))
        return price + slip

    def execute_orders(self, orders: List[Dict], tick: Dict) -> List[Dict]:
        fills = []
        for o in orders:
            exec_price = tick["price"] if o["type"] == "MARKET" else o.get("limit_price", tick["price"])
            exec_price = self.apply_slippage(exec_price, o["side"])
            fee = exec_price * o["qty"] * self.cfg.default_fee
            # update positions
            pos = self.positions.get(o["symbol"], 0.0)
            if o["side"] == "BUY":
                pos += o["qty"]
            else:
                pos -= o["qty"]
            self.positions[o["symbol"]] = pos
            fills.append({
                "timestamp": tick["timestamp"],
                "symbol": o["symbol"],
                "side": o["side"],
                "qty": o["qty"],
                "price": exec_price,
                "fee": fee
            })
            # simulate latency
            time.sleep(self.cfg.latency_ms / 1000.0)
        return fills
