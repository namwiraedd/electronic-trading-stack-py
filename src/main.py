# main.py
import argparse
from .market_data import generate_sample_ticks
from .strategy import SimpleMeanReversion
from .backtest import Backtester
from .config import Config
import os
import logging

logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate-sample", action="store_true")
    parser.add_argument("--backtest", type=str, help="path to ticks csv")
    args = parser.parse_args()

    data_path = os.path.join(os.getcwd(), "data", "sample_ticks.csv")
    if args.generate_sample:
        os.makedirs("data", exist_ok=True)
        generate_sample_ticks(data_path, n_ticks=1000)
        print("Sample ticks generated at:", data_path)
        return

    if args.backtest:
        cfg = Config()
        strat = SimpleMeanReversion(window=50, entry_z=2.5)
        bt = Backtester(strat, cfg)
        report = bt.run_from_csv(args.backtest)
        print("Backtest report:", report)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
