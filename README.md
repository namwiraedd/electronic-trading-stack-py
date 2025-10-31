# Electronic Trading Stack (Python scaffold)

Lightweight, production-oriented scaffold for an electronic trading stack:
- Market data ingestion (CSV / live adapter stub)
- Strategy module (pluggable)
- Backtester & execution simulator with slippage modeling
- Risk controls (position & pnl limits)
- Unit tests and CI-ready layout

## Quickstart
1. Create venv: `python -m venv venv && source venv/bin/activate`
2. Install deps: `pip install -r requirements.txt`
3. Generate sample data: `python src/main.py --generate-sample`
4. Run backtest: `python src/main.py --backtest data/sample_ticks.csv`
5. Run tests: `pytest -q`

## Notes
- This repo is intended as a robust engineering starting point. Replace the execution adapter with your exchange/broker SDK when ready.
- Always run QA, legal reviews, and run live-tests with strict risk gating before any real-money deployment.
