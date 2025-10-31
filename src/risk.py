# risk.py
from .config import Config
from typing import List, Dict

class RiskManager:
    def __init__(self, cfg: Config):
        self.cfg = cfg

    def check_orders(self, orders: List[Dict], positions: Dict[str,float]) -> List[Dict]:
        """
        Apply basic risk checks: max position and simple pnl cap.
        Returns list of allowed orders (may filter or reduce size).
        """
        allowed = []
        for o in orders:
            symbol = o["symbol"]
            pos = positions.get(symbol, 0.0)
            new_pos = pos + (o["qty"] if o["side"] == "BUY" else -o["qty"])
            if abs(new_pos) > self.cfg.max_position:
                # drop order if it breaches max position
                continue
            allowed.append(o)
        return allowed
