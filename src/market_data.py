# market_data.py
import pandas as pd
import numpy as np
from typing import Iterator, Dict
import time
import csv

def tick_stream_from_csv(path: str) -> Iterator[Dict]:
    """
    Stream tick-level data from a CSV. CSV should have: timestamp, symbol, price, size.
    Yields dicts in chronological order.
    """
    df = pd.read_csv(path, parse_dates=["timestamp"])
    df = df.sort_values("timestamp")
    for _, row in df.iterrows():
        yield {
            "timestamp": row["timestamp"],
            "symbol": row.get("symbol", "SYM"),
            "price": float(row["price"]),
            "size": int(row.get("size", 1))
        }

def generate_sample_ticks(path: str, n_ticks: int = 500, seed: int = 42):
    """
    Creates a small synthetic tick file to bootstrap testing.
    """
    np.random.seed(seed)
    start = pd.Timestamp("2025-01-01T09:00:00")
    times = [start + pd.Timedelta(milliseconds=int(1000*np.random.exponential(0.5))) * i for i in range(n_ticks)]
    prices = 100 + np.cumsum(np.random.normal(0, 0.05, size=n_ticks))
    sizes = np.random.randint(1, 50, size=n_ticks)
    with open(path, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "symbol", "price", "size"])
        for t,p,s in zip(times, prices, sizes):
            writer.writerow([t.isoformat(), "SYM", f"{p:.4f}", s])
