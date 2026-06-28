import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import time
from matplotlib import pyplot as plt

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def get_candles(symbol, start_date, end_date, interval=10, engine="stock", market="shares", board="TQBR", show=False):
    url = f"https://iss.moex.com/iss/engines/{engine}/markets/{market}/boards/{board}/securities/{symbol}/candles.json"

    session = requests.Session()
    all_dfs = []
    start = 0
    while True:
        params = {
            "start": start,
            "from": start_date,
            "till": end_date,
            "interval": interval,
        }

        response = session.get(url, params=params, timeout=30)
        data = response.json()

        candles = data.get("candles", {})
        rows = candles.get("data", [])
        cols = candles.get("columns", [])

        all_dfs.append(pd.DataFrame(rows, columns=cols))

        if show:
            print(all_dfs[-1]['begin'].iloc[-1])

        if len(rows) < 500:
            break
        start += 500

    if not all_dfs:
        return pd.DataFrame()

    df = pd.concat(all_dfs, ignore_index=True)
    df["timestamp"] = pd.to_datetime(df["begin"])
    df.set_index("timestamp", inplace=True)
    df.drop(columns=["begin"], inplace=True)

    return df

def save_candles_df(df, file_name):
    path = os.path.join(DATA_DIR, file_name)
    df.to_csv(path, index=False)

def main():
    start_date = datetime(2020, 6, 20)
    end_date = datetime(2026, 6, 27)
    ticker = "SBER"

    candles = get_candles(ticker, start_date, end_date, interval=10, market="shares")
    save_candles_df(candles, f"{ticker}.csv")

    candles = pd.read_csv(os.path.join(DATA_DIR, f"{ticker}.csv"))
    candles['end'] = pd.to_datetime(candles['end'])
    candles.set_index('end', inplace=True)
    candles = candles.resample('1h').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    })

    closes = candles['close'].values
    times = candles.index

    plt.plot(times, closes)
    plt.show()

if __name__ == "__main__":
    main()