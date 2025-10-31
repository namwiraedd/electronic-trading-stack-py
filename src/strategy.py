# strategy.py
from typing import Dict, List
import numpy as np

class BaseStrategy:
    """
    Minimal interface for strategies.
    Implement on_tick to produce desired order intents.
    """
    def __init__(self):
        pass

    def on_tick(self, tick: Dict) -> List[Dict]:
        """
        tick: {timestamp, symbol, price, size}
        return list of orders: {"symbol","side","qty","type","limit_price"}
        """
        raise NotImplementedError

class SimpleMeanReversion(BaseStrategy):
    """
    Very small illustrative mean-reversion strategy using rolling zscore on price.
    Not production alpha — educational template only.
    """
    def __init__(self, window=50, entry_z=2.0, exit_z=0.5):
        self.window = window
        self.entry_z = entry_z
        self.exit_z = exit_z
        self.prices = []

    def on_tick(self, tick):
        price = tick["price"]
        self.prices.append(price)
        if len(self.prices) < self.window:
            return []
        window = self.prices[-self.window:]
        mean = np.mean(window)
        std = np.std(window, ddof=1) if len(window) > 1 else 0.0
        z = (price - mean) / (std + 1e-9)
        orders = []
        # if price is far above mean -> short; far below -> buy
        if z > self.entry_z:
            # short 1 unit
            orders.append({"symbol": tick["symbol"], "side": "SELL", "qty": 1, "type": "MARKET"})
        elif z < -self.entry_z:
            orders.append({"symbol": tick["symbol"], "side": "BUY", "qty": 1, "type": "MARKET"})
        # exit conditions could be implemented by a portfolio layer; keep simple here.
        return orders
