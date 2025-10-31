# tests/test_backtest.py
import os
import tempfile
from src.market_data import generate_sample_ticks, tick_stream_from_csv
from src.strategy import SimpleMeanReversion
from src.backtest import Backtester
from src.config import Config

def test_backtest_runs(tmp_path):
    csvp = tmp_path / "ticks.csv"
    generate_sample_ticks(str(csvp), n_ticks=200)
    cfg = Config(default_slippage=0.0, default_fee=0.0)
    strat = SimpleMeanReversion(window=10, entry_z=2.0)
    bt = Backtester(strat, cfg)
    report = bt.run_from_csv(str(csvp))
    assert "n_fills" in report
    assert isinstance(report["positions"], dict)
