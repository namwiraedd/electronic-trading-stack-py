# tests/test_risk.py
from src.risk import RiskManager
from src.config import Config

def test_risk_blocks_large_order():
    cfg = Config(max_position=5)
    rm = RiskManager(cfg)
    positions = {"SYM": 0}
    orders = [{"symbol": "SYM", "side": "BUY", "qty": 10}]
    allowed = rm.check_orders(orders, positions)
    assert allowed == []
