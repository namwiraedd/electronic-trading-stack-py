# backtest.py
from typing import List, Dict
from .market_data import tick_stream_from_csv
from .strategy import BaseStrategy
from .execution import ExecutionSimulator
from .risk import RiskManager
from .config import Config
import logging

logger = logging.getLogger(__name__)

class Backtester:
    def __init__(self, strategy: BaseStrategy, cfg: Config):
        self.strategy = strategy
        self.cfg = cfg
        self.exec_sim = ExecutionSimulator(cfg)
        self.risk = RiskManager(cfg)
        self.fills = []
        self.pnl = 0.0
        self.cash = 0.0

    def run_from_csv(self, path: str):
        for tick in tick_stream_from_csv(path):
            try:
                orders = self.strategy.on_tick(tick)
                # risk check
                allowed = self.risk.check_orders(orders, self.exec_sim.positions)
                fills = self.exec_sim.execute_orders(allowed, tick)
                self._record_fills_and_update_pnl(fills)
            except Exception as e:
                logger.exception("Error processing tick: %s", e)
        return self.summary()

    def _record_fills_and_update_pnl(self, fills: List[Dict]):
        for f in fills:
            self.fills.append(f)
            # simple PnL cumulative: negative for buys (cash out), positive for sells
            if f["side"] == "BUY":
                self.cash -= f["price"] * f["qty"] + f["fee"]
            else:
                self.cash += f["price"] * f["qty"] - f["fee"]
        # simple mark-to-market PnL using last prices could be added

    def summary(self):
        return {
            "n_fills": len(self.fills),
            "cash": self.cash,
            "positions": self.exec_sim.positions
        }
